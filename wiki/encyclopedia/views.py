from django.shortcuts import render, redirect

from . import util

from django import forms
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files.storage import default_storage

import random
import markdown2
from markdown2 import Markdown


#[Using Markdown2 with Django](https://stackoverflow.com/questions/62855513/using-markdown2-with-django)

"""
# Create a custom class.
class SearchForm(forms.Form):
    query = forms.CharField(label="search") # important that the label assignment is correct.

class MyForm(forms.Form):
    # define all of the input fields i want this form to have.
    new_title_ = forms.CharField(label="new title")
    new_body_ = forms.CharField(label="new body")
"""

def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })

def pull(request, title_):
    title_URL = "wiki/"+title_
    md_text = util.get_entry(title_)
    if md_text == None:
        html_text = "The requested page was not found."
    else: 
        html_text = markdown2.markdown(md_text)
    return render(request, "encyclopedia/title.html", {
        "content": html_text,
        "page_title": title_
    })


def search(request):
    
    query = request.GET.get('q')
    listed_entries = util.list_entries()
    array = []
    alert = ""
    for n in range(len(listed_entries)):
        # if perfect match...
        if query.upper() == listed_entries[n].upper():
            return redirect('title__', title_ = query)

        # if partial match...
        if query.upper() in listed_entries[n].upper():
            array.append(listed_entries[n])

    if array == []:
        alert = "None found."

    return render(request, "encyclopedia/query.html", {
        "close_matches": array,
        "alert_": alert
    })


def create(request):
    if request.method == "POST":

        #if my_form.is_valid():
        #new_title = my_form.cleaned_data["new_title"]
        #new_body = my_form.cleaned_data["new_body_"]

        # extract form data and write to my_form
        my_form = request.POST

        # extract new_title string from my_form
        new_title_ = my_form["new_title"]

        # extract body text from my_form
        new_body_ = my_form["new_body"]

        # check that .md file doesn't already exist
        listed_entries = util.list_entries()
        for n in range(len(listed_entries)):
            if new_title_.upper() == listed_entries[n].upper():
                return HttpResponse("Title already exists.")
        
        # concatenate directory name
        new_path_ = "entries/" + new_title_ + ".md"

        # create new file, give it file name, populate with data.
        """
        with default_storage.open(new_path_,'w') as f:
            f.write(new_body_)
        """
        # use the provided util function to save.
        util.save_entry(updating_title_, updated_body_)

    return render(request, "encyclopedia/new_page.html")


def random_article(request):
    entries_list = util.list_entries()
    article_cnt = len(entries_list)
    random_int = random.randint(0,article_cnt-1)
    random_article = entries_list[random_int]
    return redirect('title__', title_ = random_article)

def editor(request):

    # the user is accessing this function by clicking 'edit' from a wiki entry.
    # that wiki entry used POST to pass its title in a hidden input.
    if request.method == "POST":
        my_form = request.POST
        title_ = my_form["editor_title"]
    
    # use the title to pull the markdown content.
    md_text = util.get_entry(title_)

    # render edit_page and populate the text area with the pre-existing content.
    return render(request, "encyclopedia/edit_page.html", {
        "editor_title": title_,
        "md_body": md_text
    })



# This will write the updated markdown text to the .md file.
# Then, it will redirect back to the wiki entry page.
def update(request):

    if request.method == "POST":
        my_form = request.POST
        updating_title_ = my_form["updating_title"]

        # grab the edited markdown data using post
        updated_body_ = my_form["new_body"]

        # concatenate directory name
        path_ = "entries/" + updating_title_ + ".md"

        # open file, write with updated content.
        """
        with default_storage.open(path_,'w') as f:
            f.write(updated_body_)
        """
        # use the provided util function to save.
        util.save_entry(updating_title_, updated_body_)

    # redirect to the title url.
    return redirect('title__', title_ = updating_title_)

