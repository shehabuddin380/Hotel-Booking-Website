# 🏨 Hotel Booking Website (Django + DRF)

A full-featured **Hotel Booking System** built with **Django, Django REST Framework (DRF), JWT Authentication, and Swagger API Docs**.  
This project allows users to search hotels, make bookings, leave reviews, and provides an **Admin Dashboard** with analytics.

---

## 🚀 Features

### 🔑 Authentication
- User Registration & Login
- JWT Authentication (Access + Refresh Tokens)
- Role-based Access (User vs Admin)

### 🏨 Hotels
- List, Create, Update, Delete Hotels
- View Hotel Details with Reviews
- Upload Hotel Images (Media Files)

### 📅 Bookings
- Book Hotels with Check-in & Check-out dates
- Confirm / Cancel Bookings
- User can see their own bookings

### ⭐ Reviews
- Leave reviews with ratings & comments
- Fetch hotel reviews with hotel details

### 📊 Admin Dashboard
- Booking stats (last week, last month)
- Top 5 Hotels (by bookings)
- Top 5 Users (by bookings)
- Sales comparison (month & year wise)

### 📖 API Documentation
- Swagger UI available at: `/swagger/`
- Redoc available at: `/redoc/`

---

## ⚙️ Tech Stack

- **Backend:** Django 5 + Django REST Framework
- **Authentication:** JWT (`djangorestframework-simplejwt`)
- **API Docs:** drf-yasg (Swagger, Redoc)
- **Debugging:** Django Debug Toolbar
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)
- **Environment:** Python 3.12, Virtualenv

---

## 📂 Project Structure

