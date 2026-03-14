# FinPay by VORTEx 🚀

FinPay is a full-stack, responsive fintech web application simulator. It demonstrates modern neobanking features including automated round-up savings, live QR code scanning, multi-user authentication, and gamified reward milestones.

Designed with a lightweight yet robust architecture, it features a custom-built, pure-Python Machine Learning engine to predict user spending habits and integrates with cloud PostgreSQL for permanent data persistence.

## ✨ Key Features

* **Secure User Authentication:** Full multi-user support with account registration and session-based state management. Every user gets an isolated balance and transaction history.
* **Persistent Cloud Storage:** Configured to work with **PostgreSQL (Neon/Supabase)** for production and **SQLite** for local development, ensuring data survives server restarts.
* **Round-Up Auto-Savings:** Simulates spare change investing by automatically rounding up transactions and routing the difference to a "Virtual Piggy Bank."
* **Pure Python ML Spend Prediction:** Uses a from-scratch implementation of **Ordinary Least Squares (Linear Regression)** to forecast future spending based on user history.
* **Gamified Milestones:** Tracks spending targets. Upon completion, a weighted randomizer dispenses cash rewards or discount coupons.
* **Live QR Code Scanner:** Integrates the device camera to scan real-world UPI QR codes, decode the payload, and auto-fill the payment pipeline.
* **Responsive Glassmorphic UI:** A modern, mobile-first dark-mode design that expands into a comprehensive dual-column dashboard on desktop.

## 🛠️ Tech Stack

**Backend & Data Layer:**

* **Python 3 / Flask:** Core logic and routing.
* **SQLAlchemy:** ORM for database flexibility.
* **PostgreSQL:** Production-grade permanent data storage.
* **Gunicorn:** WSGI HTTP Server for production deployment.

**Frontend UI/UX:**

* **HTML5 / CSS3:** Custom responsive styling with backdrop-filter glassmorphism.
* **Vanilla JavaScript:** Asynchronous API fetches and DOM state rendering.
* **APIs:** `html5-qrcode` (scanning), UI Avatars, and QR Server API.

## 📁 Project Structure

```text
FinPay_Simulator/
│
├── instance/               
│   └── finpay.db           # Local SQLite database (for development only)
├── static/                 
│   └── logo.jpeg           # Application branding
├── templates/              
│   └── index.html          # Frontend UI, CSS styling, and JS controllers
├── .gitignore              # Instructions for Git to ignore junk & local DB
├── requirements.txt        # Production dependencies
└── app.py                  # Main Flask server, auth logic, & ML engine


