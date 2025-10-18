# Crest Product API (Django + DRF + JWT)

Implements product CRUD with soft-delete, JWT authentication, role-based access (admin/user), filtering, pagination, sorting, search, bulk create, Excel export, signals logging, and rate limiting.

## Quickstart

```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Initialize project
python manage.py migrate
python manage.py createsuperuser  # optional

# Run
python manage.py runserver
```

## API Overview

- **Auth**
  - `POST /api/auth/register/` -> {username, password, role?=user}
  - `POST /api/auth/login/` -> JWT access/refresh
- **Products** (JWT required)
  - `GET /api/products/` list (pagination, search `?search=kw`, filter `?min_price=..&max_price=..`, order `?ordering=created_on` or `-updated_on`)
  - `POST /api/products/` create (admin only)
  - `GET /api/products/{id}/` retrieve
  - `PUT/PATCH /api/products/{id}/` update (admin only)
  - `DELETE /api/products/{id}/` soft-delete (admin only; sets `is_active=false`)
  - `POST /api/products/{id}/disable/` disable (admin only; sets `is_active=false`)
  - `POST /api/products/bulk_create/` bulk create (admin only; body: list of products)
- **Export**
  - `GET /api/export/products/` -> Excel file

## Role-based Access

- Add users to **admin** group for write access. Other authenticated users have read-only access.

## Notes

- Uses `django-filter` for price range filters and `SearchFilter` for keyword search in `title` & `description`.
- Uses DRF throttling (scoped) to rate-limit endpoints.
- Signals record changes into `ProductLog`.
- `image` is a URL field for simplicity; switch to `ImageField` if media storage is needed.
- DB: SQLite for demo; adapt in `settings.py` for Postgres/MySQL in production.
"# crest_task" 
