from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from . import util
import random
import markdown2
from django.http import Http404

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def display_one(request,entry):
    markdown_content = util.get_entry(entry)
    if markdown_content:
        html_content = markdown2.markdown(markdown_content)
        return render(request,"encyclopedia/display.html",{
        "entry": html_content,
        "title":entry.capitalize()})
    else:
        raise Http404("Entry not Found")
def search(request):
    query = request.GET.get('q','')
    get_one = util.get_entry(query)
    if get_one:
        return HttpResponseRedirect(reverse('display_one',args=[query]))
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request,"encyclopedia/search.html",{'results': results, 'query': query})

def create_new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title):
            messages.error(request,f"{title} already exists!")
            return render(request,"encyclopedia/create.html",)
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('display_one',args=[title]))
    else:
        return render(request,"encyclopedia/create.html")

def edit_entry(request,entry):
    if request.method == 'POST':
        new_content = request.POST.get('content')
        util.save_entry(entry,new_content)
        return HttpResponseRedirect(reverse('display_one',args=[entry]))
    else:
        content  = util.get_entry(entry)
        return render(request,"encyclopedia/edit.html",{'entry':entry, 'content':content})
    
def random_page(request):
    entries = util.list_entries()
    random_page = random.choice(entries)
    return HttpResponseRedirect(reverse('display_one',args=[random_page]))

    