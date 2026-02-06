from sqlalchemy.orm import Session
import models
import schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
  
def get_all_products(db: Session):
    return db.query(models.Product).all()
  
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, data):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return False

    db.delete(product)
    db.commit()
    return True

#cart crud logic
def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    # ✅ CHECK PRODUCT EXISTS
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None

    cart_item = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = models.Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

def get_cart(db: Session, user_id: int):
    return (
        db.query(models.Cart)
        .filter(models.Cart.user_id == user_id)
        .all()
    )


def remove_from_cart(db: Session, cart_id: int):
    item = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item    
  
  # order crud logic
def create_order(db: Session, user_id: int):
    cart_items = db.query(models.Cart).filter(
        models.Cart.user_id == user_id
    ).all()

    if not cart_items:
        return None

    order = models.Order(user_id=user_id, total_amount=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    total = 0

    for item in cart_items:
        price = item.product.price
        total += item.quantity * price

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.add(order_item)
 
    order.total_amount = total

    db.query(models.Cart).filter(
        models.Cart.user_id == user_id
    ).delete()

    db.commit()
    db.refresh(order)  

    return order

def get_user_orders(db: Session, user_id: int):
  return db.query(models.Order).filter(models.Order.user_id == user_id).all()

#payment
from uuid import uuid4
from models import Payment

def create_payment(db, order):
    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        payment_method="ONLINE",
        status="SUCCESS",
        transaction_id=str(uuid4())
    )

    order.status = "PAID"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


