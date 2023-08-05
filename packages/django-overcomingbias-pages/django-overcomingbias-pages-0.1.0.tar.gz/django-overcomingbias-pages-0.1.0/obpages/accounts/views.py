from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordContextMixin,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, TemplateView

from obpages.accounts.forms import CustomPasswordResetForm, RegisterForm

OBPAGES_AUTH_TEMPLATES_PATH = "obpages/accounts"


class ManageAccountView(TemplateView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/manage_account.html"
    extra_context = {"title": "Your Account"}

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/login.html"
    redirect_authenticated_user = True
    extra_context = {"title": "Log In"}

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        return self.request.user.get_absolute_url()


class CustomLogoutView(LogoutView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/logged_out.html"


class RedirectLoggedInUserMixin(PasswordContextMixin):
    """Mixin which redirects logged in users to their user page."""

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.request.user.get_absolute_url()
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(*args, **kwargs)


class CustomCreateView(RedirectLoggedInUserMixin, CreateView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/create.html"
    form_class = RegisterForm
    success_url = reverse_lazy("create_done")
    title = "Create Account"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateDoneView(RedirectLoggedInUserMixin, TemplateView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/create_done.html"
    title = "Account Created Successfully"


class CustomPasswordChangeView(PasswordChangeView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/password_change_form.html"


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/password_change_done.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/password_reset_form.html"
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/password_reset_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = f"{OBPAGES_AUTH_TEMPLATES_PATH}/password_reset_complete.html"
