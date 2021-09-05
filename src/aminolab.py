#Library In Development created by LilZevi
#I have not tested some functions. 
import requests
import json
import random
import string
from utils import headers, objects

class Client():
	def __init__(self, device_Id: str = "22717F5C01029F06DAED62B82F001AAB42333CD930C7936EC7B253594887BA6CE6820148ED69CBF2D0"):
		self.api = "https://aminoapps.com/api"
		self.api_p = "https://aminoapps.com/api-p"
		self.headers = headers.Headers().headers
		self.device_Id = device_Id
		self.user_Id = None
		self.sid = None

	#captcha generator
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
		self.sid = request.headers["set-cookie"]
		try:	self.user_Id = request.json()["result"]["uid"]
		except:	print(f"Error >>", request.json()["result"]["api:message"]); pass
		try:	self.sid = self.sid[0: self.sid.index(";")]
		except:	pass
		headers.sid = self.sid
		headers.user_Id = self.user_Id
		self.headers = headers.Headers(sid=self.sid).headers
		return request.json()
	
	#logout
	def logout(self):
		self.headers = {"cookie": f"sid={self.sid.replace('sid=', '')}; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Path=/"}
		request = requests.post("{self.api}/logout", headers=self.headers)
		self.sid = None
		self.user_Id = None
		request.headers["cookie"] = request.headers["set-cookie"]
		request.headers.pop("set-cookie")
		self.headers = request.headers
		return request.json()

	#get public chats list
	def get_public_chat_threads(self, ndc_Id, start: int = 0, size: int = 10):
		request = requests.get(f"{self.api}/chat/live-threads?ndcId=x{ndc_Id}&start={start}&size={size}", headers=self.headers).json()
		return objects.ChatThreads(request["result"]["threadList"]).ChatThreads

	#get joined chats list
	def my_chat_threads(self, ndc_Id, start: int = 0, size: int = 10):
		data = {"ndcId": f"x{ndc_Id}", "start": start, "size": size}
		request = requests.post(f"{self.api}/my-chat-threads", json=data, headers=self.headers).json()
		return objects.ChatThreads(request["result"]["threadList"]).ChatThreads
	
	#send_message
	def send_message(self, ndc_Id, thread_Id, message: str = None, message_type: int = 0):
		data = {
		"ndcId": f"x{ndc_Id}",
		"threadId": thread_Id,
		"message": {"content": message, "mediaType": 0, "type": message_type, "sendFailed": False, "clientRefId": 0}
		}
		request = requests.post(f"{self.api}/add-chat-message", json=data, headers=self.headers)
		return request.json()
	
	#get user information
	def get_user_info(self, user_Id: str):
		request = requests.get(f"{self.api_p}/g/s/user-profile/{user_Id}", headers=self.headers).json()
		return objects.UserInfo(request["userProfile"]).UserInfo
		
	#comment
	def submit_comment(self, ndc_Id, message, user_Id: str = None, blog_Id: str = None, wiki_Id: str = None):
		data = {"content": message, "ndcId": ndc_Id}
		if blogId: data["postType"] = "blog"; post_Id = blog_Id
		if wikiId: data["postType"] = "wiki"; post_Id = wiki_Id
		if userId: data["postType"] = "user"; post_Id = user_Id
		data["postId"] = post_Id
		request = requests.post(f"{self.api}/submit_comment", json=data, headers=self.headers)
		return request.json()
	
	#update account
	def update_account(self, nickname: str = None):
		data = {}
		if nickname:	data["nickname"] = nickname
		request = requests.post(f"{self.api}/update-account/{self.user_Id}", json=data, headers=self.headers)
		return request.json()
		
	#join chat
	def join_thread(self, ndc_Id, thread_Id):
		data = {"ndcId": f"x{ndc_Id}", "threadId": thread_Id}
		request = requests.post(f"{self.api}/join-thread", json=data, headers=self.headers)
		return request.json()
	
	#leave chat
	def leave_thread(self, ndc_Id, thread_Id):
		data = {"ndcId": f"x{ndc_Id}", "threadId": thread_Id}
		request = requests.post(f"{self.api}/leave-thread", json=data, headers=self.headers)
		return request.json()
	
	#get online users
	def get_online_members(self, ndc_Id: str):
		request = requests.get(f"{self.api}/x{ndc_Id}/online-members", headers=self.headers).json()
		return objects.MembersList(request["result"]["onlineMembersList"]).MembersList
	
	#get public communities list, languages - ru = Russia, en = English
	def get_public_communities(self, language: str, size: int = 25):
		request = requests.get(f"{self.api_p}/g/s/topic/0/feed/community?language={language}&type=web-explore&categoryKey=recommendation&size={size}&pagingType=t", headers=self.headers).json()
		return objects.CommunityList(request["communityList"]).CommunityList
	
	#get joined communities list
	def my_communities(self):
		request = requests.get(f"{self.api_p}/g/s/community/joined", headers=self.headers).json()
		return objects.CommunityList(request["communityList"]).CommunityList
		
	#follow
	def follow_user(self, ndc_Id, user_Id: str):
		data = {"followee_id": user_Id, "ndcId": f"x{ndc_Id}"}
		request = requests.post(f"{self.api}/follow-user", json=data, headers=self.headers)
		return request.json()
	
	#unfollow
	def unfollow_user(self, ndc_Id, user_Id: str):
		data = {"followee_id": user_Id, "follower_id": self.user_Id, "ndcId": f"x{ndc_Id}"}
		request = requests.post(f"{self.api}/unfollow-user", json=data, headers=self.headers)
		return request.json()
	
	#like
	def vote(self, ndc_Id, blog_Id: str = None, wiki_Id: str = None):
		data = {"ndcId": ndc_Id}
		if blogId: data["logType"] = "blog"; data["postType"] = "blog"; post_Id = blog_Id
		elif wikiId: data["logType"] = "wiki"; data["postType"] = "wiki"; post_Id = wiki_Id
		data["postId"] = post_Id
		request = requests.post(f"{self.api}/vote", json=data, headers=self.headers)
		return request.json()
	
	#unlike
	def unvote(self, ndc_Id, blog_Id: str = None, wiki_Id: str = None):
		data = {"ndcId": ndc_Id}
		if blogId: data["logType"] = "blog"; data["postType"] = "blog"; post_Id = blog_Id
		elif wikiId: data["logType"] = "wiki"; data["postType"] = "wiki"; post_Id = wiki_Id
		data["postId"] = post_Id
		request = requests.post(f"{self.api}/unvote", json=data, headers=self.headers)
		return request.json()
	
	#join community
	def join_community(self, ndc_Id: str):
		data = {"ndcId": ndc_Id}
		request = requests.post(f"{self.api}/join", json=data, headers=self.headers)
		return request.json()
	
	#leave community
	def leave_community(self, ndc_Id: str):
		data = {"ndcId": ndc_Id}
		request = requests.post(f"{self.api}/leave", json=data, headers=self.headers)
		return request.json()
		
	#request join community
	def request_join_community(self, ndc_Id, message: str = None):
		data = {"message": message, "ndcId": ndc_Id}
		request = requests.post(f"{self.api}/request_join", json=data, headers=self.headers)
		return request.json()
	
	#flag chat or user
	def report(self, ndc_Id, reason: str, flag_type: int, user_Id: str = None, blog_Id: str = None, wiki_Id: str = None, thread_Id: str = None):
		data = {"flagType": flag_type, "message": reason, "ndcId": f"x{ndc_Id}"}
		if user_Id:	data["objectId"] = user_Id; data["objectType"] = 0 
		elif blog_Id:	data["objectId"] = blog_Id; data["objectType"] = 1
		elif wiki_Id:	data["objectId"] = wiki_Id; data["objectType"] = 2
		elif thread_Id:	data["objectId"] = thread_Id; data["objectType"] = 12
		request = requests.post(f"{self.api}/add-flag", json=data, headers=self.headers)
		return request.json()
	
	#send_active_object. VERY SLOW FUCK 
	def send_active_object(self, ndc_Id):
		data = {"ndcId": ndc_Id}
		request = requests.post(f"{self.api}/community/stats/web-user-active-time", json=data, headers=self.headers)
		return request.json()
		
	#get websocket url
	def get_web_socket_url(self):
		request = requests.get(f"{self.api}/chat/web-socket-url", headers=self.headers)
		return request.json()
		
	#get link information
	def get_from_link(self, link: str):
		request = requests.get(f"{self.api_p}/g/s/link-resolution?q={link}", headers=self.headers).json()
		return objects.FromLink(request["linkInfoV2"]).FromLink

	#get blocked and blocker full list
	def get_block_full_list(self):
		request = requests.get(f"{self.api}/block/full-list", headers=self.headers)
		return request.json()
	
	#foulsc code - start chat with user or users 
	def create_chat_thread(self, ndc_Id, user_Id: str, message: str, title: str = None, nvite_type: int = 0):
		data = { 
		"ndcId": ndc_Id,
		"inviteeUids": user_Id,
		"initialMessageContent": message,
		"type": invite_type
		}
		if title:	data["title"] = title
		request = requests.post(f"{self.api}/create-chat-thread", json=data, headers=self.headers)
		return request.json()
