from django.shortcuts import render
from .models import Sport, Slot, Booked_Slot,FeaturedMatch
from users.models import Member, Staff
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime


# Create your views here.
@login_required
def add_slot(request, pk):
    slot = Slot.objects.get(id=pk)
    member = Member.objects.get(user=request.user)
    if len(member.slots.filter(date=datetime.date.today()).all()) >= 3:
        # If course is already present
        messages.success(request, f'You can book only 3 slots per day')
        return redirect('slots-home')
    member.slots.add(slot)
    messages.success(request, f'Slot Booked Successfully!')
    return redirect('slots-home')


@login_required
def remove_slot(request, pk):
    slot = Slot.objects.get(id=pk)
    member = Member.objects.get(user=request.user)
    if member.slots.contains(slot):
        # If course is already present
        member.slots.remove(slot)
        messages.success(request, f'Your slot has been cancelled successfully')
        return redirect('profile')


def home(request):
    context={
        'matches':FeaturedMatch.objects.all(),
        'staffs': Staff.objects.all()
    }
    return render(request, 'sports/home.html',context)


def sports(request):
    context = {
        'sports': Sport.objects.all()
    }
    return render(request, 'sports/sports.html', context)

class SlotListView(ListView):
    model = Slot
    template_name = 'sports/slots.html'
    context_object_name = 'slots'
    extra_context = {'staffs': Staff.objects.all(), 'sports': Sport.objects.all()}
    ordering = ['-date']


class SportSlotListView(ListView):
    model = Slot
    template_name = 'sports/sport_slots.html'
    context_object_name = 'slots'
    extra_context = {'staffs': Staff.objects.all()}

    def get_queryset(self):
        sport = get_object_or_404(Sport, name=self.kwargs.get('name'))
        return Slot.objects.filter(sport=sport).order_by('-date')


class SportListView(ListView):
    model = Sport
    template_name = 'sports/sports.html'
    context_object_name = 'sports'
    extra_context = {'staffs': Staff.objects.all(), 'slots': Slot.objects.all()}


class SlotDetailView(DetailView):
    model = Slot
    context_object_name = 'slot'
    extra_context = {'staffs': Staff.objects.all(), 'slots': Slot.objects.all()}


class SportDetailView(DetailView):
    model = Sport
    context_object_name = 'sport'
    extra_context = {'staffs': Staff.objects.all(), 'slots': Slot.objects.all()}



class MatchCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=FeaturedMatch
    fields=['title','description']

    def test_func(self):
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False

class SlotCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Slot
    fields = ['sport', 'court', 'date', 'start_time', 'end_time']

    def test_func(self):
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False


class SportCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Sport
    fields = ['name', 'courts']

    def test_func(self):
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False

class MatchUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeaturedMatch
    fields = ['title','description']

    def test_func(self):
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False


class SlotUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Slot
    fields = ['sport', 'court', 'date', 'start_time', 'end_time']

    def test_func(self):
        slot = self.get_object()
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False


class SportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sport
    fields = ['name', 'courts']

    def test_func(self):
        sport = self.get_object()
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False

class MatchDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FeaturedMatch
    context_object_name = 'match'
    success_url = '/'

    def test_func(self):
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False



class SlotDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Slot
    context_object_name = 'slot'
    success_url = '/slots'

    def test_func(self):
        slot = self.get_object()
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False


class SportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Sport
    context_object_name = 'sport'
    success_url = '/sports'

    def test_func(self):
        sport = self.get_object()
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False

