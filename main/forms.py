# -*- encoding: utf-8 -*-
from django import forms


class PerfumeForm(forms.Form):
    id = forms.CharField(label='Perfume ID (3-6)')
