from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from formtools.wizard.views import SessionWizardView
from .models import Profile
from .forms import Step1Form, Step2Form, Step3Form, Step4Form, Step5Form, Step6Form 
from django.core.files.storage import default_storage

FORMS = [
    ("step1", Step1Form),
    ("step2", Step2Form),
    ("step3", Step3Form),
    ("step4", Step4Form),
    ("step5", Step5Form),
    ("step6", Step6Form),
]

TEMPLATES = {
    "step1": "bureau/form_step1.html",
    "step2": "bureau/form_step2.html",
    "step3": "bureau/form_step3.html",
    "step4": "bureau/form_step4.html",
    "step5": "bureau/form_step5.html",
    "step6": "bureau/form_step6.html",
}
class ProfileWizard(LoginRequiredMixin, SessionWizardView):
    form_list = FORMS
    file_storage = default_storage

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_instance(self, step):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Profile(user=self.request.user)

    def done(self, form_list, **kwargs):
        profile = self.get_form_instance(None)
        for form in form_list:
            for field, value in form.cleaned_data.items():
                setattr(profile, field, value)

        if not profile.form_no:
            profile.form_no = f"VB-{self.request.user.id:05d}"
        profile.save()

        messages.success(self.request, "Profile submitted successfully.")
        return redirect("thank_you")

@login_required
def redirect_after_login(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('user_form')

@login_required(login_url='login')
def admin_dashboard(request):
    query = request.GET.get("q", "")
    profiles = Profile.objects.all()

    if query:
        profiles = profiles.filter(
            Q(caste__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )

    return render(request, 'bureau/admin_dashboard.html', {
        'profiles': profiles,
        'query': query,
    })

def thank_you(request):
    return render(request, "thank_you.html")

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'bureau/profile_detail.html', {'profile': profile})
