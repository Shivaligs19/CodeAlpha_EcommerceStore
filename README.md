# CodeAlpha E-commerce
This is a simple Django e-commerce project.
# 🛒 ShopEase – Online Grocery Store

## 📌 About the Project

ShopEase is a Django-based online grocery shopping application developed as part of the CodeAlpha Internship.

The application allows customers to browse grocery products, search for items, filter products by category, add products to their shopping cart, and place orders online.

It also provides an administration dashboard for managing products, orders, and stock.

## ✨ Features

- User Registration and Login
- User Authentication
- Product Listing
- Product Details
- Product Search
- Category Filtering
- Shopping Cart Management
- Add and Remove Cart Items
- Quantity Updates
- Checkout System
- Order Placement
- Order History
- Order Status Management
- Automatic Stock Management
- Out-of-Stock Protection
- Django Admin Dashboard
- Product Image Management

## 💻 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Django | Web Framework |
| HTML5 | Website Structure |
| CSS3 | Website Styling |
| JavaScript | Interactive Features |
| SQLite | Database |
| VS Code | Development Environment |

## 📂 Project Structure

```text
CodeAlpha_EcommerceStore/
│
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── store/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── home.html
│   ├── cart.html
│   ├── checkout.html
│   ├── login.html
│   ├── register.html
│   └── order_history.html
│
├── media/
├── venv/
├── manage.py
├── db.sqlite3
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd CodeAlpha_EcommerceStore
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

### 5. Install Django

```bash
pip install django
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

### 8. Open the Application

```text
http://127.0.0.1:8000/
```

## 🎯 Project Objective

The main objective of ShopEase is to provide a simple and user-friendly online grocery shopping experience.

Customers can conveniently purchase grocery products online, while administrators can manage products, inventory, and customer orders.

## 🚀 Future Enhancements

- Online Payment Gateway Integration
- Email Order Notifications
- Advanced Product Recommendations
- Product Ratings and Reviews
- Delivery Tracking
- Enhanced Admin Analytics

## 👩‍💻 Internship

**Internship Organization:** CodeAlpha

**Project Name:** ShopEase – Online Grocery Store

**Project Type:** Full-Stack Web Development

**Backend:** Python Django

**Frontend:** HTML, CSS and JavaScript

---

© 2026 ShopEase. All Rights Reserved.