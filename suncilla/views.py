from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import json
from .models import (
    Service, Package, Industry, Testimonial, BlogPost, 
    ContactSubmission, SiteSettings
)

def get_site_settings():
    """Get or create default site settings"""
    settings_obj, created = SiteSettings.objects.get_or_create(pk=1)
    return settings_obj

def index(request):
    """Homepage with all sections"""
    services = Service.objects.all()
    packages = Package.objects.all()
    industries = Industry.objects.all()
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    site_settings = get_site_settings()
    
    context = {
        'services': services,
        'packages': packages,
        'industries': industries,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
        'site_settings': site_settings,
    }
    return render(request, 'index.html', context)

def services(request):
    """Services page with details"""
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'services.html', context)

def packages(request):
    """Packages/Pricing page"""
    packages = Package.objects.all()
    site_settings = get_site_settings()
    context = {
        'packages': packages,
        'site_settings': site_settings,
    }
    return render(request, 'packages.html', context)

def industries(request):
    """Industries page"""
    industries = Industry.objects.all()
    context = {'industries': industries}
    return render(request, 'industries.html', context)

def about(request):
    """About page"""
    site_settings = get_site_settings()
    industries = Industry.objects.all()
    context = {
        'site_settings': site_settings,
        'industries': industries,
    }
    return render(request, 'about.html', context)

def blog(request):
    """Blog listing page"""
    posts = BlogPost.objects.filter(is_published=True)
    categories = BlogPost.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category=category)
    
    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'blog.html', context)

def blog_post(request, slug):
    """Individual blog post"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog-post.html', context)

@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page with form"""
    site_settings = get_site_settings()
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        business_type = request.POST.get('business_type', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # Validation
        if not all([name, email, phone, subject, message_text]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('contact')
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        try:
            ContactSubmission.objects.create(
                name=name,
                email=email,
                phone=phone,
                business_type=business_type,
                subject=subject,
                message=message_text,
                ip_address=ip_address,
            )
            messages.success(
                request, 
                'Thank you! Your message has been sent successfully. We\'ll get back to you within 24 hours.'
            )
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again.')
            return redirect('contact')
    
    context = {
        'site_settings': site_settings,
        'industries': Industry.objects.all(),
    }
    return render(request, 'contact.html', context)

def whatsapp_redirect(request):
    """Redirect to WhatsApp chat"""
    site_settings = get_site_settings()
    phone = site_settings.whatsapp_number
    message = settings.WHATSAPP_MESSAGE
    whatsapp_url = f"https://wa.me/{phone}?text={message}"
    return redirect(whatsapp_url)
