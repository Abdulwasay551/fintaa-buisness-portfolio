from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ContactSubmission


def contact_form_view(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone', '')
            company = request.POST.get('company', '')
            service = request.POST.get('service')
            budget = request.POST.get('budget', '')
            timeline = request.POST.get('timeline', '')
            message_text = request.POST.get('message')
            
            # Create contact submission
            contact = ContactSubmission.objects.create(
                name=name,
                email=email,
                phone=phone,
                company=company,
                service=service,
                budget=budget,
                timeline=timeline,
                message=message_text
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you within 24 hours.')
            
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again.')
        
        # Redirect back to the page they came from or to home
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('/')
