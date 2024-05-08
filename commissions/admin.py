from django.contrib import admin
from .models import Commission, Job, JobCommissionApplication

class JobInline(admin.TabularInline):
    model = Job

class CommissionAdmin(admin.ModelAdmin):
    exclude = ('openPersonnel',)
    inlines = [JobInline,]
    search_fields = ['title']
    list_display = ['title', 'status', 'made_at']
    list_filter = ['status', 'made_at']

    def save_model(self, request, obj, form, change):
        obj.author = request.user.profile
        super().save_model(request, obj, form, change)

class JobAdmin(admin.ModelAdmin):
    exclude = ['openPersonnel']
    search_fields = ['role', 'commission__title']
    list_display = ['role', 'commission', 'status', 'personnel_required']
    list_filter = ['commission__title', 'status']

class JobCommissionApplicationAdmin(admin.ModelAdmin):
    search_fields = ['job__role', 'applicant__username']
    list_display = ['job', 'applicant', 'status', 'applied_at']
    list_filter = ['job__role', 'status']

admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobCommissionApplication, JobCommissionApplicationAdmin)
