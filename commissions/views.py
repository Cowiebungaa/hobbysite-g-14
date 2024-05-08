from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Sum
from django.views.generic.edit import FormMixin
from django.forms import inlineformset_factory
from .models import Commission, Job, JobApplication
from .forms import JobCommissionForm, JobForm, JobCommissionApplicationForm


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions_list.html'
    ordering = ['made_at']
    

class CommissionDetailView(FormMixin, DetailView):
    model = Commission
    template_name = 'commission_detail.html'
    form_class = JobCommissionApplicationForm
    
    def get_success_url(self):
        return reverse('commissions:commission-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        total_personnel = commission.jobs.aggregate(total=Sum('personnel_required'))['total']
        context['has_jobs'] = commission.jobs.exists()
        context['total_personnel'] = total_personnel
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        commission = self.get_object()
        available_jobs = commission.jobs.all()
        kwargs['available_jobs'] = available_jobs
        kwargs['no_jobs'] = not self.object.jobs.exists()
        return kwargs

    def post(self, request, ai, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            job_application = JobApplication()
            job_application.job = form.cleaned_data.get('job')
            job_application.applicant = self.request.user.profile
            job_application.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commission_make.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_forms'] = CustomJobInlineFormSet(self.request.POST)
        else:
            context['job_forms'] = CustomJobInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_forms = context['job_forms']
        if job_forms.is_valid():
            self.object = form.save()
            job_forms.instance = self.object
            job_forms.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        return {'author': self.request.user.profile}

    def get_success_url(self):
        return reverse_lazy('commissions:commission-detail', kwargs={'ai': self.object.ai})


class CustomCommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CustomCommissionForm
    template_name = 'custom_commissions_update.html'

    def get_success_url(self):
        return reverse_lazy('commissions:commission-detail', kwargs={'ai': self.object.ai})


JobInlineFormSet = inlineformset_factory(
    Commission, Job, form=CustomJobForm, extra=3, can_delete=True
)
