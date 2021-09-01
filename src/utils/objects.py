class ChatThreads:
    def __init__(self, data):
        self.json = data
        self.title = []
        self.content = []
        self.threadId = []
        self.ndcId = []

    @property
    def ChatThreads(self):
        for thread in self.json:
        	try:	self.title.append(thread["title"])
        	except (KeyError, TypeError):	self.title.append(None)
        	try:	self.content.append(thread["content"])
        	except (KeyError, TypeError):	self.content.append(None)
        	try:	self.threadId.append(thread["threadId"])
        	except (KeyError, TypeError):	self.threadId.append(None)
        	try:	self.ndcId.append(thread["ndcId"])
        	except (KeyError, TypeError): self.ndcId.append(None)
        return self

class CommunityList:
    def __init__(self, data):
        self.json = data
        self.ndcId = []
        self.name = []
        self.link = []
        self.aminoId = []

    @property
    def CommunityList(self):
        for x in self.json:
            self.ndcId.append(x["ndcId"])
            self.name.append(x["name"])
            self.link.append(x["link"])
            self.aminoId.append(x["endpoint"])
        return self

class MembersList:
    def __init__(self, data):
        self.json = data
        self.nickname = []
        self.userId = []
        self.createdTime = []
        self.icon = []

    @property
    def MembersList(self):
        for x in self.json:
        	try:	self.nickname.append(x["nickname"])
        	except (KeyError, TypeError):	pass
        	try:	self.userId.append(x["uid"])
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
		self.objectType = None 
		self.shortCode = None 
		self.fullPath = None 
		self.targetCode = None 
		self.objectId = None 
		self.shortUrl = None 
		self.fullUrl = None
		self.ndcId = None
	
	@property
	def FromLink(self):
		try:	self.path = self.json["path"] 
		except (KeyError, TypeError): 	pass
		try:	self.objectType = self.json["extensions"]["linkInfo"]["objectType"]
		except (KeyError, TypeError): 	pass
		try: 	self.shortCode = self.json["extensions"]["linkInfo"]["shortCode"]
		except (KeyError, TypeError): 	pass
		try:	self.fullPath = self.json["extensions"]["linkInfo"]["fullPath"]
		except (KeyError, TypeError):	pass
		try:	self.targetCode = self.json["extensions"]["linkInfo"]["targetCode"]
		except (KeyError, TypeError):	pass
		try: 	self.objectId = self.json["extensions"]["linkInfo"]["objectId"]
		except (KeyError, TypeError):	pass
		try:	self.shortUrl = self.json["extensions"]["linkInfo"]["shareURLShortCode"]
		except (KeyError, TypeError):	pass
		try:	self.fullUrl = self.json["extensions"]["linkInfo"]["shareURLFullPath"]
		except (KeyError, TypeError):	pass
		try:	self.ndcId = self.json["extensions"]["linkInfo"]["ndcId"]
		except (KeyError, TypeError):	pass
		
		return self
