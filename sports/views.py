from django.shortcuts import render
from .models import Sport, Slot, Booked_Slot, FeaturedMatch
from users.models import Member, Staff, Rating
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from courts.models import Court


# from django.utils.timezone import datetime


# Create your views here.
@login_required
def add_slot(request, pk):
    slot = Slot.objects.get(id=pk)
    member = Member.objects.get(user=request.user)
    booked_slot = Booked_Slot.objects.first()
    if len(member.slots.filter(date=datetime.date.today()).all()) >= 3:
        messages.success(request, f'You can book only 3 slots per day')
        return redirect('slots-home')
    member.slots.add(slot)
    booked_slot.slots.add(slot)
    messages.success(request, f'Slot Booked Successfully!')
    return redirect('slots-home')


@login_required
def remove_slot(request, pk):
    slot = Slot.objects.get(id=pk)
    member = Member.objects.get(user=request.user)
    booked_slot = Booked_Slot.objects.first()
    if member.slots.contains(slot):
        # If course is already present
        member.slots.remove(slot)
        booked_slot.slots.remove(slot)
        messages.success(request, f'Your slot has been cancelled successfully')
        return redirect('profile')


def home(request):
    all_slots = Booked_Slot.objects.first().slots.all()
    all_sports = Sport.objects.all()
    dict = {}
    dict_court = {}
    for sport in all_sports:
        count = 0
        temp = sport
        s = sport.name
        for slot in all_slots:
            if slot.sport == sport:
                count += 1
        dict.__setitem__(temp, count)
    trending_sport = max(dict, key=dict.get)

    all_courts = Court.objects.all()
    all_ratings = Rating.objects.all()

    for court in all_courts:
        rtg = 0
        no_of_ratings = 0
        temp_court = court
        for rating in all_ratings:
            if rating.court == court:
                no_of_ratings += 1
                rtg += rating.rating
        if no_of_ratings == 0:
            rtg = 0
        else:
            rtg = rtg / no_of_ratings
        dict_court.__setitem__(temp_court, rtg)
    rated_court=max(dict_court, key=dict_court.get)
    context = {
        'matches': FeaturedMatch.objects.all(),
        'staffs': Staff.objects.all(),
        'trending_sport': trending_sport,
        'rated_court':rated_court,
    }
    return render(request, 'sports/home.html', context)


def sports(request):
    context = {
        'sports': Sport.objects.all()
    }
    return render(request, 'sports/sports.html', context)


class SlotListView(ListView):
    model = Slot
    template_name = 'sports/slots.html'
    context_object_name = 'slots'
    extra_context = {'staffs': Staff.objects.all(), 'sports': Sport.objects.all(),
                     'booked_slots': Booked_Slot.objects.first(), 'today': datetime.date.today()}
    ordering = ['-date']


class BookedSlotListView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    model = Booked_Slot
    template_name = 'sports/bookedslots.html'
    context_object_name = 'slots_unused'
    extra_context = {'staffs': Staff.objects.all(), 'sports': Sport.objects.all(),
                     'booked_slots': Booked_Slot.objects.first(), 'today': datetime.date.today()}
    def test_func(self):
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False


class SportSlotListView(ListView):
    model = Slot
    template_name = 'sports/sport_slots.html'
    context_object_name = 'slots'
    extra_context = {'staffs': Staff.objects.all(), 'today': datetime.date.today()}

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
    extra_context = {'staffs': Staff.objects.all(), 'slots': Slot.objects.all(), 'today': datetime.date.today()}


class MatchCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FeaturedMatch
    fields = ['title', 'description']

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
    fields = ['title', 'description']

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
