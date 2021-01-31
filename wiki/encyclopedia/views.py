from django import forms

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
import markdown2
import secrets

from . import util

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="New Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    entry = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-lg-10'}), label="Entry:")
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            entry_title = form.cleaned_data["entry_title"]
            if(util.get_entry(entry_title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(entry_title,entry)
                return HttpResponseRedirect(reverse("wiki:entry", kwargs={'entry': entry_title}))
            else:
                return render(request, "encyclopedia/pagealreadyExist.html", {
            "entry_title": entry})
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })


    return render(request, "encyclopedia/create.html", {
        "form" : NewEntryForm()
    })

def entry(request, entry): 
    md = markdown2.Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/pagedonotExist.html", {
            "entry_title": entry})
         
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": md.convert(entryPage),
            "entry_title": entry
        })

def random(request):
    entries = util.list_entries()
    rndmEntry1 = secrets.choice(entries)
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={'entry': rndmEntry1}))

def search(request):
    query = request.GET.get('q','')
    if(util.get_entry(query) is not None):
        return HttpResponseRedirect(reverse("wiki:entry", kwargs={'entry': query}))

    else:
        upperEntries = []
        for entry in util.list_entries():
            if query.upper() in entry.upper():
                upperEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
        "entries": upperEntries,
        "search": True,
        "query": query
    })
  
def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/pagedonotExist.html", {
            "entry_title": entry
        })
    else:
        form = NewEntryForm()
        form.fields["entry_title"].initial = entry     
        form.fields["entry_title"].widget = forms.HiddenInput()
        form.fields["entry"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/create.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entry_title": form.fields["entry_title"].initial
        })        
              


    