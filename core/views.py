from django.shortcuts import render, get_object_or_404
from .models import *
from django.shortcuts import render
from .models import ContactInfo, ContactMessage
from django.contrib import messages

def get_client_ip(request):

    x_forwarded_for = request.META.get(
        'HTTP_X_FORWARDED_FOR'
    )

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]

    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip



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



from django.shortcuts import render
from .models import Project, Technologies


def projects(request):
    """
    Projects archive page.

    Splits into:
      featured_projects  – up to 3 featured projects, shown in the large
                           horizontal cards at the top.
      all_projects       – every project (including featured ones) for the
                           filterable grid below.  Featured ones get a badge.
      technologies       – tech-stack grid at the bottom of the page.
    """

    featured_projects = (
        Project.objects
        .filter(featured=True)
        .select_related('case_study')      # avoids N+1 on case study links
        .order_by('display_order', '-created_at')[:3]
    )

    all_projects = (
        Project.objects
        .all()
        .select_related('case_study')
        .order_by('display_order', '-created_at')
    )

    technologies = Technologies.objects.all().order_by('order', 'name')

    context = {
        'featured_projects': featured_projects,
        'all_projects': all_projects,
        'technologies': technologies,
    }
    return render(request, 'projects.html', context)




def contact(request):

    success_message = None
    error_message = None

    contact_info = ContactInfo.objects.first()

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        company = request.POST.get("company", "").strip()

        subject = request.POST.get("subject", "").strip()

        project_type = request.POST.get(
            "project_type",
            ""
        ).strip()

        budget = request.POST.get("budget", "").strip()

        timeline = request.POST.get("timeline", "").strip()

        message = request.POST.get("message", "").strip()

        if name and email and subject and message:

            ip_address = request.META.get(
                "REMOTE_ADDR"
            )

            user_agent = request.META.get(
                "HTTP_USER_AGENT",
                ""
            )

            ContactMessage.objects.create(

                name=name,
                email=email,
                phone=phone,

                company=company,

                subject=subject,

                project_type=project_type or "other",

                budget=budget,

                timeline=timeline,

                message=message,

                ip_address=ip_address,

                user_agent=user_agent,
            )
            success_message = (
                "Your message has been sent successfully."
            )

        else:

            error_message = (
                "Please fill all required fields properly."
            )

    return render(request, "contact.html", {

        "contact_info": contact_info,

        "success_message": success_message,

        "error_message": error_message,
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

    success_message = None
    error_message = None

    selected_service = None
    selected_package = None

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        company = request.POST.get("company", "").strip()

        project_type = request.POST.get("project_type", "").strip()

        budget = request.POST.get("budget", "").strip()
        timeline = request.POST.get("timeline", "").strip()
        deadline = request.POST.get("deadline", "").strip()

        message = request.POST.get("description", "").strip()

        selected_service_slug = request.POST.get("selected_service")
        selected_package_slug = request.POST.get("selected_package")

        # Optional: resolve service/package if you use them
        try:
            if selected_service_slug:
                selected_service = Service.objects.filter(slug=selected_service_slug).first()

            if selected_package_slug:
                selected_package = ServicePackage.objects.filter(slug=selected_package_slug).first()
        except:
            selected_service = None
            selected_package = None

        if name and email and project_type and message:

            ip_address = request.META.get("REMOTE_ADDR")
            user_agent = request.META.get("HTTP_USER_AGENT", "")

            ProjectInquiry.objects.create(

                full_name=name,
                email=email,
                phone=phone,
                company=company,

                subject=f"{project_type} inquiry from {name}",

                project_type=project_type,
                service=selected_service,
                selected_package=selected_package,

                budget=budget or None,
                timeline=timeline or None,
                deadline=deadline or None,

                message=message,

                source="hire_page",
                ip_address=ip_address,
                user_agent=user_agent,
            )

            success_message = "Your project inquiry has been submitted successfully."

        else:
            error_message = "Please fill all required fields properly."

    return render(request, "hire.html", {

        "status": status,
        "faqs": faqs,

        "success_message": success_message,
        "error_message": error_message,

        "selected_service": selected_service,
        "selected_package": selected_package,
    })






# ============================================================
# views.py
# ============================================================
 
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q
 
 
# ── Constants ───────────────────────────────────────────────────────────────
POSTS_PER_PAGE = 6   # cards shown per "page" / per Load-More click
 
 
# ── Helpers ─────────────────────────────────────────────────────────────────
 
def _build_queryset(tag: str, search: str):
    """Return a filtered, published BlogPost queryset."""
    qs = BlogPost.objects.filter(is_published=True)
 
    if tag:
        qs = qs.filter(tags__icontains=tag)
 
    if search:
        qs = qs.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(tags__icontains=search)
        )
 
    return qs
 
 
def _collect_all_tags():
    """
    Gather every distinct tag from published posts in a single DB hit.
    Returns a sorted list of tag strings.
    """
    all_tags: set[str] = set()
    for tag_string in BlogPost.objects.filter(is_published=True).values_list('tags', flat=True):
        for t in (t.strip() for t in tag_string.split(',') if t.strip()):
            all_tags.add(t)
    return sorted(all_tags)
 
 
# ── Views ───────────────────────────────────────────────────────────────────
 
def blog(request):
    """
    Main blog listing.
 
    First POSTS_PER_PAGE posts are rendered server-side.
    Subsequent pages are loaded via the `blog_load_more` AJAX endpoint
    (triggered by the 'Load More' button in the template).
 
    Query params:
        tag    – filter by tag  (e.g. ?tag=django)
        search – full-text search (e.g. ?search=celery)
    """
    tag    = request.GET.get('tag',    '').strip()
    search = request.GET.get('search', '').strip()
 
    qs = _build_queryset(tag, search)
 
    paginator   = Paginator(qs, POSTS_PER_PAGE)
    page_obj    = paginator.get_page(1)          # always start at page 1
 
    # The featured post is the single most-recent published post
    # (independent of tag/search filter so it doesn't disappear)
    featured = BlogPost.objects.filter(is_published=True).first()
 
    return render(request, 'blog.html', {
        'featured':       featured,
        'posts':          page_obj.object_list,   # first N posts for the grid
        'all_tags':       _collect_all_tags(),
        'active_tag':     tag,
        'search_query':   search,
        'has_more':       page_obj.has_next(),     # show/hide Load More btn
        'next_page':      2,                       # next page the JS will fetch
        'total_count':    paginator.count,         # total matching posts
    })
 
 
def blog_load_more(request):
    """
    AJAX endpoint — returns rendered card HTML + pagination state.
 
    Called by the 'Load More' button via fetch().
 
    Query params (all forwarded from the front-end):
        page   – integer page number to fetch
        tag    – current tag filter
        search – current search term
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Graceful fallback: redirect to the main blog page
        return redirect('blog')
 
    page_number = int(request.GET.get('page',   2))
    tag         =     request.GET.get('tag',    '').strip()
    search      =     request.GET.get('search', '').strip()
 
    qs        = _build_queryset(tag, search)
    paginator = Paginator(qs, POSTS_PER_PAGE)
    page_obj  = paginator.get_page(page_number)
 
    # Render only the card fragments, not the full page
    html = render_to_string(
        'partials/blog_cards.html',
        {'posts': page_obj.object_list},
        request=request,
    )
 
    return JsonResponse({
        'html':      html,
        'has_more':  page_obj.has_next(),
        'next_page': page_number + 1,
        'loaded':    page_obj.end_index(),   # cumulative cards loaded so far
        'total':     paginator.count,
    })
 
 
def blog_detail(request, slug):
    """Full article page."""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
 
    # Related posts: prefer same-tag matches, fall back to latest 3
    post_tags     = post.get_tags()
    related_posts = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)
 
    if post_tags:
        tag_filter = Q()
        for t in post_tags:
            tag_filter |= Q(tags__icontains=t)
        related_posts = related_posts.filter(tag_filter)
 
    related_posts = related_posts[:3]
 
    return render(request, 'blog_detail.html', {
        'post':          post,
        'reading_time':  post.reading_time,
        'related_posts': related_posts,
    })




def case_studies(request):
    cases = CaseStudy.objects.filter(is_published=True)
    return render(request, 'case_studies.html', {'cases': cases})


def case_study_detail(request, slug):
    case = get_object_or_404(CaseStudy, slug=slug, is_published=True)
    return render(request, 'case_study_detail.html', {'case': case})



def blog_subscribe(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()

        if email:

            if BlogSubscriber.objects.filter(email=email).exists():

                messages.error(
                    request,
                    "You're already subscribed."
                )

            else:

                ip_address = request.META.get("REMOTE_ADDR")
                user_agent = request.META.get("HTTP_USER_AGENT", "")

                BlogSubscriber.objects.create(
                    email=email,
                    ip_address=ip_address,
                    user_agent=user_agent
                )

                messages.success(
                    request,
                    "Subscribed successfully!"
                )

        else:

            messages.error(
                request,
                "Please enter a valid email."
            )

    return render(request, "blog.html")