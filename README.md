# Home Service Management System 

A comprehensive Django-based backend for a Home Service Management System, featuring user authentication, service management, booking lifecycle control, activity logging, analytics, and automated cron jobs.

## 🚀 Features

- **User Authentication**: JWT-based auth with custom login/register logic and profile management.
- **Service Management**: CRUD operations for services with slug auto-generation and provider assignment.
- **Booking System**: Full lifecycle management (Pending -> Confirmed -> In Progress -> Completed/Cancelled).
- **Custom Admin Interface**: Enhanced UI using **Django Jazzmin** with custom icons and dark mode.
- **Activity Logs**: Automatic audit trail for all critical actions (Logins, Bookings, Service updates).
- **Analytics Dashboard**: Real-time metrics for revenue, booking status, and provider performance.
- **Automated Cron Jobs**: Standalone scripts for daily aggregation, availability sync, and reminders.
- **Standardized API**: Custom JSON renderer for consistent response structures.

## 🛠️ Tech Stack

- **Framework**: Django 5.2.9
- **API**: Django REST Framework (DRF)
- **Auth**: SimpleJWT
- **Database**: PostgreSQL (configured) / SQLite (default)
- **Admin UI**: Django Jazzmin
- **Task Scheduling**: System Cron (Crontab)

## 📋 Prerequisites

- Python 3.10+
- `pip` and `virtualenv`

## ⚙️ Setup Instructions

### 1. Clone and Navigate
```bash
cd /home/chirag/Documents/FInal_Assessment/final_assessment
```

### 2. Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the project root (use `.env.example` as a template):
```env
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

---

## ⏰ Cron Jobs Setup

The project includes automated tasks located in the `crons/` folder. To schedule them:

1. Run `crontab -e`
2. Add the entries from `CRONTAB_INSTRUCTIONS.md`
3. Logs will be generated in the `logs/` directory.

---

## 📖 API Documentation

Detailed documentation for all endpoints (Request/Response bodies) can be found in:
👉 **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)**

### Key Endpoints:
- **Auth**: `/api/auth/login/`, `/api/auth/register/`
- **Services**: `/api/services/`, `/api/services/search/`
- **Bookings**: `/api/bookings/`, `/api/bookings/{id}/status/`
- **Analytics**: `/api/analytics/dashboard/`
- **Logs**: `/api/logs/`

---

## 📂 Project Structure

```text
├── apps/
│   ├── activity_logs/   # Audit trail logic
│   ├── analytics/       # Metrics and reporting
│   ├── authentication/  # User & Profile management
│   ├── bookings/        # Booking lifecycle
│   ├── core/            # Custom renderers & global utils
│   └── services/        # Service & Provider management
├── config/              # Project settings & URLs
├── crons/               # Standalone cron scripts
├── logs/                # Cron job output logs
└── manage.py
```

## 🛡️ Admin Panel
Access the premium admin dashboard at `http://127.0.0.1:8000/admin/` using your superuser credentials.
