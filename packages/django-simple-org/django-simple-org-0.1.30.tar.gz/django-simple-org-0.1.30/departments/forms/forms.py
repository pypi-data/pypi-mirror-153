# -*- coding: utf-8 -*-
"""
@File        : forms.py
@Author      : yu wen yang
@Time        : 2022/5/5 5:38 下午
@Description :
"""
from django import forms


class DepartmentForms(forms.Form):
    name = forms.CharField(min_length=2, max_length=32)
    charger_id = forms.IntegerField(required=False)
    parent_id = forms.IntegerField(required=False)
    organization_id = forms.IntegerField()


class MoveDepartmentIndexForms(forms.Form):
    department_id = forms.IntegerField()
    type = forms.CharField(min_length=2, max_length=4)

