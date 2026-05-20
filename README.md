# Community Marketplace

An order-based marketplace application built with **Django** featuring authentication, user profiles, and complete CRUD functionality.

The project is containerized with Docker to provide reproducible builds and a consistent development environment.

---

# ✨ Features

- Django 5.2 backend
- User authentication system
- User profile management
- Complete CRUD operations
- Order-based listing system
- Modular Django app structure
- Template-based frontend
- Static asset management
- Dockerized development setup
- Pillow support for image handling

---

# 🧠 Technical Overview

The project is built using Django's standard MVT architecture and focuses on creating a structured and maintainable marketplace application.

The implementation includes:

- Django authentication system
- Dynamic template rendering
- Modular app organization
- CRUD-based listing management
- Media and image handling with Pillow
- Docker containerization
- Static and template asset separation

The application is intended primarily for development and learning purposes.

---

# 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3.13 | Core programming language |
| Django 5.2 | Backend framework |
| Docker | Containerization |
| Pillow | Image processing |
| HTML/CSS/JavaScript | Frontend templates and assets |

---

# 📁 Project Structure

```bash
.
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── manage.py
├── project/          # Django project settings
├── db/               # Main Django app
├── templates/        # HTML templates
├── static/           # CSS, JS, images
└── README.md
```

---

# 🚀 Local Development (Without Docker)

Use this only if you want to run the project directly on your machine.

## 1. Create and Activate a Virtual Environment

```bash
python -m venv market
market\Scripts\activate.bat
```

---

## 2. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 3. Run Database Migrations

```bash
python manage.py migrate
```

---

## 4. Start the Development Server

```bash
python manage.py runserver
```

Open:

```txt
http://localhost:8000
```

---

# 🐳 Run with Docker (Recommended)

Docker provides a more reproducible and isolated development environment.

## 1. Build the Docker Image

```bash
docker build -t community-marketplace .
```

---

## 2. Run the Container

```bash
docker run -p 8000:8000 community-marketplace
```

Then visit:

```txt
http://localhost:8000
```

---

# ⚙️ Django Settings Notes

For Docker-based development, ensure `settings.py` contains:

```python
ALLOWED_HOSTS = ["*"]
```

This allows Django to accept external requests coming from the Docker container environment.

---

# 📌 Development Status

Current setup uses Django’s built-in development server:

```bash
runserver
```

The project is intended mainly for development and learning purposes and is not production-hardened.

For production deployment, additional improvements would typically include:

- Gunicorn or another WSGI server
- Environment-based configuration (`.env`)
- PostgreSQL or another production database
- Reverse proxy setup (Nginx/Caddy)
- Static/media file serving strategy

---

# 👨‍💻 Author

### Herry Patel

---

# 🔒 License

This project is closed-source and proprietary.

Unauthorized copying, modification, distribution, or reuse of the source code is prohibited.

All rights reserved © Herry Patel.
