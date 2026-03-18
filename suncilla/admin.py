from django.contrib import admin
from .models import (
    Service, Package, Industry, Testimonial, BlogPost,
    ContactSubmission, SiteSettings
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    ordering = ('order',)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'is_popular', 'order', 'created_at')
    list_editable = ('is_popular', 'order')
    search_fields = ('name', 'description')
    list_filter = ('tier', 'is_popular')

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    ordering = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'is_featured', 'rating', 'order')
    list_editable = ('is_featured', 'order')
    search_fields = ('client_name', 'company', 'message')
    list_filter = ('is_featured', 'rating')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'ip_address')
    ordering = ('-created_at',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Information', {
            'fields': ('phone', 'whatsapp_number', 'email_primary', 'email_secondary')
        }),
        ('Website Information', {
            'fields': ('website_url', 'company_description')
        }),
    )
