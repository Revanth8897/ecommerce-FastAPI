# 🛒 E-Commerce Web Application

A full-stack E-Commerce application built using **FastAPI** with **JWT authentication**, **MySQL**, and **Razorpay (Test Mode)** payment integration.  
Includes **Admin Dashboard** for product management and **User flow** for ordering products.


##  Features

###  User
- User Registration & Login (JWT Authentication)
- View Products
- Add to Cart
- Place Orders
- Razorpay Test Mode Payments
- Order History

###  Admin
- Admin Login
- Create Products
- Update Products
- Delete Products
- Manage Inventory


##  Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Razorpay Payment Gateway (Test Mode)

### Frontend
- HTML
- CSS
- JavaScrip



##  Environment Variables

Create a `.env` file in the backend root directory and add the following:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ecommerce_db

SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxx


##  Author

**Revanth8897**  
Aspiring Software Engineer | Backend Python Developer  

- GitHub: https://github.com/Revanth8897  
- Skills: Python, FastAPI, SQLAlchemy, MySQL, JWT, Razorpay, HTML, CSS, JavaScript  
- Focus: Backend Development & Full Stack Projects

