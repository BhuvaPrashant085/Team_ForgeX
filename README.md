# 🎙️ Team ForgeX — AI Voice Billing System

> **An AI-powered, voice-controlled restaurant billing system** that converts spoken orders into accurate bills in real time — built with Django, Web Speech API, and fuzzy NLP matching.

---

## 🏆 Problem Statement

Restaurant billing is slow, error-prone, and staff-intensive. Waiters manually entering orders leads to:
- Human error in item entry
- Slow table turnaround
- Language/accent barriers with POS systems

**Team ForgeX solves this** by letting staff simply *speak* the order — the system does the rest.

---

## 🚀 Key Features

| Feature | Description |
|--------|-------------|
| 🎙️ **Voice Ordering** | Speak orders naturally — "2 cheese pizza and 1 coke" |
| 🧠 **AI NLP Matching** | Fuzzy matching handles typos, accents, and partial names |
| 🌐 **Hindi Number Support** | Understands *ek, do, teen, char, paanch* |
| 📋 **Live Bill Panel** | Real-time subtotal + 5% GST + discount calculation |
| 👤 **Guest Profiles** | Loyalty points, visit count, mobile-linked customer history |
| 🏷️ **Smart Discounts** | % or fixed discounts + loyalty points redemption at checkout |
| 💳 **Multi-Payment** | Cash, UPI/Online, Card — all tracked per bill |
| 📊 **Admin Dashboard** | Full control over tables, menu, bills, and customers |
| 🔄 **Auto Table Free** | Table status resets automatically after payment |
| 📱 **Responsive UI** | Works on tablets used by restaurant staff |

---

## 🛠️ Tech Stack

```
Frontend  →  Vanilla HTML/CSS/JS + Web Speech API (Chrome)
Backend   →  Django 4.x + SQLite
NLP       →  Custom fuzzy string matching (difflib + token ratio)
Auth      →  Django session auth (admin panel)
Realtime  →  Polling-based bill sync (no WebSocket needed)
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-team/team-forgex.git
cd team-forgex

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Seed initial tables, menu items & sample data
python manage.py seed_data

# 6. Create admin superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Main dashboard |
| http://127.0.0.1:8000/admin/ | Django admin panel |
| http://127.0.0.1:8000/admin-dashboard/ | Custom admin panel |

> ⚠️ **Voice recognition requires Google Chrome** — uses the Web Speech API with `lang: en-IN` for Indian English accent support.

---

## 🗣️ How Voice Ordering Works

```
Staff speaks → "2 paneer tikka and 1 mango lassi"
       ↓
Web Speech API transcribes in real time
       ↓
POST /api/parse-voice/ — NLP fuzzy matches to menu items
       ↓
Detected items appear instantly on the bill panel
       ↓
Staff confirms → bill auto-calculates with GST
       ↓
Payment selected → table freed → dashboard updated
```

**Supported voice commands:**

| Voice Command | Action |
|---------------|--------|
| *"2 butter chicken and 1 naan"* | Adds items to bill |
| *"generate bill"* | Opens bill preview |
| *"settle in cash / online / card"* | Processes payment |
| *"go to tables"* / *"dashboard"* | Navigates back |
| *"ek lassi"*, *"do pizza"* | Hindi number support |

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/parse-voice/` | NLP parse voice text → matched menu items |
| `GET`  | `/api/bill/<id>/` | Fetch current bill with items + totals |
| `POST` | `/api/bill/<id>/add-items/` | Add or merge items into bill |
| `POST` | `/api/bill/<id>/remove-item/<item_id>/` | Remove item from bill |
| `POST` | `/api/bill/<id>/generate/` | Finalize bill with discount + guest info |
| `POST` | `/api/bill/<id>/set-payment/` | Set payment method + mark paid |
| `GET`  | `/api/menu/` | Full menu list |
| `GET`  | `/api/customer/lookup/?mobile=` | Fetch guest profile + loyalty points |
| `POST` | `/api/table/<id>/free/` | Mark table as free after payment |

---

## 🗂️ Project Structure

```
team_forgex/
├── manage.py
├── requirements.txt
├── README.md
│
├── voice_billing/               ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── billing/                     ← Core application
    ├── models.py                ← MenuItem, Table, Customer, Bill, BillItem
    ├── views.py                 ← All views + NLP voice parser engine
    ├── urls.py                  ← URL routing
    ├── admin.py                 ← Django admin configuration
    ├── management/
    │   └── commands/
    │       └── seed_data.py     ← Initial data seeder
    └── templates/billing/
        ├── dashboard.html       ← Table grid + paid/pending bills
        └── billing.html         ← Voice ordering + bill panel
```

---

## 👥 Data Models

```python
Table        → id, name, status (free/occupied)
MenuItem     → id, item_name, price, category
Customer     → id, name, mobile_number, points, visit_count, created_at
Bill         → id, table, customer_name, subtotal, gst, discount, total,
               payment_method, status (open/pending/paid), created_at
BillItem     → id, bill, menu_item, qty, subtotal
```

---

## 🔮 Innovation Highlights

- **Zero hardware dependency** — runs on any device with a Chrome browser, no special POS hardware needed
- **Accent-aware NLP** — trained fuzzy matching handles Indian English pronunciations and common mishearings
- **Loyalty engine** — automatic point tracking per customer mobile number with redemption at checkout
- **One-page billing flow** — entire order → bill → payment in a single screen, no page reloads

---

## 👨‍💻 Team ForgeX

> Built with ❤️ for [Hackathon Name] · [Date]

| Member | Role |
|--------|------|
| [Name] | Backend & NLP |
| [Name] | Frontend & Voice UI |
| [Name] | Django APIs & Database |
| [Name] | Admin Panel & Testing |
