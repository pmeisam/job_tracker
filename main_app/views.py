from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Job, Column


# Define the home view
def home(request):
    return render(request, 'home.html')


# Define the about view
def about(request):
    return render(request, 'about.html')


# Define the signup view
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid credentials - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def jobs_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'index/detail.html', {'job': job})


# @login_required
class JobList(ListView):
    # model = Job
    # queryset = Job.objects.filter(user_id='1')
    # queryset = Job.objects.order_by('-created_at')
    def get_queryset(self):
        return Job.objects.filter(user_id=self.request.user.id)
    context_object_name = 'jobs'
    template_name = 'index/index.html'


# @login_required
class JobCreate(CreateView):
    model = Job
    fields = "__all__"
    # fields = ["name", "description"]
    template_name = 'index/job_form.html'
    success_url = '/jobs/'


class JobUpdate(UpdateView):
  model = Job
  template_name = 'index/job_form.html'
  fields = ['company_name', 'description']


class JobDelete(DeleteView):
  model = Job
  template_name = 'index/confirm_delete.html'
  success_url = '/jobs/'


class ColumnCreate(CreateView):
    model = Column
    fields = ['name']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    template_name = 'index/job_form.html'
    success_url = '/jobs/'