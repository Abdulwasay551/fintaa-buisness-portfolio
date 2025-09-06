"""
Admin callbacks for Unfold admin interface
"""
from django.utils.translation import gettext_lazy as _


def dashboard_callback(request, context):
    """Dashboard callback for Unfold admin"""
    from portfolio.models import ContactSubmission
    
    # Get recent contact submissions
    recent_contacts = ContactSubmission.objects.filter(is_responded=False)[:5]
    total_contacts = ContactSubmission.objects.count()
    unresponded_contacts = ContactSubmission.objects.filter(is_responded=False).count()
    
    context.update({
        "recent_contacts": recent_contacts,
        "total_contacts": total_contacts,
        "unresponded_contacts": unresponded_contacts,
        "dashboard_title": "Fintaa Software House Dashboard",
    })
    return context


def environment_callback(request):
    """Environment callback for Unfold admin"""
    return ["Development", "info"]


def contact_badge_callback(request):
    """Badge callback for contact submissions"""
    from portfolio.models import ContactSubmission
    return ContactSubmission.objects.filter(is_responded=False).count()


def permission_callback(request):
    """Permission callback for admin access"""
    return request.user.is_staff
