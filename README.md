# Real State Project

A Django-based real estate listings application featuring listings, realtors, user accounts, contact forms, and static/media handling. The project includes Docker support for local development and a simple REST API (DRF installed).

## Table of Contents
- Project Overview
- Features
- Tech Stack
- Project Structure
- Prerequisites
- Local Development (without Docker)
- Development with Docker
- Environment Variables
- Database & Migrations
- Running Tests
- Media & Static Files
- Contribution
- License

## Project Overview
This repository is a Django web application for managing real estate listings, realtors, and leads. It provides HTML templates for public listings, admin site integration, and a small API surface via Django REST Framework.

## Features
- Listings management with photos and main image
- Realtor profiles
- Contact form for leads
- User accounts and authentication
- Pages (static content) and templates
- REST API endpoints via DRF
- Docker-based development environment

## Tech Stack
- Python + Django (project generated with Django 5.x)
- PostgreSQL (used in Docker setup)
- Docker & docker-compose
- Django REST Framework

## Project Structure (high-level)
- `realState/` - Django project settings and WSGI/ASGI
- `accounts/` - user auth and account views
- `pages/` - static site pages
- `listings/` - listing models, serializers, views
- `realtors/` - realtor model and related code
- `contacts/` - contact/lead handling
- `templates/` - HTML templates
- `static/`, `media/` - static assets and uploaded media

## Prerequisites
- Python 3.10+ (create a virtualenv)
- pip
- Docker & docker-compose (optional but recommended for local dev)

## Local Development (without Docker)
1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables (example):

- `DB_HOST` - database host
- `DB_NAME` - database name
- `DB_USER` - database user
- `DB_PASS` - database password
- `SECRET_KEY` - Django secret key (optional for local)
- `DEBUG` - `True` or `False` (optional)

You can export these in your shell or use a `.env` loader in development.

4. Run migrations and start the development server:

```bash
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

## Development with Docker
This repository includes a `docker-compose.yml` that defines an `app` service (Django) and a `db` service (Postgres). To run the app with Docker:

```bash
# build and start containers
docker-compose up --build

# stop and remove containers
docker-compose down
```

The compose file mounts the project into the container and maps port `8000` by default. The app service waits for the DB, runs migrations, and starts the Django dev server.

## Environment Variables
The Django settings use environment variables for database configuration. The following are referenced in `realState/settings.py`:

- `DB_HOST` (e.g. `db` when using docker-compose)
- `DB_NAME`
- `DB_USER`
- `DB_PASS`

Additionally, set `SECRET_KEY` and `DEBUG` as needed for your environment. In the included `docker-compose.yml`, example values are provided for the development database (`devdb`, `devuser`, `root`).

## Database & Migrations
- Apply migrations:

```bash
python manage.py migrate
```

- Create a superuser:

```bash
python manage.py createsuperuser
```

- There is a small helper command `wait_for_db` under `core/management/commands` used in the Docker entrypoint to wait until the Postgres container is ready.

## Running Tests
Run Django tests with:

```bash
python manage.py test
```

## Media & Static Files
- `STATICFILES_DIRS` includes `realState/static` for development assets.
- `MEDIA_URL` is set to `/media/` and `MEDIA_ROOT` is set to `/vol/web/media` in settings (configured for Docker volume usage). Ensure your production deployment stores and serves media files appropriately.

## Contribution
Contributions are welcome. Suggested workflow:
- Fork the repository
- Create a feature branch
- Open a pull request with a clear description

Before opening a PR, ensure:
- Tests pass: `python manage.py test`
- Static assets and migrations are included if relevant

## License
This project includes a `LICENSE` file in the repository root. Check that file for license details.

---


