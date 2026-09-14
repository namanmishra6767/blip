# BLIP

BLIP is a Django-powered microblogging platform inspired by Twitter/X. Users can create short posts, upload images, and manage their own posts through a dark, responsive interface.

## Features

- User registration and login
- Case-insensitive duplicate email protection
- Create posts with up to 250 characters
- Optional image uploads
- Live character counter
- Edit and delete controls for post owners
- Responsive three-column layout
- Environment-based security configuration

## Tech stack

- Python
- Django
- SQLite for local development
- Tailwind CSS

## Local setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Python dependencies

Install the packages used by the project:

```powershell
pip install django pillow django-tailwind
```

### 3. Configure environment variables

Copy `.env.example` to `.env` or set the variables in your shell. Django does not load `.env` automatically, so shell variables or a deployment secret manager must provide them.

For local development:

```powershell
$env:DJANGO_SECRET_KEY = "generate-a-long-random-secret"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
```

For production, use a strong secret, set `DJANGO_DEBUG=False`, and provide the real host names in `DJANGO_ALLOWED_HOSTS`.

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Start the development server

```powershell
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Tailwind development

Install the frontend dependencies from the theme directory:

```powershell
Set-Location theme\static_src
npm install
```

Run the Tailwind watcher during development:

```powershell
npm run dev
```

Build the stylesheet for production:

```powershell
npm run build
```

## Security

- Never commit `.env` files or real secret keys.
- Keep `DEBUG=False` outside local development.
- Configure `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` for the deployment domain.
- Production settings enable HTTPS redirects, secure cookies, HSTS, clickjacking protection, and MIME-sniffing protection.
- Run the deployment check before releasing:

```powershell
python manage.py check --deploy
```

## Project structure

```text
blip/
├── blip/          # Django project settings and URL configuration
├── posts/         # Posts app, views, forms, migrations, and templates
├── templates/     # Shared site layout
├── static/        # Project-wide static assets
├── media/         # User-uploaded media during local development
└── theme/         # Tailwind and PostCSS setup
```

## Current roadmap

Notifications, messages, profiles, likes, comments, reposts, and search are planned features and currently appear as placeholders in the interface.
