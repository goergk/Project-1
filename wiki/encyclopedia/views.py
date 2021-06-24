from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from . import util
import markdown2 
from django.urls import reverse
from django.shortcuts import redirect
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
        return redirect(reverse("encyclopedia:entry", kwargs={"title" : string}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if string.lower() in entry.lower():
                subStringEntries.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": subStringEntries
        })

def randomEntry(request):
    return redirect(reverse("encyclopedia:entry", kwargs={"title" : choice(util.list_entries())}))
