#-*- coding:utf-8 -*-
from models import CollectionItem, ReadHistoryItem
from datetime import datetime

class Collection(object):
	
	def __init__(self, *args, **kwargs):
		self.items = list(CollectionItem.objects.all())

	def get_items(self):
		return self.items
	
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


#	def extend_collection(self, books):
#		self.items.extend(books)


class ReadHistory(object):
	
	def __init__(self, *args, **kwargs):
		self.items= list(ReadHistoryItem.objects.all())
	
	def get_items(self):
		return self.items

	def add_content(self, user_num, content):
		for item in self.items:
			if item.content.id == content.id and item.user_num == user_num:
				ReadHistoryItem.objects.filter(user_num=user_num, content_id__exact=content.id).update(read_time=datetime.now())
				return 
		read_history_item = ReadHistoryItem(user_num=user_num, content=content)
		read_history_item.save()
		self.items.append(read_history_item)
	
	def get_user_history(self, user_num):
		histories = []
		for item in self.items:
			if item.user_num == user_num:
				histories.append(item)
		return histories
	
#	def extend_history(self, contents):
#		self.items.extend(contents)



