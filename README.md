# Highly Scalable Blog API (Django & DRF)

A robust, production-ready Blog API built with Django and Django REST Framework. This project is engineered with a strong focus on **scalability, performance, and security**, solving common bottlenecks found in standard MVC applications.

## 🚀 Engineering Highlights & Scalability Features

### 1. Zero N+1 Query Bottlenecks
Instead of relying on Django's default lazy-loading (which results in `2N+1` database queries for nested serializers), this application utilizes `select_related()` and `prefetch_related()` across all list endpoints. 
- **Result:** Fetching 100 blogs with their associated users and profiles takes exactly **1 SQL query** instead of 201.

### 2. Memory-Safe Pagination
Returning thousands of database rows at once can cause severe memory exhaustion (OOM) and massive network payloads. 
- **Solution:** Implemented global `PageNumberPagination` via Django REST Framework, ensuring the API streams data in highly efficient, bounded chunks.

### 3. Transaction Safety (ACID Compliance)
The user registration endpoint involves multi-table database writes (creating a `User`, then a `Profile`). 
- **Solution:** Wrapped in a `transaction.atomic()` block. If the `Profile` fails to create (e.g., due to a database timeout), the `User` creation is rolled back. This strictly prevents corrupted states and orphaned records.

### 4. Advanced API Caching
Instead of brittle, manual caching that leaks memory and risks exposing user-specific data to other sessions, this architecture implements:
- **Full-Page Caching:** High-traffic, read-only endpoints (like `/all-blogs/`) use Django's `@cache_page(300)` to intercept requests before they hit the database, returning pre-calculated responses instantly.
- **Dynamic Dashboards:** Authenticated user endpoints skip the cache to guarantee real-time, zero-leak data delivery, relying entirely on the optimized SQL queries for speed.

### 5. Secure Environment Configuration
- Hardcoded secrets were stripped from the codebase.
- Utilizes `python-dotenv` for local development, dynamically loading `SECRET_KEY` and `DEBUG` variables from an ignored `.env` file to prevent credential leakage on GitHub.

### 6. Data Normalization & DRY Principles
- Removed redundant, duplicated fields (like storing a user's full name in both the `User` and `Profile` tables).
- Utilized dynamic `@property` methods in models to evaluate data on the fly, ensuring a single source of truth and preventing synchronization bugs.

## 🛠️ Tech Stack
- **Backend:** Python, Django, Django REST Framework (DRF)
- **Database:** SQLite (Configured for easy swap to PostgreSQL)
- **Authentication:** JWT (JSON Web Tokens) via `rest_framework_simplejwt`
- **Security:** `python-dotenv`

## 📦 Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/adarsh-pathak-2006/Really_scalable_Blog_App.git
   cd Really_scalable_Blog_App/config
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you install `python-dotenv` and `djangorestframework-simplejwt`)*

3. Environment Variables:
   Copy `.envexample` to `.env` and fill in your secrets:
   ```bash
   cp .envexample .env
   ```

4. Run Migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the Server:
   ```bash
   python manage.py runserver
   ```
