from django.shortcuts import render, redirect
from .models import Task
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewUserForm
from django.contrib.auth import authenticate, login
from to_do_list.tasks import send_notification

def index(request):
    return render(request, 'landing/index.html')


def profile(request):
    return render(request, 'profile2.html')

class CustomLoginView(LoginView):
    template_name = 'to_do_list/signin.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')
    






class TaskList(LoginRequiredMixin, ListView):
    models = Task
    queryset = models.objects.all()
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input  
        return context 

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'to_do_list/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due', 'time']
    success_url = reverse_lazy('to_do_list:tasks')
      
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(TaskCreate, self).form_valid(form)
        # send_notification.delay()
        return response

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due', 'time']
    success_url = reverse_lazy('to_do_list:tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('to_do_list:tasks')

class RegisterPage(FormView):
    template_name = 'to_do_list/signup2.html'
    form_class = NewUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
           login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            
            return redirect('dashboard')
        return super(RegisterPage,self).get(*args,**kwargs)
