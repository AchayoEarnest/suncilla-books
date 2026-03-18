from django.db import models
from django.core.validators import URLValidator, EmailValidator

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    benefits = models.TextField(help_text="Benefits separated by comma")
    icon = models.CharField(max_length=50, default='📊')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title

    def get_benefits(self):
        return [b.strip() for b in self.benefits.split(',') if b.strip()]


class Package(models.Model):
    TIER_CHOICES = [
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='starter')
    description = models.TextField()
    features = models.TextField(help_text="Features separated by newline")
    price_display = models.CharField(max_length=100, blank=True, help_text="e.g., 'Custom Pricing' or '5,000/month'")
    is_popular = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class Industry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🏢')
    how_we_help = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    image = models.CharField(max_length=500, blank=True, help_text="URL to client image")
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'order']

    def __str__(self):
        return self.client_name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    category = models.CharField(max_length=50, default='Tips')
    author = models.CharField(max_length=100, default='Suncilla Books')
    image = models.CharField(max_length=500, blank=True, help_text="URL to featured image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('responded', 'Responded'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    business_type = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class SiteSettings(models.Model):
    phone = models.CharField(max_length=20, default='+254 724 016 375')
    email_primary = models.EmailField(default='info@suncillabooks.com')
    email_secondary = models.EmailField(default='suncillabooks@gmail.com')
    website_url = models.URLField(default='https://www.suncillabooks.com')
    whatsapp_number = models.CharField(max_length=20, default='254724016375')
    company_description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Suncilla Books Settings"
