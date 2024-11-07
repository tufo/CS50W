from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# tasks = [] # define global variable, which any stranger could access; use sessions to circumvent this problem.

# Create a custom class.
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

# Create your views here.
def index(request):
    if "tasks" not in request.session: # instead of defining a global variable,  look inside the session to see if tasks exists already.
        request.session["tasks"] = []  # create tasks as an empty list.
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"] # Paradigm: LHS is the key; RHS is the variable containing values.
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST) # create a form varable by taking all the data in the variable and filling NewTaskForm.
        if form.is_valid():
            task = form.cleaned_data["task"]
            # tasks.append(task) # add this task to the list of tasks.
            request.session["tasks"] += [task] # use this as a different way to append.

            return HttpResponseRedirect(reverse("tasks:index")) # figure out the URL and then redirect; need to import.
        else:
            return render(request, "tasks/add.html", {
                "form": form # choose to re-render and send back the existing form data to the user.
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm() # render an empty form.
    })