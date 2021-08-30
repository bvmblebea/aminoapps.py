#Library In Development created by LilZevi
#I have not tested some functions. 
#I tested only auth, follow_user, unfollow_user
import requests
import json
import random
import string
from utils import headers

class Client():
	def __init__(self, deviceId: str = "22717F5C01029F06DAED62B82F001AAB42333CD930C7936EC7B253594887BA6CE6820148ED69CBF2D0"):
		self.api = "https://aminoapps.com/api"
		self.headers = headers.Headers().headers
		self.deviceId = deviceId
		self.userId = None
		self.sid = None

	def generate_captcha(self):
		value = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + "_-", k=462)).replace("--", "-")
		return value
        
    #example for auth https://github.com/LynxN1/amino_service/tree/5ae29b8115017ecf79108796eb7bb4e7f1c7a6c5 Thanks to LynxN1
	def auth(self, email: str = None, phone: str = None, password: str = None):
		data = {
		"auth_type": 0,
		"recaptcha_challenge": self.generate_captcha(),
		"recaptcha_version": "v3",
		"secret": password
		}
		if email:	data["email"] = email
		elif phone:	data["phoneNumber"] = phone
		request = requests.post(f"{self.api}/auth", json=data)
		self.headers = request.headers
		try:
			self.sid = request.headers["set-cookie"]
			self.userId = request.json()["result"]["uid"]
		except:	print(f"Error >>", request.json()["result"]["api:message"])
		try:
			self.sid = self.sid[0: self.sid.index(";")]
		except:	pass
		headers.sid = self.sid
		headers.userId = self.userId
		self.headers = headers.Headers(sid=self.sid).headers
		return request.json()
	
	#send_message
	def send_message(self, ndcId, threadId, message: str = None, messageType: int = 0):
		data = {
		"ndcId": f"x{ndcId}",
		"threadId": threadId,
		"content": message,
		"mediaType": 0,
		"type": messageType,
		"sendFailed": False,
		"clientRefId": 0
		}
		request = requests.post(f"{self.api}/add-chat-message", json=data, headers=self.headers)
		return request.json()
	
	#comment
	def submit_comment(self, ndcId, message, userId: str = None, blogId: str = None, wikiId: str = None):
		data = {"content": message, "ndcId": ndcId}
		if blogId: data["postType"] = "blog"; postId = blogId
		if wikiId: data["postType"] = "wiki"; postId = wikiId
		if userId: data["postType"] = "user"; postId = userId
		data["postId"] = postId
		request = requests.post(f"{self.api}/submit_comment", json=data, headers=self.headers)
		return request.json()
	
	#join chat
	def join_thread(self, ndcId, threadId):
		data = {"ndcId": f"x{ndcId}", "threadId": threadId}
		request = requests.post(f"{self.api}/join-thread", json=data, headers=self.headers)
		return request.json()
	
	#leave chat
	def leave_thread(self, ndcId, threadId):
		data = {"ndcId": f"x{ndcId}", "threadId": threadId}
		request = requests.post(f"{self.api}/leave-thread", json=data, headers=self.headers)
		return request.json()
	
	#get chat users
	def members_in_thread(self, ndcId, threadId, start: int = 0, size: int = 10):
		data = {
		"ndcId": f"x{ndcId}",
		"size": size,
		"start": start,
		"threadId": threadId,
		"type": "default"
		}
		request = requests.get(f"{self.api}/members-in-thread", json=data, headers=self.headers)
		return request.json()
	
	#follow
	def follow_user(self, ndcId, followee_id: str):
		data = {"followee_id": followee_id, "ndcId": f"x{ndcId}"}
		request = requests.post(f"{self.api}/follow-user", json=data, headers=self.headers)
		return request.json()
	
	#unfollow
	def unfollow_user(self, ndcId, followee_id: str):
		data = {"followee_id": followee_id, "follower_id": self.userId, "ndcId": f"x{ndcId}"}
		request = requests.post(f"{self.api}/unfollow-user", json=data, headers=self.headers)
		return request.json()
	
	#start chat with user or users
	def create_chat_thread(self, ndcId, message, userId: str):
		data = {
		"initialMessageContent": message,
		"inviteeUids": [userId],
		"ndcId": ndcId,
		"type": 0
		}
		request = requests.post(f"{self.api}/create-chat-thread", json=data, headers=self.headers)
		return request.json()
	
	#like
	def vote(self, ndcId, blogId: str = None, wikiId: str = None):
		data = {"ndcId": ndcId}
		if blogId: data["logType"] = "blog"; data["postType"] = "blog"; postId = blogId
		elif wikiId: data["logType"] = "wiki"; data["postType"] = "wiki"; postId = wikiId
		data["postId"] = postId
		request = requests.post(f"{self.api}/vote", json=data, headers=self.headers)
		return request.json()
	
	#unlike
	def unvote(self, ndcId, blogId: str = None, wikiId: str = None):
		data = {"ndcId": ndcId}
		if blogId: data["logType"] = "blog"; data["postType"] = "blog"; postId = blogId
		elif wikiId: data["logType"] = "wiki"; data["postType"] = "wiki"; postId = wikiId
		data["postId"] = postId
		request = requests.post(f"{self.api}/unvote", json=data, headers=self.headers)
		return request.json()
	
	#join community
	def join_community(self, ndcId: str):
		data = {"ndcId": ndcId}
		request = requests.post(f"{self.api}/join", json=data, headers=self.headers)
		return request.json()
	
	#request join community
	def request_join_community(self, ndcId, message: str = None):
		data = {"message": message, "ndcId": ndcId}
		request = requests.post(f"{self.api}/request_join", json=data, headers=self.headers)
		return request.json()
	
	#flag chat or user
	def report(self, ndcId, reason: str, flagType: int, userId: str = None, blogId: str = None, wikiId: str = None, threadId: str = None):
		data = {"flagType": flagType, "message": reason, "ndcId": f"x{ndcId}"}
		if userId:	data["objectId"] = userId; data["objectType"] = 0 
		elif blogId:	data["objectId"] = blogId; data["objectType"] = 1
		elif wikiId:	data["objectId"] = wikiId; data["objectType"] = 2
		elif threadId:	data["objectId"] = threadId; data["objectType"] = 12
		request = requests.post(f"{self.api}/add-flag", json=data, headers=self.headers)
		return request.json()
		
	#function post_blog():
		
	def get_web_socket_url(self):
		request = requests.get(f"{self.api}/chat/web-socket-url", headers=self.headers)
