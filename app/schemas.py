from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Customers
class CustomerBase(BaseModel):
    name: str
    sex: Optional[str] = None
    dob: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


# Products
class ProductBase(BaseModel):
    name: str
    sku: str
    unit_in_stock: int
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


# OrderDetail read/create
class OrderDetailBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    creation_time: datetime

    class Config:
        orm_mode = True


# Orders
class OrderBase(BaseModel):
    code: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    customer_id: int


class OrderCreate(OrderBase):
    details: Optional[List[OrderDetailCreate]] = []


class Order(OrderBase):
    id: int
    creation_time: datetime
    details: List[OrderDetail] = []

    class Config:
        orm_mode = True
