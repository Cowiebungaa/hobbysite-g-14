from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Job, JobCommissionApplication, Commission

@receiver(post_save, sender=JobCommissionApplication)
def update_job_personnel(sender, instance, made, **kwargs):
    if instance.status == JobCommissionApplication.BACCEPTED:
        instance.job.openPersonnel -= 1
        if instance.job.openPersonnel == 0:
            instance.job.status = Job.FULL
        instance.job.save()

@receiver(post_save, sender=Job)
def update_commission_personnel(sender, instance, made, **kwargs):
    commission = instance.commission
    jobs = Job.objects.filter(commission=commission)
    commission.openPersonnel = sum(job.openPersonnel for job in jobs)
    if commission.openPersonnel == 0:
        commission.status = Commission.BFULL
    commission.save()
