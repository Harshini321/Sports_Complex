from django.shortcuts import render,redirect
from .models import Court,UserComment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Staff
from sports.models import Slot
from users.models import Rating
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
    extra_context = {'staffs': Staff.objects.all(), 'slots': Slot.objects.all(), 'ratings': Rating.objects.all()}


class CourtDetailView(DetailView):
    model = Court
    context_object_name = 'court'
    extra_context = {'staffs': Staff.objects.all(), 'slots': Slot.objects.all(), 'ratings': Rating.objects.all(),'comments':UserComment.objects.all()}


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

@login_required
def postComment(request,pk):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=User.objects.get(username=request.user)
        court=Court.objects.get(id=pk)
        parentsno=request.POST.get('parentsno')
        if parentsno == '':
            comment=UserComment(comment=comment,user=user,court=court)
            comment.save()
            messages.success(request,"Your comment has been posted successfully!")
        else:
            parent=UserComment.objects.get(sno=parentsno)
            comment=UserComment(comment=comment,user=user,court=court,parent=parent)
            comment.save()
            messages.success(request,"Your reply has been posted successfully!")
    return redirect(f'/courts/{court.pk}')