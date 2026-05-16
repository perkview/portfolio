from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(About)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(CoreValue)
admin.site.register(SkillsHeader)
admin.site.register(TechnicalSkill)
admin.site.register(Tool)
admin.site.register(SoftSkill)
admin.site.register(SummarySkill)
admin.site.register(Project)
admin.site.register(Testimonial)
admin.site.register(ContactInfo)
admin.site.register(BasicInfo)
admin.site.register(Technologies)
admin.site.register(Service)
admin.site.register(ServicePackage)
admin.site.register(PackageFeature)
admin.site.register(FreelanceStatus)
admin.site.register(FAQ)
admin.site.register(BlogPost)
admin.site.register(ProjectInquiry)
admin.site.register(CaseStudy)
admin.site.register(AboutStat)
admin.site.register(AboutCTA)
admin.site.register(BlogSubscriber)



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'project_type',
        'budget',
        'status',
        'priority',
        'is_read',
        'is_resolved',
        'created_at',
    )

    list_filter = (
        'status',
        'priority',
        'project_type',
        'is_read',
        'is_resolved',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'subject',
        'message',
        'company',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'ip_address',
        'user_agent',
    )

    ordering = ('-created_at',)