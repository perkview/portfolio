from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import About, Education, Experience, CoreValue, SkillsHeader, TechnicalSkill, Tool, SoftSkill, SummarySkill, Project, Testimonial, ContactMessage, ContactInfo, BasicInfo, Technologies

# Create your views here.
def home(request):
    # Fetch only the first (active) records
    basic_info = BasicInfo.objects.first()
    about = About.objects.first()
    featured_projects = Project.objects.filter(featured=True).order_by('created_at')[:3]
    contact_info = ContactInfo.objects.first()

    context = {
        'basic_info': basic_info,
        'about': about,
        'featured_projects': featured_projects,
        'contact_info': contact_info,
    }
    return render(request, 'home.html', context)

def about(request):
    basic_info = BasicInfo.objects.first()
    about_data = About.objects.first()
    education_list = Education.objects.all().order_by('-id')
    experience_list = Experience.objects.all().order_by('-id')
    values_list = CoreValue.objects.all()

    context = {
        'basic_info': basic_info,
        'about': about_data,
        'education_list': education_list,
        'experience_list': experience_list,
        'values_list': values_list,
    }
    return render(request, 'about.html', context)

def skills(request):
    skills_header = SkillsHeader.objects.first()
    technical_skills = TechnicalSkill.objects.all()
    tools = Tool.objects.all()
    soft_skills = SoftSkill.objects.all()
    summary_skills = SummarySkill.objects.all()

    context = {
        'skills_header': skills_header,
        'technical_skills': technical_skills,
        'tools': tools,
        'soft_skills': soft_skills,
        'summary_skills': summary_skills,
    }
    return render(request, 'skills.html', context)

def projects(request):
    featured_projects = Project.objects.filter(featured=True).order_by('-created_at')[:3]
    recent_projects = Project.objects.filter(featured=False).order_by('-created_at')[:6]
    all_projects = Project.objects.all().order_by('-created_at')
    technologies = Technologies.objects.all()  # Fetch all tech stack items

    context = {
        'featured_projects': featured_projects,
        'recent_projects': recent_projects,
        'all_projects': all_projects,
        'technologies': technologies,
    }
    return render(request, 'projects.html', context)

def testimonials(request):
    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    other_testimonials = Testimonial.objects.filter(is_featured=False)
    return render(request, 'testimonials.html', {
        'featured_testimonials': featured_testimonials,
        'other_testimonials': other_testimonials,
    })

def resume(request):
    education_list = Education.objects.all()
    experience_list = Experience.objects.all()
    summary_skills = SummarySkill.objects.all()
    soft_skills = SoftSkill.objects.all()
    technical_skills = TechnicalSkill.objects.all()
    tools = Tool.objects.all()
    skills_header = SkillsHeader.objects.first()

    context = {
        'education_list': education_list,
        'experience_list': experience_list,
        'summary_skills': summary_skills,
        'soft_skills': soft_skills,
        'technical_skills': technical_skills,
        'tools': tools,
        'skills_header': skills_header,
    }
    return render(request, 'resume.html', context)


def contact(request):
    success_message = None
    error_message = None

    contact_info = ContactInfo.objects.first()  # fetch the only record

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Optional email notification
            try:
                send_mail(
                    subject=f"New Contact Message: {subject}",
                    message=f"From: {name} ({email})\n\nMessage:\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass

            success_message = "✅ Your message has been sent successfully!"
        else:
            error_message = "❌ Please fill in all required fields."

    return render(request, 'contact.html', {
        'contact_info': contact_info,
        'success_message': success_message,
        'error_message': error_message,
    })
