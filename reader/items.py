#-*- coding:utf-8 -*-
from models import CollectionItem, BookmarkItem, NoteItem
from datetime import datetime

class Collection(object):
	
	def __init__(self, *args, **kwargs):
		self.items = list(CollectionItem.objects.all())

	
	def add_book(self, user_num, book):
		for item in self.items:
			if item.book.id == book.id and item.user_num == user_num:
				collection_list = CollectionItem.objects.filter(user_num=user_num, book_id__exact=book.id)
				collection_list.update(dis_collect=False)
				collection_list.update(add_date = datetime.now())
				return
		collection_item = CollectionItem(user_num=user_num, book=book, dis_collect=False)
		collection_item.save() 
		self.items.append(collection_item)
	
	def remove_book(self, user_num, book):
		for item in self.items:
			if item.book.id == book.id and item.user_num == user_num:
				CollectionItem.objects.filter(user_num=user_num, book_id__exact=book.id).update(dis_collect=True)
				self.items.remove(item)
				return 
	
	def get_user_collection(self, user_num):
		collections = []
		for item in self.items:
			if item.user_num == user_num and not item.dis_collect:
				collections.append(item)
		return collections



class Bookmark(object):

	def __init__(self, *args, **kwargs):
		self.items = list(BookmarkItem.objects.all())
	
	def add_bookmark(self, user_num, content):
		for item in self.items:
			if item.content.id == content.id and item.user_num == user_num:
				content_list = BookmarkItem.objects.filter(user_num=user_num, content_id__exact=content.id)
				content_list.update(dis_add=False)
				content_list.update(add_time=datetime.now())
				return
		bookmark_item = BookmarkItem(user_num=user_num, content=content, dis_add=False)
		bookmark_item.save()
		self.items.append(bookmark_item)

	def remove_bookmark(self, user_num, content):
		for item in self.items:
			if item.content.id == content.id and item.user_num == user_num:
				BookmarkItem.objects.filter(user_num=user_num, content_id__exact=content.id).update(dis_add=True)
				self.items.remove(item)
				return

	def get_user_bookmark(self, user_num):
		bookmarks = []
		for item in self.items:
			if item.user_num == user_num and not item.dis_add:
				bookmarks.append(item)
		return bookmarks


class Note(object):
	def __init__(self, *args, **kwargs):
		self.items = list(NoteItem.objects.all())
	
	def add_note(self, user_num, content, text_content):
		for item in self.items:
			if item.content.id == content.id and item.user_num == user_num:
				note_list = NoteItem.objects.filter(user_num=user_num, content_id__exact=content.id)
				note_list.update(text_content=text_content)
				note_list.update(dis_add=False)
				note_list.update(edit_time= datetime.now())
				return
		note_item = NoteItem(user_num=user_num, content=content, dis_add=False, text_content=text_content)
		note_item.save()
		self.items.append(note_item)

	def remove_note(self, user_num, content):
		for item in self.items:
			if item.content.id == content.id and item.user_num == user_num:
			       	note_list = NoteItem.objects.filter(user_num=user_num, content_id__exact=content.id)
				note_list.update(text_content='')
				note_list.update(dis_add=True)
				self.items.remove(item)
				return
	
	def get_user_note(self, user_num):
		notes = []
		for item in self.items:
			if item.user_num == user_num and not item.dis_add:
				notes.append(item)
		return notes

	
	
		
		
		
				
		
			






