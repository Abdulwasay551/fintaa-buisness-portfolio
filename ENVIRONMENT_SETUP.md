# Environment Configuration Guide

## Overview
Your Django application is now configured to automatically switch between development and production settings based on environment variables.

## Environment Variables

### Required for Production

1. **DEBUG** - Set to `False` for production
   ```
   DEBUG=False
   ```

2. **SECRET_KEY** - Generate a new secret key for production
   ```
   SECRET_KEY=your-super-secret-production-key-here
   ```

3. **DATABASE_URL** - PostgreSQL connection string for production
   ```
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```

4. **ALLOWED_HOSTS** - Domains allowed to serve your application
   ```
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

### Optional

5. **WAGTAILADMIN_BASE_URL** - Full URL for Wagtail admin
   ```
   WAGTAILADMIN_BASE_URL=https://yourdomain.com
   ```

## Development vs Production

### Development (DEBUG=True)
- Uses SQLite database
- Static files served by Django
- Debug toolbar and detailed error pages
- Less secure settings for easier development

### Production (DEBUG=False)
- Requires PostgreSQL database via DATABASE_URL
- Static files handled by WhiteNoise with compression
- Secure cookies and SSL redirects
- HSTS security headers
- Compressed static file storage

## Setting Environment Variables

### Method 1: Create .env file
1. Copy `.env.example` to `.env`
2. Edit `.env` with your values:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:pass@host:port/db
   ALLOWED_HOSTS=yourdomain.com
   ```

### Method 2: Set in your hosting platform
Most hosting platforms (Render, Heroku, Railway, etc.) allow you to set environment variables in their dashboard.

### Method 3: Set in your shell (temporary)
```bash
export DEBUG=False
export SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://user:pass@host:port/db
```

## Testing Your Configuration

Run the environment test:
```bash
python test_env.py
```

This will show:
- Current environment variable values
- Which settings are active
- Production readiness checklist

## Database Setup for Production

1. Create a PostgreSQL database
2. Set the DATABASE_URL environment variable
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Security Checklist for Production

When DEBUG=False, these security features are automatically enabled:
- ✅ SSL redirects (`SECURE_SSL_REDIRECT = True`)
- ✅ Secure cookies (`SESSION_COOKIE_SECURE = True`)
- ✅ CSRF cookies over HTTPS (`CSRF_COOKIE_SECURE = True`)
- ✅ HSTS headers for 1 year
- ✅ XSS and content type sniffing protection
- ✅ Compressed static files with long-term caching

## Static Files in Production

Your application uses WhiteNoise to serve static files efficiently:
- Static files are automatically compressed
- Files get unique names for cache busting
- CDN-ready with proper headers

## Common Issues

1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Database connection errors**: Check your DATABASE_URL format
3. **ALLOWED_HOSTS error**: Add your domain to ALLOWED_HOSTS
4. **SSL errors**: Ensure your hosting platform provides HTTPS

## Example Production Commands

```bash
# Set production environment
export DEBUG=False
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host:port/db
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Deploy steps
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed  # Optional: populate with sample data
python manage.py runserver  # or use gunicorn for production
```

## Monitoring and Logging

In production mode, logging is configured to:
- Log INFO level and above to console
- Include detailed formatting with timestamps
- Separate logs for Django and Wagtail components

Your application is now production-ready! 🚀
