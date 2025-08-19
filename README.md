# HR Service

A Django-based **HR (Human Resources) Service** that manages employee-related data and connects to multiple HR databases. This service integrates with external **Auth Service** and **Finance Service** for authentication, authorization, and extended functionality. APIs are secured with token-based authentication and documented with **drf-spectacular**.

---

## 📑 Table of Contents

1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Architecture](#architecture)  
4. [Installation](#installation)  
5. [Configuration](#configuration)  
6. [Usage](#usage)  
7. [API Documentation](#api-documentation)  
8. [Database](#database)  
9. [Troubleshooting](#troubleshooting)  
10. [Contributors](#contributors)  
11. [License](#license)  

---

## 📖 Introduction

The **HR Service** is a backend microservice that provides structured APIs for managing HR-related data such as employee records, master data, and historical HR dumps. It integrates with:

- **Auth Service** → for authentication and token verification.  
- **Finance Service** → for connecting HR and financial data when needed.  

This service supports **multiple database routing**, ensuring HR master and dump data are stored and accessed separately.

---

## ✨ Features

- Built with **Django 5.2.5** and **Django REST Framework**.  
- **Multiple database support** with custom routers (`hr_master`, `hr_dump`).  
- Token-based authentication validated against an **external Auth Service**.  
- Integration with **Finance Service** for cross-service data sharing.  
- Custom middleware for authentication (`VerifyAuthTokenMiddleware`, `AuthServiceLogoutMiddleware`).  
- Auto-generated **OpenAPI 3.0 schema** via `drf-spectacular`.  
- Secure password validation rules enabled.  
- Configurable settings via `local_settings.py`.  

---

## 🏛 Architecture

- **Framework:** Django (WSGI application).  
- **API Layer:** Django REST Framework (DRF).  
- **Documentation:** drf-spectacular + drf-spectacular-sidecar.  
- **Authentication:** Delegated to external Auth Service.  
- **Databases:**  
  - `default` → Auth database (users & auth tokens).  
  - `hr_master` → Main HR database (core employee data).  
  - `hr_dump` → Archived HR database (historical/dump data).  
- **Middleware:**  
  - `VerifyAuthTokenMiddleware` – validates tokens with Auth Service.  
  - `AuthServiceLogoutMiddleware` – syncs logout events with Auth Service.  

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/hr-service.git
cd hr-service
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux / Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Run the development server
```bash
python manage.py runserver
```

---

## 🔧 Configuration

Settings are split across two files:

- **`settings.py`** – Core project settings.  
- **`local_settings.py`** – Environment-specific overrides.  

### Example `local_settings.py`
```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_SERVICE = 'http://localhost:8000'
FIN_SERVICE = 'http://localhost:8002'

DATABASE_SERVICE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'databases/auth.sqlite3',
    },
    'hr_master': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'databases/hr_master.sqlite3',
    },
    'hr_dump': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'databases/hr_dump.sqlite3',
    }
}

DEBUG_ = True
```

### Key Configurable Options

| Setting        | Description                                        | Default                  |
|----------------|----------------------------------------------------|--------------------------|
| `AUTH_SERVICE` | URL of external authentication service             | `http://localhost:8000` |
| `FIN_SERVICE`  | URL of external finance service                    | `http://localhost:8002` |
| `DATABASES`    | Supports multiple databases (`default`, `hr_*`)    | SQLite local DBs         |
| `DEBUG_`       | Toggle for debug mode                              | `True`                   |
| `TIME_ZONE`    | Application timezone                               | `Asia/Jakarta`           |

---

## 🚀 Usage

### Authentication

All requests must include a **token from the Auth Service**:

```http
Authorization: Token <your_token>
```

Custom middlewares validate tokens before granting access.

### Database Access

Queries are automatically routed to the correct HR database:  

- `hr_master` → for primary HR data.  
- `hr_dump` → for historical/dump HR data.  

---

## 📜 API Documentation

The project uses **drf-spectacular** for schema generation.

- OpenAPI schema available at:  
  ```
  /api/schema/
  ```
- Swagger UI (if enabled):  
  ```
  /api/docs/
  ```

---

## 🗄 Database

This service supports **multiple databases** using Django routers:

- `default` → Authentication database.  
- `hr_master` → Main HR database.  
- `hr_dump` → Archived HR database.  

You can easily switch to PostgreSQL, MySQL, or other backends by updating `local_settings.py`.

---

## 🛠 Troubleshooting

- **Token Rejected:** Ensure Auth Service is running and issuing valid tokens.  
- **Finance Integration Issues:** Confirm that `FIN_SERVICE` URL is correct.  
- **Migrations Fail:** Verify SQLite database paths or credentials for other DBs.  
- **API Docs Not Found:** Check that `drf-spectacular` is in `INSTALLED_APPS`.  

---

## 👥 Contributors

- **Your Name** – Initial Work & Maintenance  
- Contributions welcome via Pull Requests.  

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
