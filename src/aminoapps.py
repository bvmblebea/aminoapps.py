# I didn't test some functions
import requests
from json import loads
from utils import objects
from base64 import b64decode
from functools import reduce

class AminoApps:
	def __init__(self, device_id: str):
		self.api = "https://aminoapps.com/api"
		self.web = "https://aminoapps.com/web"
		self.device_id = device_id
		self.headers = {
			"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36",
			"x-requested-with": "xmlhttprequest"
		}
		
   
	def login_sid(self, sid: str):
		data = loads(b64decode(
			reduce(lambda a, e: a.replace(*e), (
				"-+",
				"_/"),
				sid + "=" * (
					-len(sid) % 4)).encode()
				)[1:-20].decode())
		self.sid = sid
		self.user_id = data["2"]
		self.headers["cookie"] = f"sid={self.sid}"
		self.headers["set-cookie"] = self.sid
		return data
	
	def logout(self):
		self.headers = requests.post(
			f"{self.api}/logout", headers=self.headers).headers
		self.sid = None
		self.user_id = None
	
	def my_chat_threads(
			self,
			ndc_id: int,
			start: int = 0,
			size: int = 10):
		data = {
			"ndcId": f"x{ndc_id}",
			"start": start,
			"size": size
		}
		response = requests.post(
			f"{self.api}/my-chat-threads",
			json=data,
			headers=self.headers).json()
		return objects.ChatThreads(
			response["result"]["threadList"]).ChatThreads

	def send_message(
			self,
			ndc_id: int,
			thread_id: str,
			message: str,
			message_type: int = 0):
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"message": {
				"content": message,
				"mediaType": 0,
				"type": message_type,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		return requests.post(
			f"{self.api}/add-chat-message",
			json=data,
			headers=self.headers).json()


	def send_image(
			self,
			ndc_id: int,
			thread_id: str,
			image_url: str):
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"message": {
				"content": None,
				"mediaType": 100,
				"mediaValue": image_url,
				"type": 0,
				"uploadId": 0,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		return requests.post(
			f"{self.api}/add-chat-message",
			json=data,
			headers=self.headers).json()
	
	def send_sticker(
			self,
			ndc_id: int,
			thread_id: str,
			sticker_id: str = "e/f09f9886"):
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"message": {
				"stickerId": sticker_id,
				"stickerType": "Emoji Sticker",
				"mediaValue": f"ndcsticker://{sticker_id}",
				"type": 3,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		return requests.post(
			f"{self.api}/add-chat-message",
			json=data,
			headers=self.headers).json()
		
	def submit_comment(
			self,
			ndc_id: int,
			content: str,
			user_id: str = None,
			blog_id: str = None,
			wiki_id: str = None):
		data = {
			"ndcId": ndc_id,
			"content": content
		}
		if blog_id:
			data["postType"] = "blog"
			post_id = blog_id
		elif wiki_id:
			data["postType"] = "wiki"
			post_id = wiki_id
		elif user_id:
			data["postType"] = "user"
			post_id = user_id
		data["postId"] = post_id
		return requests.post(
			f"{self.api}/submit_comment",
			json=data,
			headers=self.headers).json()
	
	def update_account(self, nickname: str = None):
		data = {}
		if nickname:
			data["nickname"] = nickname
		return requests.post(
			f"{self.api}/update-account/{self.user_id}",
			json=data,
			headers=self.headers).json()
	
	def join_thread(self, ndc_id: int, thread_id: str):
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id
		}
		return requests.post(
			f"{self.api}/join-thread",
			json=data,
			headers=self.headers).json()
	
	def leave_thread(self, ndc_id: int, thread_id: str):
		data = {
			"ndcId": f"x{ndc_id}", 
			"threadId": thread_id
		}
		return requests.post(
			f"{self.api}/leave-thread",
			json=data,
			headers=self.headers).json()
	
	def follow_user(self, ndc_id: int, user_id: str):
		data = {
			"followee_id": user_id,
			"ndcId": f"x{ndc_id}"
		}
		return requests.post(
			f"{self.api}/follow-user",
			json=data,
			headers=self.headers).json()
	
	def unfollow_user(self, ndc_id: int, user_id: str):
		data = {
			"followee_id": user_id,
			"follower_id": self.user_id,
			"ndcId": f"x{ndc_id}"
		}
		return requests.post(
			f"{self.api}/unfollow-user",
			json=data,
			headers=self.headers).json()
	
	def vote(
			self,
			ndc_id: int,
			blog_id: str = None,
			wiki_id: str = None):
		data = {"ndcId": ndc_id}
		if blog_id:
			data["logType"] = "blog"
			data["postType"] = "blog"
			post_id = blog_id
		elif wiki_id:
			data["logType"] = "wiki"
			data["postType"] = "wiki"
			post_id = wiki_id
		data["postId"] = post_id
		return requests.post(
			f"{self.api}/vote",
			json=data,
			headers=self.headers).json()
	
	def unvote(
			self,
			ndc_id: int,
			blog_id: str = None,
			wiki_id: str = None):
		data = {"ndcId": ndc_id}
		if blog_id:
			data["logType"] = "blog"
			data["postType"] = "blog"
			post_id = blog_id
		elif wiki_id:
			data["logType"] = "wiki"
			data["postType"] = "wiki"
			post_id = wiki_id
		data["postId"] = post_id
		return requests.post(
			f"{self.api}/unvote",
			json=data,
			headers=self.headers).json()
	
	def join_community(self, ndc_id: int, invite_code: str = None):
		data = {"ndcId": ndc_id}
		if invite_code:
			data["InviteCode"] = invite_code
		return requests.post(
			f"{self.api}/join",
			json=data,
			headers=self.headers).json()
	
	def leave_community(self, ndc_id: int):
		data = {"ndcId": ndc_id}
		return requests.post(
			f"{self.api}/leave",
			json=data,
			headers=self.headers).json()

	def request_to_join_community(
			self,
			ndc_id: int,
			message: str = None):
		data = {"ndcId": ndc_id}
		if message:
			data["message"] = message
		return requests.post(
			f"{self.api}/request_join",
			json=data,
			headers=self.headers).json()
	
	def add_flag(
			self,
			ndc_id: int,
			reason: str,
			flag_type: int,
			user_id: str = None,
			blog_id: str = None,
			wiki_id: str = None,
			thread_id: str = None):
		data = {
			"flagType": flag_type,
			"message": reason,
			"ndcId": f"x{ndc_id}"
		}
		if user_id:
			data["objectId"] = user_id
			data["objectType"] = 0
		elif blog_id:
			data["objectId"] = blog_id
			data["objectType"] = 1
		elif wiki_id:
			data["objectId"] = wiki_id
			data["objectType"] = 2
		elif thread_id:
			data["objectId"] = thread_id
			data["objectType"] = 12
		return requests.post(
			f"{self.api}/add-flag",
			json=data,
			headers=self.headers).json()
	
	def send_active_object(self, ndc_id: int):
		data = {"ndcId": ndc_id}
		return requests.post(
			f"{self.api}/community/stats/web-user-active-time",
			json=data,
			headers=self.headers).json()
	
	def get_websocket_url(self):
		return requests.get(
			f"{self.api}/chat/web-socket-url", headers=self.headers).json()

	def block_full_list(self):
		return requests.get(
			f"{self.api}/block/full-list", headers=self.headers).json()
	
	def create_chat_thread(
			self,
			ndc_id: int,
			user_id: str,
			message: str,
			type: int = 0):
		data = {
			"ndcId": ndc_id,
			"inviteeUids": user_id,
			"initialMessageContent": message,
			"type": type
		}
		return requests.post(
			f"{self.api}/create-chat-thread",
			json=data,
			headers=self.headers).json()
		
	def get_online_users(self, ndc_id: int):
		return objects.MembersList(
			requests.get(
				f"{self.api}/x{ndc_id}/online-members", headers=self.headers).json()["result"]["onlineMembersList"]).MembersList
	
	def check_thread(self, ndc_id: int):
		data = {"ndcId": f"x{ndc_id}"}
		return requests.post(
			f"{self.api}/thread-check",
			json=data,
			headers=self.headers).json()

	def link_translation(
			self,
			ndc_id: int,
			user_id: str = None,
			blog_id: str = None,
			wiki_id: str = None,
			thread_id: str = None):
		data = {"ndcId": f"x{ndc_id}"}
		if user_id:
			data["objectId"] = user_id
			data["objectType"] = 0
		elif blog_id:
			data["objectId"] = blog_id
			data["objectType"] = 1
		elif wiki_id:
			data["objectId"] = wiki_id
			data["objectType"] = 2
		elif thread_id:
			data["objectId"] = thread_id
			data["objectType"] = 12
		return requests.post(
			f"{self.api}/link-translation",
			json=data,
			headers=self.headers).json()
        
        
	def get_blog_categories(self, ndc_id: int):
		return requests.get(
			f"{self.api}/get-blog-category?ndcId={ndc_id}", headers=self.headers).json()

	# in development
	def create_blog(
			self,
			ndc_id: int,
			title: str,
			content: str = None,
			categories_list: list = None,
			extensions: dict = None,
			fans_only: bool = False,
			type: int = 0):
		media_list = []
		data = {
   	 	"postJSON": {
  		  	"title": title,
 		   	"content": content,
    			"type": type,
  		  	"mediaList": media_list,
 		   	"extensions": extensions,
   		 	"ndcId": ndc_id
   		}
		}
		if fans_only:
			data["extensions"] = {"fansOnly": fans_only}
		elif categories_list:
			data["taggedBlogCategoryIdList"] = categories_list
		return requests.post(
			f"{self.api}/blog",
			json=data,
			headers=self.headers).json()

	# delete blog
	def delete_blog(self, ndc_id: int, blog_id: str):
		data = {
			"ndcId": f"x{ndc_id}",
			"postId": blog_id,
			"postType": "blog"
		}
		return requests.post(
			f"{self.api}/post/delete",
			json=data,
			headers=self.headers).json()
	
	def get_thread_users(
			self,
			ndc_id: int,
			thread_id: str,
			type: str = "default",
			start: int = 0,
			size: int = 10):
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"type": type,
			"start": start,
			"size": size
		}
		return requests.post(
			f"{self.api}/members-in-thread",
			json=data,
			headers=self.headers).json()
	
	
	def get_thread_messages(
			self,
			ndc_id: int,
			thread_id: str,
			size: int = 10):
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id, 
			"size": size
		}
		return requests.post(
			f"{self.api}/chat-thread-messages",
			json=data,
			headers=self.headers).json()
	
	
	def get_blog_votes(self, ndc_id: int, blog_id: str):
		return requests.get(
			f"{self.api}/x{ndc_id}/blog/{blog_id}/votes", headers=self.headers).json()
	
	
	def poll_option(self, ndc_id: int, blog_id: str, option_id: str):
		return requests.post(
			f"{self.api}/poll-option/x{ndc_id}/{blog_id}/{option_id}/vote", headers=self.headers).json()
	
	
	def register(
			self,
			email: str,
			password: str,
			nickname: str,
			verification_code: str):
		data = {
			"email": email,
			"nickname": nickname,
			"phoneNumber": "",
			"secret2": password,
			"validationContext": {
				"data": {
					"code": verification_code
				},
			"code": verification_code,
			"identity": email,
			"type": 1,
			"__original": {
			"data": {
				"code": verification_code
			},
			"code": verification_code,
			"identity": email,
			"type": 1,
			"__response": {}
				}
			}
		}
		return requests.post(
			f"{self.api}/register",
			json=data,
			headers=self.headers).json()
	
	def check_security_validation(self, email: str, verification_code: str):
		data = {
		"validationContext": {
			{
				"data": {
					"code": verification_code
				},
				"identity": email,
				"type": 1,
				"verifyInfoKey": None 
				}
			}
		}
		return requests.post(
			f"{self.api}/auth/check-security-validation",
			json=data,
			headers=self.headers).json()
	
	def remove_comment(
			self,
			ndc_id: int,
			comment_id: int,
			blog_id: str = None,
			wiki_id: str = None):
		data = {
			"ndcId": ndc_id,
			"commentId": comment_id
		}
		if blog_id:
			data["postType"] = "blog"
			post_id = blog_id
		elif wiki_id:
			data["postType"] = "wiki"
			post_id = wiki_id
		data["postId"] = post_id
		return requests.post(
			f"{self.api}/remove_comment",
			json=data,
			headers=self.headers).json()
	
	def request_security_validation(self, email: str, type: int = 1):
		data = {
			"identity": email,
			"type": type,
			"verifyInfoKey": None
		}
		return requests.post(
			f"{self.api}/auth/request-security-validation",
			json=data,
			headers=self.headers).json()
	
	def find_exist_single_chat(self, ndc_id: int, user_id: str):
		data = {"ndcId": ndc_id, "uid": user_id}
		return requests.post(
			f"{self.api}/find-exist-single-chat",
			json=data,
			headers=self.headers).json()
	
	def get_user_profile(self, ndc_id: int):
		data = {"ndcId": ndc_id}
		return requests.post(
			f"{self.api}/get-user-profile",
			json=data,
			headers=self.headers).json()
	
	def delete_account(self, password: str):
		data = {"secret": password}
		return requests.post(
			f"{self.api}/account/delete-request/",
			json=data,
			headers=self.headers).json()
	
	def get_live_threads(
			self,
			ndc_id: int,
			start: int = 0,
			size: int = 10):
		return requests.get(
			f"{self.api}/chat/live-threads?ndcId=x{ndc_id}&start={start}&size={size}",
			headers=self.headers).json()
	
	def get_thread(self, ndc_id: int, thread_id: str):
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id
		}
		return requests.post(
			f"{self.api}/get-one-thread",
			json=data,
			headers=self.headers).json()
	
	def get_blog(self, ndc_id: int, blog_id: str):
		return requests.get(
			f"{self.web}/x{ndc_id}/blog/{blog_id}", headers=self.headers).json()
	
	def get_user_profile(self, ndc_id: int, user_id: str):
		data = {
			"ndcId": f"x{ndc_id}",
			"userId": user_id
		}
		return requests.post(
			f"{self.api}/chat/get-user-profile",
			json=data,
			headers=self.headers).json()
	
	def pick_locale(self, locale: str = "en"):
		data = {"locale": locale}
		return requests.post(
			f"{self.api}/pick-locale",
			json=data,
			headers=self.headers).json()
