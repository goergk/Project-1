from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from . import util
import markdown2 
from django.urls import reverse
from random import choice
from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'title_area'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'content_area'}))

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'content_area'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "header": "All Pages"
    })

def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(title)),
            "title": title,
            "exists": True
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": f"<h1>Page '{ title }' was not found</h1>",
            "title": "Page was not found",
            "exists": False
        })

def searchPage(request):
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

def randomPage(request):
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title" : choice(util.list_entries())}))

def newPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            if util.get_entry(form.cleaned_data["title"]) is not None:
                return render(request, "encyclopedia/new.html", {
                    "new": False,
                    "title": form.cleaned_data["title"],
                    "entry": form
                })
            else:    
                util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title" : form.cleaned_data["title"]}))
        else:
            return render(request, "encyclopedia/new.html", {
                "new": True,
                "title": '',
                "entry": form
            })
    return render(request, "encyclopedia/new.html", {
        "new": True,
        "title": '',
        "entry": NewEntryForm()
    })

def editPage(request, title):
    if util.get_entry(title) is not None:
        if request.method == "POST":
            form = EditEntryForm(request.POST)
            if form.is_valid():
                util.save_entry(title, bytes(form.cleaned_data["content"], 'utf8'))
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title" : title}))
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title),
            "entry": EditEntryForm(initial={'content':util.get_entry(title)}),
            "exists": True
        })
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "exists": False
        })


