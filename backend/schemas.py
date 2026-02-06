from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# ================= USER =================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool


# ================= PRODUCT =================

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    stock: int = 0


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None



# ================= CART =================

class CartCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartProductResponse(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    quantity: int
    product: CartProductResponse

    class Config:
        from_attributes = True


# ================= ORDER =================

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


# ================= PAYMENT =================

class PaymentCreate(BaseModel):
    order_id: int
    payment_method: str


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: str
    transaction_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# razorpay 
class RazorpayOrderCreate(BaseModel):
    order_id: int

class RazorpayOrderResponse(BaseModel):
    razorpay_order_id: str
    amount: int
    currency: str

class RazorpayVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
