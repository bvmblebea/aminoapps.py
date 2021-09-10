class ChatThreads:
    def __init__(self, data):
        self.json = data
        self.title = []
        self.content = []
        self.thread_Id = []
        self.ndc_Id = []

    @property
    def ChatThreads(self):
        for thread in self.json:
        	try:	self.title.append(thread["title"])
        	except (KeyError, TypeError):	self.title.append(None)
        	try:	self.content.append(thread["content"])
        	except (KeyError, TypeError):	self.content.append(None)
        	try:	self.thread_Id.append(thread["threadId"])
        	except (KeyError, TypeError):	self.thread_Id.append(None)
        	try:	self.ndc_Id.append(thread["ndcId"])
        	except (KeyError, TypeError): self.ndc_Id.append(None)
        
        return self

class CommunityList:
    def __init__(self, data):
        self.json = data
        self.ndc_Id = []
        self.name = []
        self.link = []
        self.amino_Id = []

    @property
    def CommunityList(self):
        for x in self.json:
            self.ndc_Id.append(x["ndcId"])
            self.name.append(x["name"])
            self.link.append(x["link"])
            self.amino_Id.append(x["endpoint"])
            
        return self

class MembersList:
    def __init__(self, data):
        self.json = data
        self.nickname = []
        self.user_Id = []
        self.createdTime = []
        self.icon = []

    @property
    def MembersList(self):
        for x in self.json:
        	try:	self.nickname.append(x["nickname"])
        	except (KeyError, TypeError):	pass
        	try:	self.user_Id.append(x["uid"])
        	except (KeyError, TypeError):	pass
        	try:	self.createdTime.append(x["createdTime"])
        	except (KeyError, TypeError):	pass
        	try:	self.icon.append(x["icon"])
        	except (KeyError, TypeError):	pass

        return self

class FromLink:
	def __init__(self, data):
		self.json = data
		self.path = None
		self.object_type = None 
		self.short_code = None 
		self.full_path = None 
		self.target_code = None 
		self.object_Id = None 
		self.short_url = None 
		self.full_url = None
		self.ndc_Id = None
	
	@property
	def FromLink(self):
		try:	self.path = self.json["path"] 
		except (KeyError, TypeError): 	pass		
		try:	self.object_type = self.json["extensions"]["linkInfo"]["objectType"]
		except (KeyError, TypeError): 	pass
		try: 	self.short_code = self.json["extensions"]["linkInfo"]["shortCode"]
		except (KeyError, TypeError): 	pass
		try:	self.full_path = self.json["extensions"]["linkInfo"]["fullPath"]
		except (KeyError, TypeError):	pass
		try:	self.target_code = self.json["extensions"]["linkInfo"]["targetCode"]
		except (KeyError, TypeError):	pass
		try: 	self.object_Id = self.json["extensions"]["linkInfo"]["objectId"]
		except (KeyError, TypeError):	pass
		try:	self.short_url = self.json["extensions"]["linkInfo"]["shareURLShortCode"]
		except (KeyError, TypeError):	pass
		try:	self.full_url = self.json["extensions"]["linkInfo"]["shareURLFullPath"]
		except (KeyError, TypeError):	pass
		try:	self.ndc_Id = self.json["extensions"]["linkInfo"]["ndcId"]
		except (KeyError, TypeError):	pass
		
		return self

class UserInfo:
	def __init__(self, data):
		self.json = data
		self.amino_Id = None 
		self.user_Id = None
		self.nickname = None
		self.content = None 
		self.icon = None 
		self.web_URL = None
		self.createdTime = None 
		self.modifiedTime = None

	@property
	def UserInfo(self):
		try:	self.amino_Id = self.json["aminoId"]
		except (KeyError, TypeError): 	pass 
		try:	self.user_Id = self.json["uid"]
		except (KeyError, TypeError): 	pass 
		try:	self.nickname = self.json["nickname"]
		except (KeyError, TypeError): 	pass 
		try:	self.content = self.json["content"]
		except (KeyError, TypeError): 	pass 
		try:	self.icon = self.json["icon"]
		except (KeyError, TypeError): 	pass 
		try:	self.web_URL = self.json["webURL"]
		except (KeyError, TypeError): 	pass
		try:	self.createdTime = self.json["createdTime"]
		except (KeyError, TypeError): 	pass 
		try:	self.modifiedTime = self.json["modifiedTime"]
		except (KeyError, TypeError): 	pass 
		
		return self 
		
class BlogsList:
	def __init__(self, data):
		self.json = data
		self.blog_Id = []
		self.title = []
		self.content = []
		self.comments_count = []
		self.createdTime = []
		self.modifiedTime = []
		
	@property
	def BlogsList(self):
		for blog in self.json:
			try:	self.blog_Id.append(blog["blogId"])
			except (KeyError, TypeError):	pass
			try:	self.title.append(blog["title"])
			except (KeyError, TypeError):	pass
			try:	self.content.append(blog["content"])
			except (KeyError, TypeError):	pass
			try:	self.comments_count.append(blog["commentsCount"])
			except (KeyError, TypeError):	pass
			try:	self.createdTime.append(blog["createdTime"])
			except (KeyError, TypeError):	pass
			try:	self.modifiedTime.append(blog["modifiedTime"])
			except (KeyError, TypeError):	pass

		return self
