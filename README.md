# Fintaa Business Portfolio

A modern, responsive business portfolio website built with Django and Wagtail CMS, featuring dual admin interfaces for comprehensive content management and business operations.

## 🚀 Features

### Frontend Features
- **Modern Responsive Design** - Works perfectly on all devices
- **Dynamic Content Management** - Powered by Wagtail CMS
- **Portfolio Showcase** - Display projects with detailed case studies
- **Blog/News Section** - Keep your audience updated with latest insights
- **Contact Form** - Integrated contact submission system
- **Team Pages** - Showcase your team members
- **Service Pages** - Detailed service offerings
- **SEO Optimized** - Built-in SEO best practices

### Admin Features
- **Dual Admin Interfaces**:
  - **Django Unfold Admin** - Modern business management interface
  - **Wagtail CMS Admin** - Content management system
- **Contact Management** - Track and manage contact submissions
- **User Management** - Comprehensive user and permissions system
- **Content Publishing** - Advanced page publishing and versioning
- **Analytics Dashboard** - Business insights and metrics

### Technical Features
- **Django 5.2.6** - Latest stable Django framework
- **Wagtail 7.1.1** - Advanced CMS capabilities
- **PostgreSQL Support** - Production-ready database
- **SQLite Development** - Easy local development
- **WhiteNoise** - Efficient static file serving
- **Security Features** - Production-ready security settings
- **Environment Configuration** - Flexible development/production setup

## 🛠️ Technology Stack

### Backend
- **Python 3.12+**
- **Django 5.2.6** - Web framework
- **Wagtail 7.1.1** - Content Management System
- **PostgreSQL** - Production database
- **SQLite** - Development database

### Frontend
- **HTML5/CSS3** - Modern web standards
- **JavaScript** - Interactive functionality
- **Responsive Design** - Mobile-first approach

### Admin Interfaces
- **Django Unfold 0.65.0** - Modern admin interface
- **Wagtail Admin** - Content management interface

### Deployment
- **Gunicorn** - WSGI HTTP Server
- **WhiteNoise** - Static file serving
- **Docker Support** - Containerization ready

## 📋 Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- Git
- PostgreSQL (for production)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Abdulwasay551/fintaa-buisness-portfolio.git
cd fintaa-buisness-portfolio
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
# Copy environment example
cp .env.example .env

# Edit .env file with your settings (optional for development)
# DEBUG=True is set by default for development
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# (Optional) Seed with sample data
python manage.py seed
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit:
- **Website**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
- **Wagtail CMS**: http://localhost:8000/cms/

## 👨‍💼 Admin Access

This project features **two admin interfaces** for different purposes:

### 1. Django Unfold Admin
**URL**: `http://localhost:8000/admin/`

**Purpose**: Business management and operations
- Contact submission management with advanced filtering
- User and permission management  
- System administration
- Business analytics and insights

**Features**:
- Modern dark theme interface
- Advanced filtering and search capabilities
- Bulk actions for contact submissions
- Business dashboard with metrics
- Role-based access control
- Response tracking for contact submissions
- Admin notes for internal team coordination

**Main Sections**:
- **Contact Submissions**: View and manage all website inquiries
- **Users & Groups**: Manage system users and permissions
- **Business Management**: Analytics and business insights

### 2. Wagtail CMS Admin
**URL**: `http://localhost:8000/cms/`

**Purpose**: Content management and website editing
- Page creation and editing with visual editor
- Blog post management with rich content
- Portfolio/project showcase management
- Team member profiles and company information
- Service page management

**Features**:
- Visual page editor with live preview
- Advanced page tree management
- Content versioning and publishing workflow
- Media library management
- Multi-site support
- SEO optimization tools
- Rich text editing with multimedia support

**Main Sections**:
- **Pages**: Manage all website pages and content
- **Images**: Media library for photos and graphics
- **Documents**: File management system
- **Snippets**: Reusable content blocks
- **Users**: Content editor permissions

### Admin User Setup
```bash
# Create superuser (access to both admin interfaces)
python manage.py createsuperuser

# Follow prompts to create username, email, and password
```

### Quick Test Setup
For quick testing, you can use these demo credentials:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

Create this user quickly with:
```bash
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin already exists')" | python manage.py shell
```

## 🗂️ Project Structure

```
fintaa-buisness-portfolio/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── build.sh                 # Production build script
├── .env.example            # Environment variables example
├── ENVIRONMENT_SETUP.md    # Detailed environment guide
│
├── setting/                # Django settings package
│   ├── __init__.py
│   ├── settings.py         # Main settings file
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
│
├── portfolio/              # Main application
│   ├── models.py          # Database models
│   ├── admin.py           # Django admin configuration
│   ├── views.py           # View functions
│   ├── urls.py            # App URL patterns
│   ├── admin_callbacks.py # Unfold admin customizations
│   ├── templatetags/      # Custom template tags
│   ├── management/        # Management commands
│   │   └── commands/
│   │       ├── seed.py    # Database seeding
│   │       └── simple_seed.py
│   ├── migrations/        # Database migrations
│   └── templates/         # HTML templates
│
├── static/                # Static files (CSS, JS, images)
├── staticfiles/          # Collected static files
└── media/                # User uploaded files
```

## 🗃️ Database Models

### Content Models
- **HomePage** - Main homepage content
- **AboutPage** - About us page
- **ContactPage** - Contact information
- **ServicePage** - Individual service pages
- **ProjectPage** - Portfolio projects
- **BlogPage** - Blog posts
- **TeamPage** - Team member listings

### Business Models
- **ContactSubmission** - Contact form submissions
- **ServiceItem** - Homepage services
- **TeamMember** - Team member details
- **CompanyValue** - Company values display

## 🌐 Environment Configuration

### Development (Default)
- **DEBUG**: `True`
- **Database**: SQLite
- **Static Files**: Served by Django
- **Security**: Relaxed for development

### Production
- **DEBUG**: `False`
- **Database**: PostgreSQL (via DATABASE_URL)
- **Static Files**: WhiteNoise with compression
- **Security**: Full security headers enabled

### Environment Variables
```bash
# Required for production
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Optional
WAGTAILADMIN_BASE_URL=https://yourdomain.com
```

## 📦 Management Commands

### Database Seeding
```bash
# Full seed with sample content
python manage.py seed

# Simple contact submissions only
python manage.py simple_seed

# Clean existing data before seeding
python manage.py seed --clean
```

### Testing Environment
```bash
# Test environment configuration
python test_env.py
```

## 🚢 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic`
- [ ] Create superuser
- [ ] Set up HTTPS/SSL

### Quick Deploy Commands
```bash
# Production setup
export DEBUG=False
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host:port/db
export ALLOWED_HOSTS=yourdomain.com

# Deploy
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
gunicorn setting.wsgi:application
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📞 Contact Management

The system includes a comprehensive contact management feature:

### Contact Submission Features
- **Form Fields**: Name, email, phone, company, service type, budget, timeline, message
- **Admin Interface**: View, filter, and manage submissions
- **Response Tracking**: Mark submissions as responded/pending
- **Admin Notes**: Internal notes for team coordination
- **Email Integration**: Contact details for follow-up

### Accessing Contact Submissions
1. Login to Django admin: `http://localhost:8000/admin/`
2. Navigate to "Contact Submissions"
3. Use filters to find specific submissions
4. Mark as responded when contacted
5. Add internal notes for team coordination

## 🔧 Customization

### Adding New Pages
1. Define model in `portfolio/models.py`
2. Create template in `portfolio/templates/`
3. Add to Wagtail admin panels
4. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Modifying Admin Interface
- **Django Admin**: Edit `portfolio/admin.py`
- **Unfold Customization**: Edit `portfolio/admin_callbacks.py`
- **Wagtail Admin**: Configure in model `content_panels`

## 🚨 Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database connection errors**
   - Check DATABASE_URL format
   - Ensure PostgreSQL is running
   - Verify credentials

3. **Permission errors**
   - Check user permissions
   - Create superuser if needed
   - Verify file permissions

4. **Environment variables not loading**
   - Check .env file location
   - Verify variable names
   - Restart development server

## 📖 Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Wagtail Documentation**: https://docs.wagtail.org/
- **Django Unfold**: https://github.com/unfoldadmin/django-unfold
- **Environment Setup Guide**: See `ENVIRONMENT_SETUP.md`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For support and questions:
- **Email**: info@Fintaa.pk
- **Documentation**: Check `ENVIRONMENT_SETUP.md`
- **Issues**: Create a GitHub issue

---

**Fintaa Software House** - Transforming Ideas into Digital Reality
