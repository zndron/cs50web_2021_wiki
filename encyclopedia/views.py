from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.template import loader

from . import util

import random, markdown2


class EntryForm(forms.Form):
    name = forms.CharField(label="Назва статті", widget=forms.TextInput(attrs={'class':'form-control', 'required': True}))
    content = forms.CharField(label="Текст статті", widget=forms.Textarea(attrs={'class':'form-control', 'required': True}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view(request, name):
    content = util.get_html_entry(name)

    if content == None:
        template = loader.get_template('encyclopedia/error.html')
        return HttpResponseNotFound(template.render({
            'content': 'Такої статті не існує, ви можете створити таку статтю.'
        }, request))
        
    return render(request, "encyclopedia/view.html", {
        "name": name,
        "content": content
    })

def edit(request, name):
    content = util.get_entry(name)

    if content == None:
        template = loader.get_template('encyclopedia/error.html')
        return HttpResponseNotFound(template.render({
            'content': 'Такої статті не існує, ви можете створити таку статтю.'
        }, request))

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():    
            formData = form.cleaned_data

            title = name
            content = formData["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse('encyclopedia:view', args=[name]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "name": name,
                "form": form
            })

    form = EntryForm({'name': name, 'content': content})
    form.fields['name'].widget = forms.HiddenInput()

    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "form": form
    })


def add(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data

            title = formData["name"]
            content = formData["content"]

            entries = util.list_entries()
            for i in range(len(entries)):
                entries[i] = entries[i].lower()

            if title.lower() not in entries:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('encyclopedia:view', args=[title]))
            else:            
                form.add_error('name', 'Стаття з такою назвою вже існує.')
                return render(request, "encyclopedia/add.html", {
                    "form": form
                })
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": EntryForm()
    })

def search(request):
    if request.method == "POST":
        query = request.POST['q']

        content = util.get_entry(query)
        entries = util.search(query)

        if content:
            return HttpResponseRedirect(reverse('encyclopedia:view', args=[query]))

        return render(request, "encyclopedia/search.html", {
            'query': query,
            'entries': entries
        })

    return render(request, "encyclopedia/search.html", {
            'query': '',
            'entries': []
        })

def random_page(request):
    list = util.list_entries()
    title = random.choice(list)

    return HttpResponseRedirect(reverse('encyclopedia:view', args=[title]))
