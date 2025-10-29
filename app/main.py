from fastapi import FastAPI
from database import engine, Base
from routers import customers, products, orders, order_details

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI PostgreSQL CRUD Example")

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(order_details.router)
