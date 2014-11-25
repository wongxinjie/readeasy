# -*- coding: utf-8 -*-
import re
import urllib

class BookInfo:
	def __init__(self, isbn):
		self.isbn = isbn
		self.regex_dict = {'average_info': r'(?<= <strong class="ll rating_num " property="v:average">).*? (?= </strong>)', 'vote_info': r'(?<= <a href="collections"><span property="v:votes">).*?(?= </span>)', 'buy_info': r'(?<= <div id="buyinfo-printed">).*?(?= </div>)', 'borrow_info': r'(?<= <ul class="bs more-after">).*?(?= </ul>)'}
	       	self.get_book_page()

	def get_compile_result(self, regex):
		compiler = re.compile(regex, re.S|re.I|re.U)
		result_list = [result for result in compiler.findall(self.lines)]
		return result_list

	def get_book_id(self):
		url = "http://book.douban.com/subject_search?search_text=%s"%self.isbn
		urlopener = urllib.urlopen(url)
		lines = urlopener.read()
		book_id_compiler = re.compile(r'(?<= <a href="http://book.douban.com/subject/).*?(?=/" title)', re.S|re.I|re.U)
		book_id_list = [book_id for book_id in book_id_compiler.findall(lines)]
		if book_id_list:
			return book_id_list[0]

	def get_book_page(self):
		book_id = self.get_book_id()
		self.url = "http://book.douban.com/subject/%s/" % book_id
		urlopener = urllib.urlopen(self.url)
		self.lines = urlopener.read()
	
		
	def get_book_info(self):
		#get vote numbers
		vote_list = self.get_compile_result(self.regex_dict['vote_info'])
		if vote_list:
			vote_str = vote_list[0].strip().split('<')
			if vote_str:
				self.votes = vote_str[0]
		#get average score
		average_list = self.get_compile_result(self.regex_dict['average_info'])
		if average_list:
			self.average = average_list[0]
		#get buy infomation
		buy_info_list = self.get_compile_result(self.regex_dict['buy_info'])
		buy_info_list = [buy_info.replace('<ul class="bs noline more-after ">', '') for buy_info in buy_info_list]
		buy_info_list = [buy_info.replace('<li class="">', '') for buy_info in buy_info_list]
		self.buy_info = [buy_info.replace('h2', 'h5').decode('utf8') for buy_info in buy_info_list]
		#get borrow infomation
		borrow_info_list = self.get_compile_result(self.regex_dict['borrow_info'])
		self.borrow_info = [borrow_info.decode('utf8') for borrow_info in borrow_info_list]


	









