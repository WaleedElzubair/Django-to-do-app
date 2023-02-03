from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView , FormView
from . models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


# By default the ListView Looks for a template with the modelName_list.html 
# This can be overridden by setting the “template_name” attribute.
# template_name = Location/name of the html.

# context_object_name: Override the default queryset name of “object_list” 
# by setting the “context_object_name” attribute. 
# It helps to have a more user friendly name to work with besides just “object_list”.

# paginate_by & ordering: The list view also has pagination and ordering already built in. 
# We can set these methods by setting their attributes like I did in the code example above.


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user= self.request.user)
        context['count'] = context['tasks'].filter(complete= False).count()
        
        search_input = self.request.GET.get("search-area") or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains = search_input )
        context['search_input'] = search_input
        return context 



# By default the DetailView looks for a template with the modelName_detail.html 
# This can be overridden by setting the “template_name” attribute.
# template_name = Location/name of the html.

# context_object_name: Override the default queryset name of “object” 
# by setting the “context_object_name” attribute. 

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'



# By default the CreateView looks for a template with the modelName_form.html 
# This can be overridden by setting the “template_name” attribute.
# template_name = Location/name of the html.
# By default this view creates a model form for us based on the model we specify 
# We can use our own model form by creating a model form and setting the “form_class attribute”. 
# form_class = ModelForm name

# context_object_name: Override the default queryset name of “object” 
# by setting the “context_object_name” attribute. 

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title' , 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

# By default the UpdateView looks for a template with the modelName_form.html 
# This can be overridden by setting the “template_name” attribute.
# template_name = Location/name of the html.

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields =  ['title' , 'description', 'complete']
    success_url = reverse_lazy('tasks')


# By default the DeleteView looks for a template with the modelName_confirm_delete.html 
# This can be overridden by setting the “template_name” attribute.
# template_name = Location/name of the html.

# context_object_name: Override the default queryset name of “object2” 
# by setting the “context_object_name” attribute. 
# It helps to have a more user friendly name to work with besides just “object_list”.

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task_delete.html'
    success_url = reverse_lazy('tasks') 