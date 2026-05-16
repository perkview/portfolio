from django.db import models
from django.utils.text import slugify

# Create your models here.
class About(models.Model):
    profile_image = models.ImageField(
        upload_to='profile/',
        default='profile/default.jpg'
    )

    title = models.CharField(
        max_length=100,
        default="About Me"
    )

    intro = models.TextField()

    description = models.TextField()

    resume_link = models.URLField(blank=True, null=True)

    # NEW FIELDS
    location = models.CharField(
        max_length=100,
        default="Pakistan"
    )

    availability_text = models.CharField(
        max_length=100,
        default="Open to Freelance"
    )

    projects_status = models.CharField(
        max_length=100,
        default="Available for Projects"
    )

    profile_status = models.CharField(
        max_length=50,
        default="Available"
    )

    def __str__(self):
        return self.title


class Education(models.Model):
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    year_range = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.degree


class Experience(models.Model):
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    year_range = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.role


class CoreValue(models.Model):
    title = models.CharField(max_length=100)

    description = models.TextField()

    icon_class = models.CharField(
        max_length=100,
        default="bi bi-star-fill"
    )

    icon_bg = models.CharField(
        max_length=50,
        default="rgba(59,130,246,0.1)"
    )

    icon_color = models.CharField(
        max_length=50,
        default="var(--accent)"
    )

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title
    



class AboutStat(models.Model):

    title = models.CharField(max_length=100)

    value = models.PositiveIntegerField(default=0)

    suffix = models.CharField(
        max_length=10,
        default="+"
    )

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title
    


class AboutCTA(models.Model):

    eyebrow = models.CharField(
        max_length=100,
        default="Ready to Build?"
    )

    heading = models.CharField(
        max_length=255,
        default="Let's work on something worth building."
    )

    highlighted_text = models.CharField(
        max_length=255,
        default="worth building."
    )

    subheading = models.TextField()

    primary_button_text = models.CharField(
        max_length=50,
        default="Start a Project"
    )

    primary_button_link = models.CharField(
        max_length=255,
        default="/freelance/"
    )

    secondary_button_text = models.CharField(
        max_length=50,
        default="Send a Message"
    )

    secondary_button_link = models.CharField(
        max_length=255,
        default="/contact/"
    )

    def __str__(self):
        return self.heading
    
class SkillsHeader(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.TextField(blank=True)

class TechnicalSkill(models.Model):
    category = models.CharField(max_length=100)
    skills = models.CharField(max_length=255)
    proficiency = models.PositiveIntegerField(default=0)  # e.g. 85%

class Tool(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='tools/', blank=True, null=True)

class SoftSkill(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, help_text="Bootstrap icon class")

class SummarySkill(models.Model):
    skill_name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=20, default='#007BFF')


class Project(models.Model):

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('experimental', 'Experimental'),
    ]

    CATEGORY_CHOICES = [
        ('fullstack', 'Full Stack'),
        ('django', 'Django'),
        ('ai', 'AI / ML'),
        ('automation', 'Automation'),
        ('ecommerce', 'E-commerce'),
        ('productivity', 'Productivity'),
        ('game', 'Game'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    live_demo_link = models.URLField(blank=True, null=True)
    github_link    = models.URLField(blank=True, null=True)

    # ── Renamed: template uses is_featured, keep `featured` as DB col ──
    featured = models.BooleanField(default=False, db_column='featured')

    tech_stack = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated, e.g. Django, Bootstrap, MySQL"
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='fullstack',
        help_text="Shown as the card category label"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed'
    )

    # ── New fields the template reads ──────────────────────────────────
    users_count = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text="Display string, e.g. '1,200+'"
    )

    performance_note = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text="Short metric shown in the metrics row, e.g. '99% Uptime'"
    )

    case_study = models.OneToOneField(
        'CaseStudy',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='project_ref',
        help_text="Link this project to its case study"
    )

    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower = shown first. Controls card order."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    # ── Auto slug ──────────────────────────────────────────────────────
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.title)
            slug = base
            n = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # ── Template helpers ───────────────────────────────────────────────
    @property
    def is_featured(self):
        """Alias so template {% if project.is_featured %} works."""
        return self.featured

    @property
    def tags_list(self):
        """
        Returns a clean Python list from the comma-separated tech_stack.
        Template: {% for tag in project.tags_list %}
        """
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    @property
    def tech_stack_lower(self):
        """
        Lowercase string used for the data-tech attribute in the filter bar.
        e.g. 'django,postgresql,stripe' → matches JS filter logic.
        """
        return self.tech_stack.lower()

    def get_category_display_label(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)


class Testimonial(models.Model):

    STAR_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    name = models.CharField(max_length=100)

    position = models.CharField(max_length=150, blank=True)

    company = models.CharField(max_length=150, blank=True)

    image = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True
    )

    feedback = models.TextField()

    stars = models.PositiveIntegerField(
        choices=STAR_CHOICES,
        default=5
    )

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.company})"
    



class ContactMessage(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Reviewing'),
        ('replied', 'Replied'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('spam', 'Spam'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('web', 'Web Application'),
        ('saas', 'SaaS Platform'),
        ('ai', 'AI Integration'),
        ('automation', 'Automation / Bots'),
        ('ecommerce', 'E-Commerce'),
        ('dashboard', 'Dashboard / CMS'),
        ('api', 'Backend / API'),
        ('mvp', 'MVP / Prototype'),
        ('student', 'Student Project'),
        ('other', 'Other / Not Sure'),
    ]

    BUDGET_CHOICES = [
        ('under-500', '< $500'),
        ('500-1500', '$500–1.5k'),
        ('1500-5000', '$1.5k–5k'),
        ('5000-plus', '$5k+'),
        ('discuss', "Let's Talk"),
        ('not-sure', 'Not Sure'),
    ]

    # =========================================================
    # USER INFO
    # =========================================================
    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    company = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    # =========================================================
    # PROJECT INFO
    # =========================================================
    subject = models.CharField(max_length=150)

    project_type = models.CharField(
        max_length=30,
        choices=PROJECT_TYPE_CHOICES,
        default='other'
    )

    budget = models.CharField(
        max_length=30,
        choices=BUDGET_CHOICES,
        blank=True,
        null=True
    )

    timeline = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    message = models.TextField()

    # =========================================================
    # WORKFLOW
    # =========================================================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='normal'
    )

    is_read = models.BooleanField(default=False)

    is_resolved = models.BooleanField(default=False)

    admin_notes = models.TextField(
        blank=True,
        null=True
    )

    replied_at = models.DateTimeField(
        blank=True,
        null=True
    )

    resolved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    # =========================================================
    # META / TRACKING
    # =========================================================
    source = models.CharField(
        max_length=50,
        default='portfolio_contact_form'
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # =========================================================
    # BUSINESS INTELLIGENCE / SALES
    # =========================================================

    lead_score = models.PositiveIntegerField(
        default=0,
        help_text="Internal score for lead quality."
    )

    conversion_probability = models.PositiveIntegerField(
        default=0,
        help_text="Estimated probability of conversion (0-100)."
    )

    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Estimated project value."
    )

    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Internal tags like startup, urgent, high-budget."
    )

    follow_up_date = models.DateTimeField(
        blank=True,
        null=True
    )

    last_contacted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    assigned_to = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text="Assigned admin/team member."
    )

    internal_priority_notes = models.TextField(
        blank=True,
        null=True
    )

    is_hot_lead = models.BooleanField(
        default=False
    )

    is_archived = models.BooleanField(
        default=False
    )

    client_budget_estimate = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    expected_close_date = models.DateField(
        blank=True,
        null=True
    )

    communication_history = models.JSONField(
        default=list,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    @property
    def is_high_value(self):
        return self.lead_score >= 80


    @property
    def short_message(self):
        return self.message[:120]




class ContactInfo(models.Model):
    email = models.EmailField(max_length=150)

    # Optional social links
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    github = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return f"Contact Info ({self.email})"

class BasicInfo(models.Model):
    # 👤 Hero Section Data
    full_name = models.CharField(max_length=100, help_text="Your full name (e.g. Muhammad Ahmad)")
    tagline = models.CharField(max_length=200, help_text="Your short title or tagline (e.g. Full Stack Developer | UI/UX Enthusiast)")
    hero_image = models.ImageField(upload_to='profile/', default='profile/default.jpg', help_text="Profile image for hero section")


    # 💬 About Preview Section
    about_heading = models.CharField(max_length=100, default="About Me", help_text="Heading shown above About section preview")
    about_short_description = models.TextField(help_text="Short paragraph displayed on the home page in 'About Me' section")

    # 🌐 Buttons / Call To Actions
    work_button_text = models.CharField(max_length=50, default="View My Work")
    contact_button_text = models.CharField(max_length=50, default="Contact Me")

    # 📞 Contact Preview Section
    contact_preview_heading = models.CharField(max_length=100, default="Let’s Connect")
    contact_preview_text = models.TextField(help_text="Short paragraph shown before the Contact button at the end")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Basic Info"
        verbose_name_plural = "Basic Info"

    def __str__(self):
        return self.full_name
    
class Technologies(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='tech_icons/')  # or use URLField if icons are external
    order = models.PositiveIntegerField(default=0)  # optional: to control display order

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    

class Service(models.Model):

    name = models.CharField(max_length=120)

    slug = models.SlugField(unique=True)

    short_description = models.CharField(max_length=220)

    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to='services/covers/',
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    seo_title = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    seo_description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name
    



class ServicePackage(models.Model):

    BILLING_CHOICES = [
        ('fixed', 'Fixed Price'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom Quote'),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='packages'
    )

    name = models.CharField(max_length=120)

    slug = models.SlugField(unique=True)

    short_description = models.CharField(max_length=220)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    billing_type = models.CharField(
        max_length=20,
        choices=BILLING_CHOICES,
        default='fixed'
    )

    features = models.JSONField(
        default=list,
        blank=True
    )

    delivery_time = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    revisions = models.PositiveIntegerField(
        default=0
    )

    is_popular = models.BooleanField(default=False)

    is_featured = models.BooleanField(default=False)

    is_custom_quote = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    button_text = models.CharField(
        max_length=50,
        default='Get Started'
    )

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'price']

    def __str__(self):
        return f"{self.service.name} - {self.name}"
    



class ProjectInquiry(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Reviewing'),
        ('qualified', 'Qualified'),
        ('discovery', 'Discovery Call'),
        ('proposal_sent', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('in_progress', 'In Progress'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('spam', 'Spam'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('web', 'Web Application'),
        ('saas', 'SaaS Platform'),
        ('ai', 'AI Integration'),
        ('automation', 'Automation / Bots'),
        ('ecommerce', 'E-Commerce'),
        ('dashboard', 'Dashboard / CMS'),
        ('api', 'Backend / API'),
        ('mvp', 'MVP / Prototype'),
        ('student', 'Student Project'),
        ('other', 'Other / Not Sure'),
    ]

    BUDGET_CHOICES = [
        ('under-500', '< $500'),
        ('500-1500', '$500–1.5k'),
        ('1500-5000', '$1.5k–5k'),
        ('5000-plus', '$5k+'),
        ('discuss', "Let's Talk"),
        ('not-sure', 'Not Sure'),
    ]

    SOURCE_CHOICES = [
        ('contact_page', 'Contact Page'),
        ('services_page', 'Services Page'),
        ('package_page', 'Package Page'),
        ('landing_page', 'Landing Page'),
        ('portfolio_page', 'Portfolio Page'),
        ('case_study_page', 'Case Study Page'),
        ('direct', 'Direct'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('other', 'Other'),
    ]

    # =====================================================
    # CLIENT INFORMATION
    # =====================================================

    full_name = models.CharField(max_length=120)

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    company = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # =====================================================
    # PROJECT DETAILS
    # =====================================================

    subject = models.CharField(max_length=200)

    project_type = models.CharField(
        max_length=30,
        choices=PROJECT_TYPE_CHOICES,
        default='other'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    selected_package = models.ForeignKey(
        ServicePackage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    budget = models.CharField(
        max_length=50,
        choices=BUDGET_CHOICES,
        blank=True,
        null=True
    )

    client_budget_estimate = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    timeline = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    deadline = models.DateField(
        blank=True,
        null=True
    )

    message = models.TextField()

    attachments = models.FileField(
        upload_to='inquiries/files/',
        blank=True,
        null=True
    )

    # =====================================================
    # BUSINESS WORKFLOW
    # =====================================================

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='new'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )

    is_read = models.BooleanField(default=False)

    is_resolved = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)

    is_hot_lead = models.BooleanField(default=False)

    admin_notes = models.TextField(
        blank=True,
        null=True
    )

    internal_priority_notes = models.TextField(
        blank=True,
        null=True
    )

    replied_at = models.DateTimeField(
        blank=True,
        null=True
    )

    resolved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    follow_up_date = models.DateTimeField(
        blank=True,
        null=True
    )

    last_contacted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    expected_close_date = models.DateField(
        blank=True,
        null=True
    )

    assigned_to = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text="Assigned admin/team member."
    )

    # =====================================================
    # SALES / BUSINESS INTELLIGENCE
    # =====================================================

    lead_score = models.PositiveIntegerField(
        default=0,
        help_text="Internal score for lead quality."
    )

    conversion_probability = models.PositiveIntegerField(
        default=0,
        help_text="Estimated probability of conversion (0-100)."
    )

    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Estimated project value."
    )

    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Internal tags like startup, urgent, high-budget."
    )

    communication_history = models.JSONField(
        default=list,
        blank=True
    )

    # =====================================================
    # TRACKING / ANALYTICS
    # =====================================================

    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        default='contact_page'
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    referrer = models.URLField(
        blank=True,
        null=True
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project Inquiry"
        verbose_name_plural = "Project Inquiries"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

    @property
    def is_high_value(self):
        return self.lead_score >= 80

    @property
    def short_message(self):
        return self.message[:120]





class PackageFeature(models.Model):

    package = models.ForeignKey(
        ServicePackage,
        on_delete=models.CASCADE,
        related_name='package_features'
    )

    feature = models.CharField(max_length=200)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.feature
    


    


class FreelanceStatus(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('limited', 'Taking Limited Work'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    available_from = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_status_display()





class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('pricing', 'Pricing'),
        ('workflow', 'Workflow'),
        ('legal', 'Legal'),
        ('general', 'General'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')

    def __str__(self):
        return self.question


class BlogPost(models.Model):
    title         = models.CharField(max_length=200)
    slug          = models.SlugField(unique=True, blank=True)
    content       = models.TextField()
    cover_image   = models.ImageField(upload_to='blog/', blank=True, null=True)
    tags          = models.CharField(max_length=255, blank=True)   # comma-separated
    is_published  = models.BooleanField(default=True)
    published_at  = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-published_at']
 
    def __str__(self):
        return self.title
 
    # Auto-generate slug on first save
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
 
    # ── Helpers ──────────────────────────────────────────────
 
    @property
    def reading_time(self):
        """Estimated reading time in minutes (≈200 wpm)."""
        words = len(self.content.split())
        return max(1, words // 200)
 
    def get_tags(self):
        """Return a cleaned list of tag strings."""
        return [t.strip() for t in self.tags.split(',') if t.strip()]
    


class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    project = models.CharField(max_length=200, blank=True)  # e.g. FileNest, QuantumTask

    problem = models.TextField()
    approach = models.TextField()
    tech_decisions = models.TextField()
    outcome = models.TextField()
    lessons_learned = models.TextField()

    cover_image = models.ImageField(upload_to='case_studies/', blank=True, null=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title





class BlogSubscriber(models.Model):

    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)

    source = models.CharField(
        max_length=50,
        default="website_newsletter"
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email