# 🗣️ Learning App Backend

A robust Django REST framework backend for the Devora Learning App, featuring speech evaluation insights and automated API documentation.

## 🚀 Key Features

- **Speech Evaluation API**: Compare recognized text against target words with logic for correctness.
- **RESTful Architecture**: Clean API structure powered by Django REST Framework.
- **Automated Documentation**: OpenAPI 3.0 schema generation with Swagger UI.
- **Production Ready**: Configured for seamless deployment on Render with Whitenoise for static files.

## 🛠️ Technology Stack

- **Framework**: [Django 5](https://www.djangoproject.com/)
- **GEMINI API**:[Google Studio]()
- **API**: [Django REST Framework](https://www.django-rest-framework.org/)
- **Documentation**: [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- **Database**: PostgreSQL (Production) / SQLite (Local)
- **Server**: Gunicorn

## 💻 Local Development

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd devora-test-be
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the `backend/` directory:
   ```env
   DEBUG=True
   SECRET_KEY=your-local-secret-key
   ALLOWED_HOSTS=*
   GEMINI_API_KEY
   ```

5. **Run Migrations**:
   ```bash
   python backend/manage.py migrate
   ```

6. **Start the server**:
   ```bash
   python backend/manage.py runserver
   ```

## 🌐 API Documentation

Once the server is running, you can access the documentation at:
- **Swagger UI**: `http://127.0.0.1:8000/docs/`
- **Schema (YAML)**: `http://127.0.0.1:8000/schema/`

## 🌍 Deployment on Render

### 1. Build & Start Commands
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn --pythonpath backend backend.wsgi:application`

### 2. Environment Variables
Ensure the following are set in the Render dashboard:
- `PYTHON_VERSION`: `3.11` (or your preferred version)
- `SECRET_KEY`: A secure random string
- `GEMINI_KEY`: Gemini API
- `DEBUG`: `False`
- `DATABASE_URL`: Your PostgreSQL connection string (Render provides this if using their managed DB)
- `ALLOWED_HOSTS`: `your-app-name.onrender.com`

---
*Built with ❤️ for better speech learning.*
