from django.db import models

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
    description = models.TextField()

    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    live_demo_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)

    featured = models.BooleanField(default=False)

    tech_stack = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated technologies, e.g. Django, Bootstrap, MySQL"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='fullstack'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

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
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
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
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, blank=True)  # e.g. "fas fa-code"
    price_range = models.CharField(max_length=100, blank=True)  # e.g. "$50 - $200"
    turnaround = models.CharField(max_length=100, blank=True)   # e.g. "3–5 days"
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


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


class ProjectInquiry(models.Model):
    PROJECT_TYPES = [
        ('website', 'Website Development'),
        ('django', 'Django Web App'),
        ('ecommerce', 'E-commerce Store'),
        ('automation', 'Automation Script'),
        ('ai', 'AI Integration'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()

    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)

    budget = models.CharField(max_length=100)
    deadline = models.DateField(null=True, blank=True)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project_type}"


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
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)

    tags = models.CharField(max_length=255, blank=True)  # comma-separated

    is_published = models.BooleanField(default=True)

    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    # 🔥 reading time helper
    def reading_time(self):
        words = len(self.content.split())
        return max(1, words // 200)

    # 🔥 clean tags
    def get_tags(self):
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