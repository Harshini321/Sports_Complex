from django.shortcuts import render
from .models import Court
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Staff

# Create your views here.
def courts(request):
    context = {
        'courts': Court.objects.all()
    }
    return render(request, 'courts/courts.html', context)


class CourtListView(ListView):
    model = Court
    template_name = 'courts/courts.html'
    context_object_name = 'courts'
    extra_context = {'staffs': Staff.objects.all()}


class CourtDetailView(DetailView):
    model = Court
    context_object_name = 'court'


class CourtCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Court
    fields = ['name', 'capacity']

    def test_func(self):
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False


class CourtUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Court
    fields = ['name', 'capacity']

    def test_func(self):
        slot = self.get_object()
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False


class CourtDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Court
    context_object_name = 'court'
    success_url = '/courts'

    def test_func(self):
        slot = self.get_object()
        if self.request.user.email.startswith('staff') or self.request.user.is_superuser:
            return True
        return False
