class chatThreads:
    def __init__(self, data):
        self.json = data
        self.title = []
        self.content = []
        self.threadId = []
        self.ndcId = []

    @property
    def chatThreads(self):
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
