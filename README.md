# HR Service API

## Introduction
The **HR Service API** is a Django-based backend application that provides RESTful endpoints for managing HR-related data.  
It integrates with an external **Auth Service** for authentication, uses **DRF Spectacular** for API documentation, and supports powerful filtering and field selection.  

Main components:
- **`hr_master` app**: Handles HR database models.
- **Custom middleware**: Validates tokens with Auth Service.
- **Database router**: Routes requests to the HR-specific database.

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## Installation
```bash
git clone <repository_url>
cd <project_directory>
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment variables
Create a `local_settings.py` file in the `hr` directory:
```python
DEBUG_ = True
AUTH_SERVICE = "http://auth-service-url"
DATABASE_SERVICE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hr_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Run migrations
```bash
python manage.py migrate
```

---

## Usage
- Start the server:
```bash
python manage.py runserver
```
- Admin Panel:  
  ```
  http://127.0.0.1:8000/admin/
  ```
- API Root:  
  ```
  http://127.0.0.1:8000/api/hr/
  ```

---

## Features
- Token-based authentication via external Auth Service.
- Detailed filtering, searching, and ordering.
- Ability to select (`fields`) or exclude (`exclude`) specific fields.
- Pagination with total pages and current page.
- Auto-generated API schema & ReDoc docs.

---

## Dependencies
- Python 3.x
- Django 5.2.5
- Django REST Framework
- drf-spectacular
- drf-spectacular-sidecar
- django-filter

---

## Configuration
- `DJANGO_SETTINGS_MODULE` → Defaults to `hr.settings`.
- Middleware:
  - `VerifyAuthTokenMiddleware`: Validates token via Auth Service.
  - `AuthServiceLogoutMiddleware`: Handles logout requests.

---

## API Endpoints

### **Master Data**

#### 1. Company
`GET /api/hr/master/company/` — List companies  
**Query Parameters:**
- `name`, `code`, `is_active`, `parent_name`, `children_name`, `max_depth`, `fields`, `exclude`, `parent_isnull`  
**Example Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 2,
      "name": "Mazta Distribusi Indonesia",
      "code": "MDI",
      "is_active": true
    }
  ]
}
```

#### 2. Unit
`GET /api/hr/master/unit/` — List units  
Params similar to Company.

#### 3. Level
`GET /api/hr/master/level/` — List job levels  
Params similar to Unit.

#### 4. Employment Type
`GET /api/hr/master/employment-type/` — List employment types  
**Params:** `name`, `code`, `is_active`, `fields`, `exclude`

#### 5. Shift
`GET /api/hr/master/shift/` — List shifts  
**Params:** `name`, `code`, `start_day`, `end_day`, `is_active`, `fields`, `exclude`

#### 6. Branch
`GET /api/hr/master/branch/` — List branches  
**Params:** `name`, `code`, `company_name`, `city`, `province`, `company_id`, `fields`, `exclude`

#### 7. Employee
`GET /api/hr/master/employee/` — List employees  
**Params:**  
Search: `full_name`, `province`, `city`, `religion`, `marital_status`, `birthplace`, `code`, `nik`, `unit_name`, `level_name`, etc.  
Exact match: `company_id`, `branch_id`, `unit_id`, `level_id`, `employment_type_id`, `shift_id`, `user_id`  
Boolean: `parent_isnull`

---

## API Documentation
- **Schema (OpenAPI 3)**:  
  ```
  http://127.0.0.1:8000/api/schema/
  ```
- **ReDoc UI**:  
  ```
  http://127.0.0.1:8000/api/docs/
  ```

---

## Troubleshooting
- **Error: Couldn't import Django**  
  Ensure your virtual environment is active and dependencies are installed.
- **Auth Token errors**  
  Check that `AUTH_SERVICE` URL in `local_settings.py` is correct and reachable.