<<<<<<< HEAD
# Team_ForgeX
Team ForgeX is an AI-powered voice-controlled restaurant billing system that converts spoken orders into accurate bills in real time.
=======
# Voice Billing System — Django

A voice-based restaurant billing system built with Django + SQLite.

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install Django
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Seed tables and menu data
python manage.py seed_data

# 5. Create admin user
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

Then open: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

## Features
- 10 tables on dashboard (free / occupied)
- Tap a table → opens billing page
- Tap mic button → speak order (e.g. "2 cheese pizza and 1 coke")
- Voice text sent to Django `/api/parse-voice/` → fuzzy matched to menu
- Detected items shown with "Add" / "Add All" buttons
- Bill auto-calculates subtotal + 5% GST + total
- Click any menu item manually to add qty 1
- Generate Bill → marks bill paid, frees table, shows receipt modal

## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/parse-voice/ | Parse voice text, return matched items |
| GET  | /api/bill/<id>/ | Get current bill |
| POST | /api/bill/<id>/add-items/ | Add/merge items to bill |
| POST | /api/bill/<id>/remove-item/<item_id>/ | Remove item |
| POST | /api/bill/<id>/generate/ | Finalize bill |
| GET  | /api/menu/ | Get full menu list |

## Voice Note
- Works in Chrome (Web Speech API)
- Language set to en-IN (supports Indian English accent)
- Supports Hindi numbers: ek, do, teen, char, paanch

## Project Structure
```
voice_billing/
├── manage.py
├── requirements.txt
├── voice_billing/        ← Django project config
│   ├── settings.py
│   └── urls.py
└── billing/              ← Main app
    ├── models.py         ← MenuItem, Table, Customer, Bill
    ├── views.py          ← All views + NLP voice parser
    ├── urls.py
    ├── admin.py
    ├── management/commands/seed_data.py
    └── templates/billing/
        ├── dashboard.html
        └── billing.html
```
>>>>>>> 89923f7 (Initial commit of voice billing project)
