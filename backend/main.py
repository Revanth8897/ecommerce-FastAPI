from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
import models
import schemas
import auth
import crud
import razorpay
from uuid import uuid4
from auth import get_current_user
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

razorpay_client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development ONLY
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

# ---------------- AUTH ----------------

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# login

@app.post("/login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user or not auth.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.email})
    return {
    "access_token": token,
    "token_type": "bearer",
    "is_admin": user.is_admin
}


# ---------------- PRODUCTS ----------------

@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only admin users can create products"
        )

    return crud.create_product(db, product)


@app.get("/products/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    db_product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.price = product.price
    db_product.description = product.description

    db.commit()
    db.refresh(db_product)

    return db_product

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    if not crud.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}


# ---------------- CART ----------------

@app.post("/cart")
def add_to_cart(
    cart: schemas.CartCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    item = crud.add_to_cart(db, user.id, cart.product_id, cart.quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Added to cart"}

@app.get("/cart", response_model=list[schemas.CartResponse])
def view_cart(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.get_cart(db, user.id)

@app.delete("/cart/{cart_id}")
def delete_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    item = crud.remove_from_cart(db, cart_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item removed"}

@app.put("/cart/{cart_id}", response_model=schemas.CartResponse)
def update_cart_item(
    cart_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart_item = db.query(models.Cart).filter(
        models.Cart.id == cart_id,
        models.Cart.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if quantity <= 0:
        db.delete(cart_item)
        db.commit()
        raise HTTPException(status_code=200, detail="Item removed")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)

    return cart_item


# ---------------- ORDERS ----------------
@app.post("/orders", response_model=schemas.OrderResponse)
def place_order(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = crud.create_order(db, user.id)

    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")

    return order


@app.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_user_orders(db, current_user.id)

from uuid import uuid4

@app.put("/orders/{order_id}/pay")
def mark_order_paid(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # ✅ UPDATE ORDER STATUS
    order.status = "PAID"

    # ✅ CREATE PAYMENT RECORD (THIS WAS MISSING)
    payment = models.Payment(
        order_id=order.id,
        amount=order.total_amount,      # REQUIRED
        payment_method="ONLINE",
        status="SUCCESS",
        transaction_id=str(uuid4())
    )

    db.add(payment)
    db.commit()

    return {"message": "Payment successful"}

#payment api
@app.put("/orders/{order_id}/pay", response_model=schemas.PaymentResponse)
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    payment = crud.create_payment(db, order)
    return payment

# Create Razorpay Order API 
@app.post("/razorpay/order")
def create_razorpay_order(
    data: schemas.RazorpayOrderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == data.order_id,
        models.Order.user_id == user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    amount_paise = int(order.total_amount * 100)

    rp_order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": f"order_{order.id}",
        "payment_capture": 1
    })

    order.razorpay_order_id = rp_order["id"]
    db.commit()

    return {
        "razorpay_order_id": rp_order["id"],
        "amount": amount_paise,
        "currency": "INR",
        "key": os.getenv("RAZORPAY_KEY_ID")
    }

# Razorpay Payment Verification API

@app.post("/razorpay/verify")
def verify_payment(
    data: schemas.RazorpayVerify,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": data.razorpay_order_id,
            "razorpay_payment_id": data.razorpay_payment_id,
            "razorpay_signature": data.razorpay_signature
        })
    except:
        raise HTTPException(status_code=400, detail="Payment verification failed")

    order = db.query(models.Order).filter(
        models.Order.razorpay_order_id == data.razorpay_order_id
    ).first()

    order.status = "PAID"

    payment = models.Payment(
        order_id=order.id,
        amount=order.total_amount,
        payment_method="RAZORPAY",
        status="SUCCESS",
        transaction_id=data.razorpay_payment_id
    )

    db.add(payment)
    db.commit()

    return {"message": "Payment successful"}

# refund api
@app.post("/payments/{payment_id}/refund")
def refund_payment(
    payment_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    payment = db.query(models.Payment).filter(
        models.Payment.transaction_id == payment_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    refund = razorpay_client.payment.refund(payment_id)

    payment.status = "REFUNDED"
    db.commit()

    return {
        "message": "Refund successful",
        "refund_id": refund["id"]
    }
