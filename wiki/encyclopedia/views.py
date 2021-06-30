from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from . import util
import markdown2 
from django.urls import reverse
from random import choice
from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "header": "All Pages"
    })

def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(title)),
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": f"<h1>Page '{ title }' was not found</h1>",
            "title": "Page was not found"
        })

def searchEntry(request):
    string = request.GET['title']

    if util.get_entry(string):
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title" : string}))
    else:
        substringEntries = []
        for entry in util.list_entries():
            if string.lower() in entry.lower():
                substringEntries.append(entry)
        if len(substringEntries) > 0:
            return render(request, "encyclopedia/index.html", {
                "entries": substringEntries,
                "header": "Are you looking for:"
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": substringEntries,
                "header": "No matching results were found"
            })

def randomEntry(request):
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title" : choice(util.list_entries())}))

def newPage(request):
    return render(request, "encyclopedia/new.html", {
        "entry": NewEntryForm()
    })
