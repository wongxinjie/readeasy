#-*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from models import Category, Author, Book, Content

class BookAdmin(admin.ModelAdmin):
	list_display = ['caption', 'isbn', 'id']
	list_filter = ['caption' ]
	ordering = ['-id']
	filter_horizontal = ('authors', 'categories')


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Content)

