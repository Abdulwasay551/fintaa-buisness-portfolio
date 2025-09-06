from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import ContactSubmission

class Command(BaseCommand):
    help = 'Simple seed command for contact submissions'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample contact submissions...')
        
        # Create some sample contact submissions
        contact_submissions = [
            {
                'name': 'John Smith',
                'email': 'john@example.com',
                'phone': '+92-300-1234567',
                'company': 'Smith Industries',
                'message': 'I need a modern e-commerce website for my business.',
                'service': 'web_development',
                'budget': '5k_15k',
                'timeline': '3_months',
                'is_responded': False
            },
            {
                'name': 'Sarah Johnson',
                'email': 'sarah@techstartup.com',
                'phone': '+92-321-9876543',
                'company': 'Tech Startup Co',
                'message': 'Looking for a React Native mobile app for our startup.',
                'service': 'mobile_app_development',
                'budget': '15k_50k',
                'timeline': '6_months',
                'is_responded': True,
                'notes': 'Called and discussed requirements. Proposal sent.'
            },
            {
                'name': 'Ahmed Ali',
                'email': 'ahmed@business.pk',
                'phone': '+92-333-5555555',
                'company': 'Business Solutions Ltd',
                'message': 'Want to integrate AI chatbot into our existing system.',
                'service': 'ai_automation',
                'budget': '50k_plus',
                'timeline': 'flexible',
                'is_responded': False
            }
        ]
        
        for submission_data in contact_submissions:
            ContactSubmission.objects.get_or_create(
                email=submission_data['email'],
                defaults=submission_data
            )
            self.stdout.write(f"Created contact submission for {submission_data['name']}")
        
        self.stdout.write(self.style.SUCCESS('Sample contact submissions created successfully!'))
