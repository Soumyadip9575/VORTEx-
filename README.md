# FinPay by VORTEx 🚀

FinPay is a full-stack, responsive fintech web application simulator. It demonstrates modern neobanking features including automated round-up savings, live QR code scanning, and gamified reward milestones. 

Designed with a lightweight architecture, it features a custom-built, pure-Python Machine Learning engine to predict user spending habits without relying on heavy external data science libraries.

## ✨ Key Features

* **Round-Up Auto-Savings:** Simulates spare change investing by automatically rounding up transactions to the nearest ₹10 or ₹100 and routing the difference to a "Virtual Piggy Bank."
* **Pure Python ML Spend Prediction:** Uses a from-scratch implementation of Ordinary Least Squares (Linear Regression) to forecast future transaction amounts based on historical data arrays.
* **Spending Analytics & AI Insights:** Real-time categorization of expenses to determine favorite spending categories, accompanied by dynamic, rule-based "AI" prompts.
* **Gamified Milestones:** Tracks category-specific spending targets. Upon completion, a weighted randomizer dispenses pure cash rewards or discount coupons (e.g., Domino's, Amazon, Uber).
* **Live QR Code Scanner:** Integrates your device's camera to scan real-world UPI QR codes, decode the payload, and auto-fill the payment pipeline.
* **Responsive Fintech UI:** A glassmorphic, mobile-first design that automatically expands into a comprehensive dual-column analytics dashboard on desktop screens.

## 🛠️ Tech Stack

**Backend & Data Layer:**
* **Python 3:** Core logic, routing, and mathematical modeling.
* **Flask:** Lightweight WSGI web application framework.
* **Standard Libraries:** `math`, `random`, `datetime`.
* **Database:** In-memory state management (Python dictionaries/lists for lightweight prototyping).

**Frontend UI/UX:**
* **HTML5 / CSS3:** Custom, framework-free responsive styling (CSS Grid & Flexbox).
* **Vanilla JavaScript:** DOM manipulation, asynchronous API fetches (`fetch`), and state rendering.
* **Libraries & APIs:** `html5-qrcode` (camera scanning), UI Avatars API, QR Server API.

## 📁 Project Structure

```text
FinPay_Simulator/
│
├── app.py                  # Main Flask server, backend logic, and ML model
├── static/                 
│   └── logo.jpeg           # Application branding
└── templates/              
    └── index.html          # Frontend UI, CSS, and JS controllers