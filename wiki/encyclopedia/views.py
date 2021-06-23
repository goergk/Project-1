from django.shortcuts import render
from . import util
import markdown2 

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

