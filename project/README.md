# Django DRF Project with Telegram Bot Integration

A production-ready Django REST Framework project featuring JWT authentication, Telegram bot integration, and modern web design.

## 🚀 Features

- **Django REST Framework**: Modern API development with DRF
- **JWT Authentication**: Secure token-based authentication using SimpleJWT
- **Telegram Bot Integration**: Full-featured bot connected to Django backend
- **Production Ready**: Configured for deployment with security best practices
- **Environment Configuration**: All secrets managed via environment variables
- **CORS Support**: Properly configured for frontend integration
- **Modern UI**: Beautiful, responsive web templates

## 📋 Requirements

- Python 3.8+
- PostgreSQL (recommended) or SQLite for development
- Telegram Bot Token (from @BotFather)

## 🛠️ Installation

### 1. Clone and Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

Required environment variables:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create logs directory
mkdir logs
```

### 4. Static Files

```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

## 🚀 Running the Application

### Development Server

```bash
# Start Django development server
python manage.py runserver

# In another terminal, start Telegram bot
python manage.py run_telegram_bot
```

### Production Deployment

```bash
# Using Gunicorn
gunicorn django_project.wsgi:application --bind 0.0.0.0:8000

# Start Telegram bot in production
python manage.py run_telegram_bot
```

## 📡 API Endpoints

### Public Endpoints (No Authentication)

- `GET /api/public/` - Public API message
- `POST /auth/login/` - User login (returns JWT tokens)
- `POST /auth/register/` - User registration

### Secure Endpoints (JWT Required)

- `GET /api/secure/` - User-specific data
- `GET/PUT /api/profile/` - User profile management
- `GET/POST /api/posts/` - User posts list/create
- `GET/PUT/DELETE /api/posts/{id}/` - Individual post operations

### Authentication Headers

```bash
Authorization: Bearer <your_jwt_access_token>
```

## 🤖 Telegram Bot Commands

- `/start` - Welcome message and bot introduction
- `/help` - Help information and available commands
- `/stats` - Get platform statistics from Django backend
- `/profile <username>` - Link Telegram account to Django user
- `/posts` - Get latest posts from the platform

## 📝 API Usage Examples

### Login and Get Token

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Access Secure Endpoint

```bash
curl -X GET http://localhost:8000/api/secure/ \
  -H "Authorization: Bearer your_jwt_access_token"
```

### Create a Post

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer your_jwt_access_token" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Post content here", "is_published": true}'
```

## 🔧 Configuration

### Database Configuration

The project supports both PostgreSQL and SQLite:

```python
# PostgreSQL (recommended for production)
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# SQLite (development only)
DATABASE_URL=sqlite:///db.sqlite3
```

### CORS Configuration

Configure allowed origins in your `.env` file:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Security Settings

Production security settings are automatically enabled when `DEBUG=False`:

- HTTPS redirect
- Secure cookies
- HSTS headers
- XSS protection
- Content type sniffing protection

## 📁 Project Structure

```
django_project/
├── django_project/          # Main project settings
├── api/                     # API app with models and views
├── authentication/          # Authentication endpoints
├── telegram_bot/           # Telegram bot integration
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── logs/                   # Application logs
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚀 Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Using Railway/Heroku

1. Set environment variables in your platform dashboard
2. Add `Procfile`:
```
web: gunicorn django_project.wsgi:application --port $PORT
bot: python manage.py run_telegram_bot
```

### Using DigitalOcean/AWS

1. Set up PostgreSQL database
2. Configure environment variables
3. Use systemd services for bot management
4. Set up Nginx reverse proxy

## 🔍 Monitoring and Logging

Logs are configured to write to both console and file:

- Application logs: `logs/django.log`
- Error tracking: Built-in Django logging
- Telegram bot logs: Console output with timestamps

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the documentation above
2. Review the code comments
3. Check Django and DRF documentation
4. Open an issue on GitHub

## 🔄 Updates and Maintenance

- Keep dependencies updated: `pip list --outdated`
- Monitor security advisories
- Regular database backups
- Monitor bot performance and logs

---

**Built with ❤️ using Django, DRF, and Python-Telegram-Bot**