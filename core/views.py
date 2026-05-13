from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import *

# Create your views here.
def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]
    latest_blog = BlogPost.objects.filter(is_published=True)[:3]
    latest_cases = CaseStudy.objects.filter(is_published=True)[:3]

    return render(request, 'home.html', {
        'projects': featured_projects,
        'blogs': latest_blog,
        'cases': latest_cases
    })




def about(request):
    basic_info    = BasicInfo.objects.first()
    about_data    = About.objects.first()
    education_list  = Education.objects.all().order_by('-id')
    experience_list = Experience.objects.all().order_by('-id')
    values_list   = CoreValue.objects.all()                    # already ordered by display_order via Meta
    stats_list    = AboutStat.objects.all()                    # ordered by display_order via Meta
    cta           = AboutCTA.objects.first()
    testimonials  = Testimonial.objects.filter(is_featured=True).order_by('-created_at')

    context = {
        'basic_info':      basic_info,
        'about':           about_data,
        'education_list':  education_list,
        'experience_list': experience_list,
        'values_list':     values_list,
        'stats_list':      stats_list,
        'cta':             cta,
        'testimonials':    testimonials,
    }
    return render(request, 'about.html', context)



def projects(request):
    featured_projects = Project.objects.filter(featured=True).order_by('-created_at')[:3]
    recent_projects = Project.objects.filter(featured=False).order_by('-created_at')[:6]
    all_projects = Project.objects.all().order_by('-created_at')
    technologies = Technologies.objects.all().order_by('name')  # optional ordering

    context = {
        'featured_projects': featured_projects,
        'recent_projects': recent_projects,
        'all_projects': all_projects,
        'technologies': technologies,
    }
    return render(request, 'projects.html', context)





def contact(request):
    success_message = None
    error_message = None

    contact_info = ContactInfo.objects.first()

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

            try:
                send_mail(
                    subject=f"New Contact: {subject}",
                    message=f"""
Name: {name}
Email: {email}

Message:
{message}
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass

            success_message = "Your message was sent successfully."
        else:
            error_message = "Please fill all fields properly."

    return render(request, 'contact.html', {
        'contact_info': contact_info,
        'success_message': success_message,
        'error_message': error_message,
    })



def services(request):
    services_list = Service.objects.all().order_by('-is_featured')

    featured_services = services_list.filter(is_featured=True)
    normal_services = services_list.filter(is_featured=False)

    context = {
        'featured_services': featured_services,
        'normal_services': normal_services,
    }

    return render(request, 'services.html', context)




def hire(request):

    status = FreelanceStatus.objects.first()

    faqs = FAQ.objects.all()

    success = None

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        project_type = request.POST.get("project_type")
        budget = request.POST.get("budget")
        deadline = request.POST.get("deadline")
        description = request.POST.get("description")

        if name and email and project_type and budget and description:

            ProjectInquiry.objects.create(
                name=name,
                email=email,
                project_type=project_type,
                budget=budget,
                deadline=deadline if deadline else None,
                description=description
            )

            success = "Your project request has been sent successfully."

        else:
            success = "Please fill all required fields."

    return render(request, 'hire.html', {
        'status': status,
        'faqs': faqs,
        'success': success
    })


def blog(request):

    tag = request.GET.get('tag')

    posts = BlogPost.objects.filter(is_published=True)

    if tag:
        posts = posts.filter(tags__icontains=tag)

    # all tags (for filter UI)
    all_tags = set()
    for post in BlogPost.objects.filter(is_published=True):
        for t in post.get_tags():
            all_tags.add(t)

    return render(request, 'blog.html', {
        'posts': posts,
        'all_tags': sorted(all_tags),
        'active_tag': tag
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    # Reading time (approx 200 words per minute)
    word_count = len(post.content.split())
    reading_time = max(1, word_count // 200)

    # Related posts (simple logic: same tags OR latest posts)
    related_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]

    return render(request, 'blog_detail.html', {
        'post': post,
        'reading_time': reading_time,
        'related_posts': related_posts
    })




def case_studies(request):
    cases = CaseStudy.objects.filter(is_published=True)
    return render(request, 'case_studies.html', {'cases': cases})


def case_study_detail(request, slug):
    case = get_object_or_404(CaseStudy, slug=slug, is_published=True)
    return render(request, 'case_study_detail.html', {'case': case})