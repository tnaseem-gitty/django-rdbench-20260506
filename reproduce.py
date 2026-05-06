from django import forms
from django.forms import SelectDateWidget
from django.http import HttpResponse
from django.urls import path
from django.core.exceptions import ValidationError
from django.shortcuts import render

class ReproForm(forms.Form):
    my_date = forms.DateField(widget=SelectDateWidget())

def repro_view(request):
    form = ReproForm(request.GET)  # for ease of reproducibility
    if form.is_valid():
        return HttpResponse("ok")
    else:
        return HttpResponse("not ok")

urlpatterns = [path('repro/', repro_view, name='repro')]

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    import sys
    execute_from_command_line(sys.argv)
