from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class HomePage(Page):
    """Main homepage with hero section"""
    
    # Hero Section
    hero_title = models.CharField(max_length=255, default="Fintaa")
    hero_subtitle = models.CharField(max_length=255, default="SOFTWARE HOUSE")
    hero_typing_text = models.CharField(
        max_length=500, 
        help_text="Text for typing animation",
        default="Transforming Ideas into Digital Reality..."
    )
    hero_description = RichTextField(
        default="Pakistan's Premier Software Development Company - Specializing in cutting-edge technology solutions, from web development to AI agents, we deliver excellence in every project."
    )
    hero_primary_button_text = models.CharField(max_length=50, default="Get Started")
    hero_secondary_button_text = models.CharField(max_length=50, default="View Portfolio")
    
    # About Section
    about_title = models.CharField(max_length=255, default="About Fintaa")
    about_description = RichTextField(
        default="Registered in Pakistan as a sole proprietorship, Fintaa Software House is your trusted partner in digital transformation."
    )
    about_additional_text = RichTextField(blank=True)
    
    # Stats
    technologies_count = models.CharField(max_length=10, default="50+")
    projects_count = models.CharField(max_length=10, default="100+")
    client_satisfaction = models.CharField(max_length=10, default="95%")
    years_experience = models.CharField(max_length=10, default="5+")
    
    # Contact Information
    contact_email = models.EmailField(default="info@Fintaa.pk")
    contact_location = models.CharField(max_length=255, default="Pakistan")
    business_hours = models.CharField(max_length=255, default="24/7 Available")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_typing_text'),
            FieldPanel('hero_description'),
            FieldPanel('hero_primary_button_text'),
            FieldPanel('hero_secondary_button_text'),
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('about_title'),
            FieldPanel('about_description'),
            FieldPanel('about_additional_text'),
        ], heading="About Section"),
        
        MultiFieldPanel([
            FieldPanel('technologies_count'),
            FieldPanel('projects_count'),
            FieldPanel('client_satisfaction'),
            FieldPanel('years_experience'),
        ], heading="Statistics"),
        
        MultiFieldPanel([
            FieldPanel('contact_email'),
            FieldPanel('contact_location'),
            FieldPanel('business_hours'),
        ], heading="Contact Information"),
        
        InlinePanel('services', label="Services"),
        InlinePanel('about_features', label="About Features"),
    ]
    
    max_count = 1


class ServiceItem(Orderable):
    """Individual service items for the homepage"""
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='services')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_svg = models.TextField(
        help_text="SVG icon code for the service",
        blank=True
    )
    
    # Service features (up to 3)
    feature_1 = models.CharField(max_length=255, blank=True)
    feature_2 = models.CharField(max_length=255, blank=True)
    feature_3 = models.CharField(max_length=255, blank=True)
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon_svg'),
        MultiFieldPanel([
            FieldPanel('feature_1'),
            FieldPanel('feature_2'),
            FieldPanel('feature_3'),
        ], heading="Service Features"),
    ]


class AboutFeature(Orderable):
    """Features for the about section"""
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='about_features')
    
    feature_text = models.CharField(max_length=255)
    
    panels = [
        FieldPanel('feature_text'),
    ]


class ServicePage(Page):
    """Individual service detail pages"""
    
    hero_title = models.CharField(max_length=255)
    hero_description = RichTextField()
    hero_image_url = models.URLField(blank=True, help_text="URL for hero image")
    
    # Service Details
    service_overview = RichTextField()
    
    # Process section
    process_title = models.CharField(max_length=255, default="Our Process")
    
    # Technologies section
    technologies_title = models.CharField(max_length=255, default="Technologies We Use")
    
    # Pricing section
    pricing_title = models.CharField(max_length=255, default="Pricing")
    pricing_description = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_description'),
            FieldPanel('hero_image_url'),
        ], heading="Hero Section"),
        
        FieldPanel('service_overview'),
        
        MultiFieldPanel([
            FieldPanel('process_title'),
            InlinePanel('process_steps', label="Process Steps"),
        ], heading="Process Section"),
        
        MultiFieldPanel([
            FieldPanel('technologies_title'),
            InlinePanel('technologies', label="Technologies"),
        ], heading="Technologies"),
        
        MultiFieldPanel([
            FieldPanel('pricing_title'),
            FieldPanel('pricing_description'),
            InlinePanel('pricing_plans', label="Pricing Plans"),
        ], heading="Pricing"),
    ]


class ProcessStep(Orderable):
    """Process steps for service pages"""
    page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name='process_steps')
    
    step_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    panels = [
        FieldPanel('step_number'),
        FieldPanel('title'),
        FieldPanel('description'),
    ]


class Technology(Orderable):
    """Technologies used for services"""
    page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name='technologies')
    
    name = models.CharField(max_length=255)
    logo_url = models.URLField(blank=True, help_text="URL for technology logo")
    description = models.TextField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('logo_url'),
        FieldPanel('description'),
    ]


class PricingPlan(Orderable, ClusterableModel):
    """Pricing plans for services"""
    page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name='pricing_plans')
    
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_popular = models.BooleanField(default=False)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('price'),
        FieldPanel('description'),
        FieldPanel('is_popular'),
        InlinePanel('features', label="Features"),
    ]


class PricingFeature(Orderable):
    """Features for pricing plans"""
    plan = ParentalKey(PricingPlan, on_delete=models.CASCADE, related_name='features')
    
    feature_text = models.CharField(max_length=255)
    is_included = models.BooleanField(default=True)
    
    panels = [
        FieldPanel('feature_text'),
        FieldPanel('is_included'),
    ]


class ProjectPage(Page):
    """Individual project showcase pages"""
    
    # Project Details
    project_title = models.CharField(max_length=255)
    project_subtitle = models.CharField(max_length=255, blank=True)
    client_name = models.CharField(max_length=255)
    project_url = models.URLField(blank=True, help_text="Live project URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    
    # Project Info
    project_overview = RichTextField()
    project_challenge = RichTextField(blank=True)
    project_solution = RichTextField(blank=True)
    project_results = RichTextField(blank=True)
    
    # Project Meta
    project_duration = models.CharField(max_length=100, blank=True)
    project_team_size = models.CharField(max_length=100, blank=True)
    completion_date = models.DateField(blank=True, null=True)
    
    # Featured Image
    featured_image_url = models.URLField(blank=True, help_text="URL for featured project image")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('project_title'),
            FieldPanel('project_subtitle'),
            FieldPanel('client_name'),
            FieldPanel('project_url'),
            FieldPanel('github_url'),
            FieldPanel('featured_image_url'),
        ], heading="Project Details"),
        
        MultiFieldPanel([
            FieldPanel('project_overview'),
            FieldPanel('project_challenge'),
            FieldPanel('project_solution'),
            FieldPanel('project_results'),
        ], heading="Project Content"),
        
        MultiFieldPanel([
            FieldPanel('project_duration'),
            FieldPanel('project_team_size'),
            FieldPanel('completion_date'),
        ], heading="Project Meta"),
        
        InlinePanel('project_technologies', label="Technologies Used"),
        InlinePanel('project_images', label="Project Images"),
    ]


class ProjectTechnology(Orderable):
    """Technologies used in projects"""
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name='project_technologies')
    
    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=100,
        choices=[
            ('frontend', 'Frontend'),
            ('backend', 'Backend'),
            ('database', 'Database'),
            ('deployment', 'Deployment'),
            ('other', 'Other'),
        ],
        default='other'
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('category'),
    ]


class ProjectImage(Orderable):
    """Images for project showcase"""
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name='project_images')
    
    image_url = models.URLField(help_text="URL for project image")
    caption = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    
    panels = [
        FieldPanel('image_url'),
        FieldPanel('caption'),
        FieldPanel('is_featured'),
    ]


class BlogPage(Page):
    """Blog/News pages"""
    
    # Blog Content
    excerpt = models.TextField(max_length=500, help_text="Short description for blog listing")
    featured_image_url = models.URLField(blank=True, help_text="URL for featured blog image")
    
    # Blog Meta
    author = models.CharField(max_length=255, default="Fintaa Team")
    publish_date = models.DateTimeField(auto_now_add=True)
    read_time = models.CharField(max_length=20, default="5 min read")
    
    # Content
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('code', blocks.TextBlock(label='Code')),
    ], blank=True, use_json_field=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('excerpt'),
        FieldPanel('featured_image_url'),
        FieldPanel('author'),
        FieldPanel('read_time'),
        FieldPanel('content'),
        InlinePanel('blog_tags', label="Tags"),
    ]


class BlogTag(Orderable):
    """Tags for blog posts"""
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='blog_tags')
    
    tag_name = models.CharField(max_length=100)
    
    panels = [
        FieldPanel('tag_name'),
    ]


class ContactSubmission(ClusterableModel):
    """Contact form submissions"""
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    service = models.CharField(
        max_length=100,
        choices=[
            ('web_development', 'Web Development'),
            ('mobile_app_development', 'Mobile App Development'),
            ('ai_automation', 'AI & Automation'),
            ('cybersecurity', 'Cybersecurity'),
            ('digital_marketing', 'Digital Marketing'),
            ('call_center_services', 'Call Center Services'),
        ]
    )
    budget = models.CharField(
        max_length=50,
        choices=[
            ('under_5k', 'Under $5,000'),
            ('5k_15k', '$5,000 - $15,000'),
            ('15k_50k', '$15,000 - $50,000'),
            ('50k_plus', '$50,000+'),
            ('not_sure', 'Not Sure'),
        ],
        blank=True
    )
    timeline = models.CharField(
        max_length=50,
        choices=[
            ('asap', 'ASAP'),
            ('1_month', 'Within 1 Month'),
            ('3_months', 'Within 3 Months'),
            ('6_months', 'Within 6 Months'),
            ('flexible', 'Flexible'),
        ],
        blank=True
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Internal notes for admin use")
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('email'),
            FieldPanel('phone'),
            FieldPanel('company'),
        ], heading="Contact Information"),
        MultiFieldPanel([
            FieldPanel('service'),
            FieldPanel('budget'),
            FieldPanel('timeline'),
        ], heading="Project Details"),
        FieldPanel('message'),
        MultiFieldPanel([
            FieldPanel('is_responded'),
            FieldPanel('notes'),
        ], heading="Admin Section"),
    ]
    
    def __str__(self):
        return f"{self.name} - {self.get_service_display()}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"


class AboutPage(Page):
    """About Us page"""
    
    hero_title = models.CharField(max_length=255, default="About Fintaa")
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_description = RichTextField()
    hero_image_url = models.URLField(blank=True, help_text="URL for hero image")
    
    # Company Story
    story_title = models.CharField(max_length=255, default="Our Story")
    story_content = RichTextField()
    
    # Mission & Vision
    mission_title = models.CharField(max_length=255, default="Our Mission")
    mission_content = RichTextField()
    vision_title = models.CharField(max_length=255, default="Our Vision")
    vision_content = RichTextField()
    
    # Values
    values_title = models.CharField(max_length=255, default="Our Values")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_description'),
            FieldPanel('hero_image_url'),
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('story_title'),
            FieldPanel('story_content'),
        ], heading="Company Story"),
        
        MultiFieldPanel([
            FieldPanel('mission_title'),
            FieldPanel('mission_content'),
            FieldPanel('vision_title'),
            FieldPanel('vision_content'),
        ], heading="Mission & Vision"),
        
        MultiFieldPanel([
            FieldPanel('values_title'),
            InlinePanel('values', label="Company Values"),
        ], heading="Values Section"),
        
        InlinePanel('team_members', label="Team Members"),
    ]
    
    max_count = 1


class CompanyValue(Orderable):
    """Company values for about page"""
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name='values')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_name = models.CharField(max_length=100, blank=True, help_text="Material icon name")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon_name'),
    ]


class TeamMember(Orderable):
    """Team members for about page"""
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name='team_members')
    
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    image_url = models.URLField(blank=True, help_text="URL for team member photo")
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('bio'),
        FieldPanel('image_url'),
        MultiFieldPanel([
            FieldPanel('linkedin_url'),
            FieldPanel('twitter_url'),
            FieldPanel('github_url'),
        ], heading="Social Links"),
    ]


class ContactPage(Page):
    """Contact Us page"""
    
    hero_title = models.CharField(max_length=255, default="Get In Touch")
    hero_description = RichTextField()
    
    # Contact Information
    office_address = models.TextField(blank=True)
    email_address = models.EmailField(default="info@Fintaa.pk")
    phone_number = models.CharField(max_length=20, blank=True)
    business_hours = models.CharField(max_length=255, default="24/7 Available")
    
    # Map
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL")
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_description'),
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('office_address'),
            FieldPanel('email_address'),
            FieldPanel('phone_number'),
            FieldPanel('business_hours'),
        ], heading="Contact Information"),
        
        FieldPanel('map_embed_url'),
        
        InlinePanel('contact_methods', label="Additional Contact Methods"),
    ]
    
    max_count = 1
    
    def serve(self, request):
        from django.shortcuts import redirect
        from django.contrib import messages
        
        if request.method == 'POST':
            # Handle form submission
            try:
                # Create contact submission
                submission = ContactSubmission.objects.create(
                    name=request.POST.get('name', ''),
                    email=request.POST.get('email', ''),
                    phone=request.POST.get('phone', ''),
                    company=request.POST.get('company', ''),
                    service=request.POST.get('service', 'general'),
                    budget=request.POST.get('budget', 'not_specified'),
                    timeline=request.POST.get('timeline', 'flexible'),
                    message=request.POST.get('message', ''),
                    status='new'
                )
                messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
                return redirect(request.path)
            except Exception as e:
                messages.error(request, 'There was an error submitting your message. Please try again.')
        
        return super().serve(request)


class ContactMethod(Orderable):
    """Additional contact methods"""
    page = ParentalKey(ContactPage, on_delete=models.CASCADE, related_name='contact_methods')
    
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    icon_name = models.CharField(max_length=100, blank=True)
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('link'),
        FieldPanel('icon_name'),
    ]


# New Page Models for Multi-page Navigation

class ServicesPage(Page):
    """Services listing page"""
    
    hero_title = models.CharField(max_length=255, default="Our Services")
    hero_description = RichTextField(
        default="<p>We offer comprehensive software development services to transform your ideas into reality.</p>"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_description'),
        InlinePanel('service_items', label="Services"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['services'] = self.service_items.all()
        return context


class ServicePageItem(Orderable):
    """Individual service for Services page"""
    page = ParentalKey(ServicesPage, on_delete=models.CASCADE, related_name='service_items')
    title = models.CharField(max_length=255)
    description = RichTextField()
    icon = models.CharField(max_length=100, help_text="Font Awesome icon class")
    features = RichTextField(blank=True, help_text="List of features for this service")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon'),
        FieldPanel('features'),
    ]


class TeamPage(Page):
    """Team page showing all team members"""
    
    hero_title = models.CharField(max_length=255, default="Our Team")
    hero_description = RichTextField(
        default="<p>Meet the talented individuals who make our software house exceptional.</p>"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_description'),
        InlinePanel('team_members', label="Team Members"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['team_members'] = self.team_members.all()
        return context


class TeamPageMember(Orderable):
    """Individual team member for Team page"""
    page = ParentalKey(TeamPage, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = RichTextField()
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    skills = models.CharField(max_length=500, help_text="Comma-separated skills")
    
    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('bio'),
        FieldPanel('email'),
        FieldPanel('linkedin'),
        FieldPanel('github'),
        FieldPanel('twitter'),
        FieldPanel('skills'),
    ]


class BlogIndexPage(Page):
    """Blog listing page"""
    
    hero_title = models.CharField(max_length=255, default="Our Blog")
    hero_description = RichTextField(
        default="<p>Stay updated with the latest in technology, development insights, and industry trends.</p>"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_description'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get all blog posts
        blog_posts = BlogPost.objects.live().public().order_by('-first_published_at')
        context['blog_posts'] = blog_posts
        return context
    
    subpage_types = ['portfolio.BlogPost']


class BlogPost(Page):
    """Individual blog post"""
    
    excerpt = models.TextField(max_length=500, help_text="Brief description for listing pages")
    author = models.CharField(max_length=255, default="Fintaa Team")
    publish_date = models.DateField("Post date")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    
    # Content
    content = StreamField([
        ('heading', blocks.CharBlock(classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('code', blocks.TextBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('list', blocks.ListBlock(blocks.CharBlock(label="Item"))),
    ], blank=True, use_json_field=True)
    
    # Tags
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    content_panels = Page.content_panels + [
        FieldPanel('excerpt'),
        FieldPanel('author'),
        FieldPanel('publish_date'),
        FieldPanel('featured_image'),
        FieldPanel('content'),
        FieldPanel('tags'),
    ]
    
    parent_page_types = ['portfolio.BlogIndexPage']


class PortfolioIndexPage(Page):
    """Portfolio listing page"""
    
    hero_title = models.CharField(max_length=255, default="Our Portfolio")
    hero_description = RichTextField(
        default="<p>Explore our successful projects and see how we've helped businesses transform their digital presence.</p>"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_description'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get all project pages
        projects = ProjectPage.objects.live().public().order_by('-first_published_at')
        context['projects'] = projects
        return context
    
    subpage_types = ['portfolio.ProjectPage']
    max_count = 1
