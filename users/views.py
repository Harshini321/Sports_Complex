from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, RateForm,RateUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Member, Rating
import datetime
from courts.models import Court
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template import loader


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! U are now able to login')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'member': Member.objects.filter(user=request.user).first(),
        'date': datetime.date.today()
    }
    return render(request, 'users/profile.html', context)


def update_rating(request, pk):
    court = Court.objects.get(id=pk)
    if request.method == 'POST':
        form = RateUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Rating has been edited!')
            return redirect('courts-detail', pk=pk)
    else:
        form = RateUpdateForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'users/rating.html', context)


@login_required
def rating(request, pk):
    court = Court.objects.get(id=pk)
    member = request.user
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.member = member
            rate.court = court
            rate.save()
            return redirect('courts-detail', pk=pk)
    else:
        form = RateForm()

    court_rating = Rating.objects.filter(court=court)
    existing_rating = Rating.objects.filter(court=court, member=member)
    final_rating = 0
    for rtg in court_rating:
        final_rating += rtg.rating
    if len(court_rating) != 0:
        final_rating = final_rating / len(court_rating)
    else:
        final_rating = 'Be the first one to Rate!'
    context = {
        'form': form,
        'court': court,
        'final_rating': final_rating,
        'existing_rating': existing_rating,
        'court_ratings': court_rating
    }
    return render(request, 'users/rating.html', context)

# class RatingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Rating
#     fields = ['rating']
#
#     def form_valid(self, form):
#         form.instance.member = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         rtg = self.get_object()
#         print(rtg)
#         print(rtg.member)
#         print(self.request.user)
#         if self.request.user != rtg.member:
#             return True
#         return False
