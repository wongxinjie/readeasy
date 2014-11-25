#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.db.models import Q
from django.forms.formsets import formset_factory

from django import forms
from django.contrib.auth.forms import UserCreationForm

from bootstrap_toolkit.widgets import BootstrapUneditableInput
from models import Book, Category, Author, Content, CollectionItem, BookmarkItem, NoteItem 
from forms import LoginForm, UserCreateForm, NoteForm
from items import Collection, Bookmark, Note
from book_info import BookInfo

def book_list(request):
	book_list = Book.objects.all()
	categories = Category.objects.all()	

	return render_to_response("book_list.html", {"book_list": book_list, "categories": categories}, RequestContext(request, ))

def book_show(request, id=''):
	try:
		book = Book.objects.get(id=id)
		categories = Category.objects.all()
		content_list = book.content_set.all()
		if book.isbn in request.session:
			bookInfo = request.session.get(book.isbn)
		else:
			bookInfo = BookInfo(book.isbn)
			bookInfo.get_book_info()
			request.session[book.isbn] = bookInfo
	except Book.DoesNotExist:
		raise Http404
	return render_to_response("book_show.html", {"book": book, "categories": categories, "content_list": content_list, "book_info":bookInfo}, RequestContext(request, ))


def read_page(request, id=''):
	try:
		content = Content.objects.get(id=id)
	except Content.DoesNotExist:
		raise Http404
	if request.user.is_authenticated():
		form = NoteForm()
		return render_to_response("read_page.html", {"content": content}, RequestContext(request, {"form": form, }))
	else:
		return render_to_response("read_page.html", {"content": content}, RequestContext(request, ))


def read(request, id=''):
	try:
		book = Book.objects.get(id=id)
		content = book.content_set.all()[0]
	except Book.DoesNotExist:
		raise Http404
	return HttpResponseRedirect("/book/chapter/%d/" % (content.id))
	

def get_next_content(request, id=''):
	try:
		content = Content.objects.get(id=id)
		book = Book.objects.get(id=content.book.id)
		content_list = list(book.content_set.all().order_by('id'))
		next_content_num = content_list.index(content)+1
		if next_content_num < len(content_list):
			next_content = content_list[next_content_num]
		else:
			next_content = content_list[0]
	except Content.DoesNotExist:
		raise Http404
	
	return HttpResponseRedirect("/book/chapter/%d/" % (next_content.id))

def get_content_list(request, id=''):
	try:
		content = Content.objects.get(id=id)
		book = Book.objects.get(id=content.book.id)
		content_list = book.content_set.all()
	except Content.DoesNotExist:
		raise Http404

	return render_to_response("content_list.html", {"book": book, "content_list": content_list}, RequestContext(request, ))

def category(request, id=''):
	cut_category = Category.objects.get(id=id)
	book_list = cut_category.book_set.all()
	categories = Category.objects.all()
	return render_to_response("book_list.html", {"book_list": book_list, "categories": categories}, RequestContext(request, ))

def author(request, id=''):
	cut_author = Author.objects.get(id=id)
	book_list = cut_author.book_set.all()
	categories = Category.objects.all()
	return render_to_response("author.html", {"book_list": book_list, "author": cut_author, "categories": categories}, RequestContext(request, ))


def search(request):
	query = request.GET.get('title', '')
	if query:
		query_set = (
			Q(caption__icontains = query)|
			Q(isbn__iexact = query))
		book_list = Book.objects.filter(query_set).distinct()
	else:
		book_list = []
	
	categories = Category.objects.all()
	return render_to_response("book_list.html", {"book_list": book_list, "categories": categories}, RequestContext(request, ))


def user_login(request):

	if request.method == 'GET':
		form = LoginForm()
		return render_to_response("login.html", RequestContext(request, {"form": form, }))
	else:
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user = authenticate(username = username, password = password)
			if user is not None and user.is_active:
				login(request, user)
				request.session['username'] = username
				return HttpResponseRedirect("/")
			else:
				return render_to_response("login.html", RequestContext(request, {"form": form, "password_is_wrong": True}))
		else:
			return render_to_response("login.html", RequestContext(request, {"form": form, }))



def register(request):
	if request.method == 'GET':
		form = UserCreateForm()
		return render_to_response("register.html", RequestContext(request, {"form": form, }))
	else:
		form = UserCreateForm(request.POST)
		if form.is_valid():
			username = form.clean_username()
			password = form.clean_password2()
			
			form.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect("/")
		else:
			return render_to_response("register.html", RequestContext(request, {"form": form, "account_error": True }))
	 
	


@login_required(login_url='/user/login/')
def user_logout(request):
	logout(request)
	try:
		del request.session['username']
	except KeyError:
		pass
	return HttpResponseRedirect("/")


@login_required(login_url='/user/login/')
def take_note(request, id=''):
	content = Content.objects.get(id=id)
	user_num = request.user.id
	if request.method == 'CET':
		form = NoteForm()
		return render_to_responsen("read_page.html", {"content": content}, RequestContext(request, {"form": form, }))
	else:
		form = NoteForm(request.POST)
		if form.is_valid():
			clean_data = form.clean()
			text_content = clean_data['content']
			note = Note()
			note.add_note(user_num, content, text_content)
			return HttpResponseRedirect("/book/chapter/%d/" % (content.id))
		else:
			return render_to_response("read_page.html", {"content": content}, RequestContext(request, {"form": form, }))

@login_required(login_url='/user/login/')
def delete_note(request, id=''):
	content = Content.objects.get(id=id)
	user_num = request.user.id
	note = Note()
	note.remove_note(user_num, content)
	note_list = note.get_user_note(user_num)
	return HttpResponseRedirect("/user/note/")

@login_required(login_url='/user/login/')
def view_note(request):
	categories = Category.objects.all()
	user_num = request.user.id
	note = Note()
	note_list = note.get_user_note(user_num)
	return render_to_response("view_note.html", {"note_list": note_list, "categories": categories}, RequestContext(request, ))
	
		
@login_required(login_url='/user/login/')
def collect(request, id=''):
	book = Book.objects.get(id=id)
        user_num = request.user.id
	collection = Collection()
	collection.add_book(user_num, book)
	return HttpResponseRedirect("/book/%d/" % (book.id))

@login_required(login_url='/user/login/')
def dis_collect(request, id=''):
	book = Book.objects.get(id=id)
	user_num = request.user.id
	collection = Collection()
	collection.remove_book(user_num, book)
	collection_list = collection.get_user_collection(user_num)
	
	return HttpResponseRedirect("/user/collection/")

@login_required(login_url='/user/login/')
def view_collection(request):
	categories = Category.objects.all()
	user_num = request.user.id
	collection = Collection()
	collection_list = collection.get_user_collection(user_num)
		
	return render_to_response("view_collection.html", {"collection_list": collection_list, "categories": categories}, RequestContext(request, ))

@login_required(login_url='/user/login/')
def mark(request, id=''):
	content = Content.objects.get(id=id)
	user_num = request.user.id
	bookmark = Bookmark()
	bookmark.add_bookmark(user_num, content)
	return HttpResponseRedirect("/book/chapter/%d/" % (content.id))

@login_required(login_url='/user/login/')
def dis_mark(request, id=''):
	content = Content.objects.get(id=id)
	user_num = request.user.id
	bookmark = Bookmark()
	bookmark.remove_bookmark(user_num, content)
	bookmark_list = bookmark.get_user_bookmark(user_num)
	return HttpResponseRedirect("/user/bookmark/")

@login_required(login_url='/user/login/')
def view_bookmark(request):
	categories = Category.objects.all()
	user_num = request.user.id
	bookmark = Bookmark()
	bookmark_list = bookmark.get_user_bookmark(user_num)
	return render_to_response("view_bookmark.html", {"bookmark_list": bookmark_list, "categories": categories}, RequestContext(request, ))

@login_required(login_url='/user/login/')
def account(request):
	categories = Category.objects.all()
	return render_to_response("account.html", {"categories": categories, },  RequestContext(request, ))

def about(request):
	categories = Category.objects.all()
	return render_to_response("about.html", {"categories": categories, },  RequestContext(request,))

def contact(request):
	categories = Category.objects.all()
	return render_to_response("contact.html", {"categories": categories, }, RequestContext(request,))






