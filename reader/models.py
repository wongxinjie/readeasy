#-*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink


class Category(models.Model):
	name = models.CharField(max_length=50, unique=True,  verbose_name=u'分类')
	
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['-id']
		verbose_name_plural = verbose_name = u'分类'


class Author(models.Model):
	name = models.CharField(max_length=50, verbose_name=u'作者')
	brief_desc = models.TextField(verbose_name=u'简介')

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name_plural = verbose_name = u'作者'


class Book(models.Model):
	caption = models.CharField(max_length=50, verbose_name=u'标题')
	isbn = models.CharField(max_length=13, unique=True, verbose_name=u'ISBN')
	authors = models.ManyToManyField(Author, verbose_name=u'作者')
	categories = models.ManyToManyField(Category, verbose_name=u'分类') 
	brief_desc = models.TextField(verbose_name=u'简介')
	
	def __unicode__(self):
		return u'%s %s' % (self.caption, self.isbn)

	class Meta:
		get_latest_by = '-id'
		ordering = ['-id']
		verbose_name_plural = verbose_name = u'图书'

		
class Content(models.Model):
	title = models.CharField(max_length=50, verbose_name=u'标题')
	book = models.ForeignKey(Book, verbose_name=u'图书')
        content = models.TextField(verbose_name=u'内容')
		
	def __unicode__(self):
		return self.title
	class Meta:
		get_latest_by = 'id'
		ordering = ['id']
		verbose_name_plural = verbose_name  = u'章节内容'

class CollectionItem(models.Model):
	user_num = models.IntegerField(null=True)
	book = models.ForeignKey(Book)
	dis_collect = models.BooleanField(default=False)
	add_date = models.DateTimeField(auto_now_add = True)
	
	class Meta:
		get_latest_by = 'add_date'
		ordering = ['-add_date']


class BookmarkItem(models.Model):
	user_num = models.IntegerField(null=True)
	content = models.ForeignKey(Content)
	dis_add = models.BooleanField(default=False)
	add_time = models.DateTimeField(auto_now_add = True)
	
	class Meta:
		get_latest_by = 'add_time'
		ordering = ['-add_time']

class NoteItem(models.Model):
	user_num = models.IntegerField(null = True)
	content = models.ForeignKey(Content)
	dis_add = models.BooleanField(default=False)
	text_content = models.TextField()
	edit_time = models.DateTimeField(auto_now_add = True)
	
	class Meta:
		get_latest_by = 'edit_time'
		ordering = ['-edit_time']



