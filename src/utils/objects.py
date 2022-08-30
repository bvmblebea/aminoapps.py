class ChatThreads:
	def __init__(self, data):
		self.json = data
		self.title = []
		self.ndc_id = []
		self.content = []
		self.thread_id = []
	
	@property
	def ChatThreads(self):
		for thread in self.json:
			try:
				self.title.append(thread["title"])
			except (KeyError, TypeError):
				pass
			try:
				self.content.append(thread["content"])
			except (KeyError, TypeError):
				pass
			try:
				self.thread_id.append(thread["threadId"])
			except (KeyError, TypeError):
				pass
			try:
				self.ndc_id.append(thread["ndcId"])
			except (KeyError, TypeError):
				pass
		return self


class CommunityList:
	def __init__(self, data):
		self.json = data
		self.name = []
		self.link = []
		self.ndc_id = []
		self.amino_id = []

	@property
	def CommunityList(self):
		for community in self.json:
			self.name.append(community["name"])
			self.link.append(community["link"])
			self.ndc_id.append(community["ndcId"])
			self.amino_id.append(community["endpoint"])
		return self

class MembersList:
	def __init__(self, data):
		self.json = data
		self.icon = []
		self.user_id = []
		self.nickname = []
		self.created_time = []
	
	@property
	def MembersList(self):
		for members in self.json:
			try:
				self.nickname.append(members["nickname"])
			except (KeyError, TypeError):
				pass
			try:
				self.user_id.append(members["uid"])
			except (KeyError, TypeError):
				pass
			try:
				self.created_time.append(members["createdTime"])
			except (KeyError, TypeError):
				pass
			try:
				self.icon.append(members["icon"])
			except (KeyError, TypeError):
				pass
		return self

class FromLink:
	def __init__(self, data):
		self.json = data
		self.path = None
		self.ndc_id = None
		self.full_url = None
		self.object_id = None 
		self.short_url = None 
		self.full_path = None  
		self.short_code = None
		self.object_type = None 
		self.target_code = None 
	
	@property
	def FromLink(self):
		try:
			self.path = self.json["path"] 
		except (KeyError, TypeError): 
			pass		
		try:
			self.object_type = self.json["extensions"]["linkInfo"]["objectType"]
		except (KeyError, TypeError): 
			pass
		try: 
			self.short_code = self.json["extensions"]["linkInfo"]["shortCode"]
		except (KeyError, TypeError):
			pass
		try:
			self.full_path = self.json["extensions"]["linkInfo"]["fullPath"]
		except (KeyError, TypeError):
			pass
		try:
			self.target_code = self.json["extensions"]["linkInfo"]["targetCode"]
		except (KeyError, TypeError):
			pass
		try: 
			self.object_id = self.json["extensions"]["linkInfo"]["objectId"]
		except (KeyError, TypeError):
			pass
		try:
			self.short_url = self.json["extensions"]["linkInfo"]["shareURLShortCode"]
		except (KeyError, TypeError):
			pass
		try:
			self.full_url = self.json["extensions"]["linkInfo"]["shareURLFullPath"]
		except (KeyError, TypeError):
			pass
		try:
			self.ndc_id = self.json["extensions"]["linkInfo"]["ndcId"]
		except (KeyError, TypeError):
			pass
		return self

class UserInfo:
	def __init__(self, data):
		self.json = data
		self.icon = None
		self.web_URL = None
		self.user_id = None
		self.content = None 
		self.amino_id = None 
		self.nickname = None
		self.created_time = None 
		self.modified_time = None

	@property
	def UserInfo(self):
		try:
			self.amino_id = self.json["aminoId"]
		except (KeyError, TypeError):
			pass 
		try:
			self.user_id = self.json["uid"]
		except (KeyError, TypeError): 
			pass 
		try:
			self.nickname = self.json["nickname"]
		except (KeyError, TypeError): 
			pass 
		try:
			self.content = self.json["content"]
		except (KeyError, TypeError): 
			pass 
		try:
			self.icon = self.json["icon"]
		except (KeyError, TypeError): 
			pass 
		try:
			self.web_URL = self.json["webURL"]
		except (KeyError, TypeError): 
			pass
		try:
			self.created_time = self.json["createdTime"]
		except (KeyError, TypeError): 
			pass 
		try:
			self.modified_time = self.json["modifiedTime"]
		except (KeyError, TypeError): 
			pass 
		return self 
		
class BlogsList:
	def __init__(self, data):
		self.json = data
		self.title = []
		self.blog_id = []
		self.content = []
		self.created_time = []
		self.modified_time = []
		self.comments_count = []
		
	@property
	def BlogsList(self):
		for blog in self.json:
			try:
				self.blog_id.append(blog["blogId"])
			except (KeyError, TypeError):
				pass
			try:
				self.title.append(blog["title"])
			except (KeyError, TypeError):
				pass
			try:
				self.content.append(blog["content"])
			except (KeyError, TypeError):
				pass
			try:
				self.comments_count.append(blog["commentsCount"])
			except (KeyError, TypeError):
				pass
			try:
				self.created_time.append(blog["createdTime"])
			except (KeyError, TypeError):
				pass
			try:
				self.modified_time.append(blog["modifiedTime"])
			except (KeyError, TypeError):
				pass
		return self
