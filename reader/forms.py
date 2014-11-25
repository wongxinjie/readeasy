#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class LoginForm(forms.Form):
	username = forms.CharField(
		required = True,
		label = u"用户名",
		#error_messages = {"required", "请输入用户名"},
		widget = forms.TextInput(
			attrs = {
				"placeholder": u"用户名",
			}
		),
	)
	
	password = forms.CharField(
		required = True,
		label = u"密码",
		#error_messages = {"required", "请输入密码"},
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": u"密码",
			}
		),
	)

	def clean(self):
		if not self.is_valid():
			raise forms.ValidationError(u"用户名和密码为必填项")
		else:
			cleaned_data = super(LoginForm, self).clean()


class UserCreateForm(UserCreationForm):
	username = forms.CharField(
		required = True,
		label = u"用户名",
		widget = forms.TextInput(
			attrs = {
				"placeholder": u"字母、数字或者下划线",
			}
		),
	)

	email = forms.EmailField(
		required = False,
		label = u"邮箱",
		widget = forms.TextInput(
			attrs = {
				"placeholder": u"邮箱(非必须)",
			}
		),
	)

	password1 = forms.CharField(
		required = True,
		label = u"密码",
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": u"密码",
			}
		),
	)

	password2 = forms.CharField(
		required = True,
		label = u"密码(确认)",
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": u"密码(确认)",
			}
		),
	)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
	
	def clean(self):
		if not self.is_valid():
			raise forms.ValidationError(u"信息填写不正确")
		elif self.cleaned_data['password1'] <> self.cleaned_data['password2']:
			raise forms.ValidationError(u"密码不一致")
		else:
			cleaned_data = super(UserCreateForm, self).clean()
		return cleaned_data
			

class NoteForm(forms.Form):
	content = forms.CharField(
		required = True,
		widget = forms.Textarea(attrs={'cols': 67, 'rows': 20, 'style':'resize:none; overflow-y:auto'})
	)

	def clean(self):
		if not self.is_valid():
			raise forms.ValidationError(u"信息填写不正确-_-")
		else:
			cleaned_data = super(NoteForm, self).clean()
		return cleaned_data

