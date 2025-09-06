from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = [
        'name', 
        'email', 
        'service_display', 
        'created_at', 
        'response_status'
    ]
    list_filter = ['service', 'is_responded', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'service'),
            'classes': ('wide',),
        }),
        ('Message Details', {
            'fields': ('message',),
            'classes': ('wide',),
        }),
        ('Response Status', {
            'fields': ('is_responded', 'created_at'),
            'classes': ('wide',),
        }),
    )
    
    def service_display(self, obj):
        """Display service with nice formatting"""
        service_icons = {
            'web_development': '🌐',
            'mobile_app_development': '📱',
            'ai_automation': '🤖',
            'cybersecurity': '🔐',
            'digital_marketing': '📈',
            'call_center_services': '📞',
        }
        icon = service_icons.get(obj.service, '💼')
        service_name = obj.get_service_display()
        return format_html(
            '<span style="font-size: 14px;">{} {}</span>',
            icon,
            service_name
        )
    service_display.short_description = 'Service'
    
    def response_status(self, obj):
        """Display response status with colors"""
        if obj.is_responded:
            return format_html(
                '<span style="color: #10b981; font-weight: bold;">✓ Responded</span>'
            )
        else:
            return format_html(
                '<span style="color: #ef4444; font-weight: bold;">⏳ Pending</span>'
            )
    response_status.short_description = 'Status'
    
    actions = ['mark_as_responded', 'mark_as_pending']
    
    def mark_as_responded(self, request, queryset):
        updated = queryset.update(is_responded=True)
        self.message_user(
            request,
            f'{updated} contact submission(s) marked as responded.'
        )
    mark_as_responded.short_description = "Mark selected submissions as responded"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(is_responded=False)
        self.message_user(
            request,
            f'{updated} contact submission(s) marked as pending.'
        )
    mark_as_pending.short_description = "Mark selected submissions as pending"
