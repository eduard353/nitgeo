from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View, CreateView, DetailView, UpdateView

from .forms import RegisterForm, LoginForm, ReactivationForm, ResetPasswordForm, PasswordSetForm, ProfileForm
from .models import ActivationToken, PasswordResetToken, Profile
from .utils import send_activation_email, send_password_reset_email

User = get_user_model()


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user_token = ActivationToken.objects.create(user=user)

        send_activation_email(user, user_token, self.request)
        messages.success(self.request, 'You have to activate your account')
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['form_errors'] = form.errors
        return self.render_to_response(context)


class ActivateAccountView(View):
    def get(self, request, username, token):
        user = get_object_or_404(User, username=username)
        token = get_object_or_404(ActivationToken, token=token, user=user)

        if user.is_active:
            messages.error(request, 'User is already activated')
            return redirect('accounts:login')

        if token.verify_token():
            user.is_active = True
            token.delete()
            user.save()

            messages.success(request, 'Activation complete')
            return redirect('accounts:login')

        messages.error(request, 'Token expired')
        return redirect('accounts:login')


class PasswordSetView(View):
    def get(self, request, username, token):
        user = get_object_or_404(User, username=username)
        token = get_object_or_404(PasswordResetToken, token=token, user=user)
        form = PasswordSetForm(user)
        return render(request, 'accounts/set_password.html', {'form': form})

    def post(self, request, username, token):
        user = get_object_or_404(User, username=username)
        token = get_object_or_404(PasswordResetToken, token=token, user=user)
        form = PasswordSetForm(user, data=request.POST)

        if form.is_valid():
            form.save()
            token.delete()
            messages.success(self.request, 'Your password has been updated.')
            return redirect('accounts:login')

        form_errors = form.errors
        form.clean()
        return render(request, 'accounts/set_password.html', {'form': form, 'form_errors': form_errors})


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('nitmap:home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        return redirect('accounts:login')

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        username = form.cleaned_data['username']

        user = User.objects.filter(username=username)
        if user.exists():
            user = user.first()
            if not user.is_active:
                messages.error(self.request, 'Activate yor account')
                return redirect('accounts:login')

        context['non_field_errors'] = form.non_field_errors()
        return self.render_to_response(context)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class ReactivationSentView(FormView):
    template_name = 'accounts/reactivate_token.html'
    form_class = ReactivationForm
    success_url = reverse_lazy('accounts:reactivation_sent')

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data['email'])

        if user.is_active:
            messages.warning(self.request, 'This account is already active.')
            return redirect('accounts:login')

        token = user.activation_token
        token.delete()
        new_token = ActivationToken.objects.create(user=user)
        send_activation_email(user, new_token, self.request)

        messages.success(self.request, 'Activation email has been sent. Please check your email')
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['form_errors'] = form.errors
        return self.render_to_response(context)


class PasswordResetSentView(FormView):
    template_name = 'accounts/reset_password_token.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_sent')

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data['email'])

        if not user.is_active:
            messages.warning(self.request, 'This account is not active.')
            return redirect('accounts:login')

        token = PasswordResetToken.objects.filter(user=user).first()
        if token is not None:
            token.delete()
        new_token = PasswordResetToken.objects.create(user=user)
        send_password_reset_email(user, new_token, self.request)

        messages.success(self.request, 'Password reset email has been sent. Please check your email')
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['form_errors'] = form.errors
        return self.render_to_response(context)


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile/create.html'
    success_url = reverse_lazy('inforium:customers_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['form_errors'] = form.errors
        return self.render_to_response(context)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        profile = self.get_object()
        context['profile'] = profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user__username=self.kwargs['username'])

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        form_errors = form.errors
        return self.render_to_response(self.get_context_data(form=form, form_errors=form_errors))

    def get_success_url(self):
        profile = self.get_object()
        return reverse_lazy('accounts:profile_detail', kwargs={'username': profile.user.username})

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user != profile.user:
            raise PermissionDenied('You are not allowed to edit profile')
        return super().dispatch(request, *args, **kwargs)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile/update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user__username=self.kwargs['username'])

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        form_errors = form.errors
        return self.render_to_response(self.get_context_data(form=form, form_errors=form_errors))

    def get_success_url(self):
        profile = self.get_object()
        return reverse_lazy('accounts:profile_detail', kwargs={'username': profile.user.username})

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user != profile.user:
            raise PermissionDenied("You are not allowed to edit this profile")
        return super().dispatch(request, *args, **kwargs)


class FollowView(LoginRequiredMixin, View):
    def get(self, request, username):
        pass


class UnfollowView(LoginRequiredMixin, View):
    pass
