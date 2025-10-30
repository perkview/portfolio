from django.db import models

# Create your models here.
class About(models.Model):
    profile_image = models.ImageField(upload_to='profile/', default='profile/default.jpg')
    title = models.CharField(max_length=100, default="About Me")
    intro = models.TextField()
    description = models.TextField()
    resume_link = models.URLField(blank=True, null=True)

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

    def __str__(self):
        return self.title
    
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
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_demo_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    tech_stack = models.CharField(max_length=255, blank=True, help_text="Comma-separated technologies, e.g. Django, Bootstrap, MySQL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    feedback = models.TextField()
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
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

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