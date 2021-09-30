# Library In Development created by LilZevi
# I have not tested some functions.
import websocket
import requests
import json
import time
import base64
import random
import string
from utils import headers, objects, exception


class Client():
    def __init__(
            self,
            device_Id: str = "22717F5C01029F06DAED62B82F001AAB42333CD930C7936EC7B253594887BA6CE6820148ED69CBF2D0"):
        self.api = "https://aminoapps.com/api"
        self.api_p = "https://aminoapps.com/api-p"
        self.headers = headers.Headers().headers
        self.device_Id = device_Id
        self.user_Id = None
        self.sid = None

    # captcha generator
    def generate_captcha(self):
        value = "".join(
            random.choices(
                string.ascii_uppercase +
                string.ascii_lowercase +
                "_-",
                k=462)).replace(
            "--",
            "-")
        return value

    # auth with sid
    def auth_sid(self, sid: str, user_Id: str = None):
        try:
            value = str(base64.b64decode(sid.replace("sid=", "")))
            value_index = value.index("{")
            value_index_two = value.index("}")
            value = value[value_index: value_index_two + 1]
            data = json.loads(value)
            self.user_Id = data["2"]
        except BaseException:
            self.user_Id = user_Id
        self.sid = f"sid={sid}"
        headers.sid = self.sid
        if self.user_Id:
            headers.user_Id = self.user_Id
        else:
            headers.user_Id = None

    # example for auth
    # https://github.com/LynxN1/amino_service/tree/5ae29b8115017ecf79108796eb7bb4e7f1c7a6c5
    # Thanks to LynxN1
    def auth(self, email: str = None, phone: str = None, password: str = None):
        data = {
            "auth_type": 0,
            "recaptcha_challenge": self.generate_captcha(),
            "recaptcha_version": "v3",
            "secret": password
        }
        if email:
            data["email"] = email
        elif phone:
            data["phoneNumber"] = phone
        request = requests.post(f"{self.api}/auth", json=data)
        try:
            self.headers = request.headers
            self.sid = request.headers["set-cookie"]
            try:
                self.sid = self.sid[0: self.sid.index(";")]
            except BaseException:
                return
            self.user_Id = request.json()["result"]["uid"]
            headers.sid = self.sid
            headers.user_Id = self.user_Id
            self.headers = headers.Headers(sid=self.sid).headers
            return request.json()
        except BaseException:
            return exception.CheckExceptions(request.json())

    # logout
    def logout(self):
        self.headers = {
            "cookie": f"sid={self.sid.replace('sid=', '')}; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Path=/"}
        request = requests.post(f"{self.api}/logout", headers=self.headers)
        self.sid = None
        self.user_Id = None
        request.headers["cookie"] = request.headers["set-cookie"]
        request.headers.pop("set-cookie")
        self.headers = request.headers
        return request.json()

    # get public chats list
    def get_public_chat_threads(self, ndc_Id, start: int = 0, size: int = 10):
        request = requests.get(
            f"{self.api}/chat/live-threads?ndcId=x{ndc_Id}&start={start}&size={size}",
            headers=self.headers).json()
        return objects.ChatThreads(request["result"]["threadList"]).ChatThreads

    # get joined chats list
    def my_chat_threads(self, ndc_Id, start: int = 0, size: int = 10):
        data = {"ndcId": f"x{ndc_Id}", "start": start, "size": size}
        request = requests.post(
            f"{self.api}/my-chat-threads",
            json=data,
            headers=self.headers).json()
        return objects.ChatThreads(request["result"]["threadList"]).ChatThreads

    # send_message
    def send_message(
            self,
            ndc_Id,
            thread_Id,
            message: str = None,
            message_type: int = 0):
        data = {
            "ndcId": f"x{ndc_Id}",
            "threadId": thread_Id,
            "message": {
                "content": message,
                "mediaType": 0,
                "type": message_type,
                "sendFailed": False,
                "clientRefId": 0}}
        request = requests.post(
            f"{self.api}/add-chat-message",
            json=data,
            headers=self.headers)
        return request.json()

    # send_image. don't tested
    def send_Image(self, ndc_Id, thread_Id, image_link: str):
        data = {
            "ndcId": f"x{ndc_Id}",
            "threadId": thread_Id,
            "message": {
                "content": None,
                "mediaType": 100,
                "mediaValue": image_link,
                "type": 0,
                "uploadId": 0,
                "sendFailed": False,
                "clientRefId": 0}}
        request = requests.post(
            f"{self.api}/add-chat-message",
            json=data,
            headers=self.headers)
        return request.json()

    # get user information
    def get_user_info(self, user_Id: str):
        request = requests.get(
            f"{self.api_p}/g/s/user-profile/{user_Id}",
            headers=self.headers).json()
        return objects.UserInfo(request["userProfile"]).UserInfo

    # comment
    def submit_comment(
            self,
            ndc_Id,
            message,
            user_Id: str = None,
            blog_Id: str = None,
            wiki_Id: str = None):
        data = {"ndcId": ndc_Id, "content": message}
        if blog_Id:
            data["postType"] = "blog"
            post_Id = blog_Id
        if wiki_Id:
            data["postType"] = "wiki"
            post_Id = wiki_Id
        if user_Id:
            data["postType"] = "user"
            post_Id = user_Id
        data["postId"] = post_Id
        request = requests.post(
            f"{self.api}/submit_comment",
            json=data,
            headers=self.headers)
        return request.json()

    # get supported languages list
    def get_supported_languages(self):
        request = requests.get(
            f"{self.api_p}/g/s/community-collection/supported-languages",
            headers=self.headers)
        return request.json()

    # update account
    def update_account(self, nickname: str = None):
        data = {}
        if nickname:
            data["nickname"] = nickname
        request = requests.post(
            f"{self.api}/update-account/{self.user_Id}",
            json=data,
            headers=self.headers)
        return request.json()

    # join chat
    def join_thread(self, ndc_Id, thread_Id):
        data = {"ndcId": f"x{ndc_Id}", "threadId": thread_Id}
        request = requests.post(
            f"{self.api}/join-thread",
            json=data,
            headers=self.headers)
        return request.json()

    # leave chat
    def leave_thread(self, ndc_Id, thread_Id):
        data = {"ndcId": f"x{ndc_Id}", "threadId": thread_Id}
        request = requests.post(
            f"{self.api}/leave-thread",
            json=data,
            headers=self.headers)
        return request.json()

    # get online users
    def get_online_members(self, ndc_Id: str, start: int = 0, size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/live-layer?topic=ndtopic:x{ndc_Id}:online-members&start={start}&size={size}",
            headers=self.headers).json()
        return objects.MembersList(request["userProfileList"]).MembersList

    # get recent users
    def get_recent_members(self, ndc_Id: str, start: int = 0, size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile?type=recent&start={start}&size={size}",
            headers=self.headers).json()
        return objects.MembersList(request["userProfileList"]).MembersList

    # get banned users
    def get_banned_members(self, ndc_Id: str, start: int = 0, size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile?type=banned&start={start}&size={size}",
            headers=self.headers).json()
        return objects.MembersList(request["userProfileList"]).MembersList

    # get community curators
    def get_curators_list(self, ndc_Id: str):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile?type=curators",
            headers=self.headers).json()
        return objects.MembersList(request["userProfileList"]).MembersList

    # get community leaders
    def get_leaders_list(self, ndc_Id: str):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile?type=leaders",
            headers=self.headers).json()
        return objects.MembersList(request["userProfileList"]).MembersList

    # get public communities list, languages - ru = Russia, en = English
    def get_public_communities(self, language: str, size: int = 25):
        request = requests.get(
            f"{self.api_p}/g/s/topic/0/feed/community?language={language}&type=web-explore&categoryKey=recommendation&size={size}&pagingType=t",
            headers=self.headers).json()
        return objects.CommunityList(request["communityList"]).CommunityList

    # get joined communities list
    def my_communities(self):
        request = requests.get(
            f"{self.api_p}/g/s/community/joined",
            headers=self.headers).json()
        return objects.CommunityList(request["communityList"]).CommunityList

    # follow
    def follow_user(self, ndc_Id, user_Id: str):
        data = {"followee_id": user_Id, "ndcId": f"x{ndc_Id}"}
        request = requests.post(
            f"{self.api}/follow-user",
            json=data,
            headers=self.headers)
        return request.json()

    # unfollow
    def unfollow_user(self, ndc_Id, user_Id: str):
        data = {
            "followee_id": user_Id,
            "follower_id": self.user_Id,
            "ndcId": f"x{ndc_Id}"}
        request = requests.post(
            f"{self.api}/unfollow-user",
            json=data,
            headers=self.headers)
        return request.json()

    # like
    def vote(self, ndc_Id, blog_Id: str = None, wiki_Id: str = None):
        data = {"ndcId": ndc_Id}
        if blog_Id:
            data["logType"] = "blog"
            data["postType"] = "blog"
            post_Id = blog_Id
        elif wiki_Id:
            data["logType"] = "wiki"
            data["postType"] = "wiki"
            post_Id = wiki_Id
        data["postId"] = post_Id
        request = requests.post(
            f"{self.api}/vote",
            json=data,
            headers=self.headers)
        return request.json()

    # unlike
    def unvote(self, ndc_Id, blog_Id: str = None, wiki_Id: str = None):
        data = {"ndcId": ndc_Id}
        if blog_Id:
            data["logType"] = "blog"
            data["postType"] = "blog"
            post_Id = blog_Id
        elif wiki_Id:
            data["logType"] = "wiki"
            data["postType"] = "wiki"
            post_Id = wiki_Id
        data["postId"] = post_Id
        request = requests.post(
            f"{self.api}/unvote",
            json=data,
            headers=self.headers)
        return request.json()

    # get community blogs list
    def get_recent_blogs(self, ndc_Id: str, start: int = 0, size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/feed/blog-all?pagingType=t&start={start}&size={size}",
            headers=self.headers).json()
        return objects.BlogsList(request["blogList"]).BlogsList

    # join community
    def join_community(self, ndc_Id: str):
        data = {"ndcId": ndc_Id}
        request = requests.post(
            f"{self.api}/join",
            json=data,
            headers=self.headers)
        return request.json()

    # leave community
    def leave_community(self, ndc_Id: str):
        data = {"ndcId": ndc_Id}
        request = requests.post(
            f"{self.api}/leave",
            json=data,
            headers=self.headers)
        return request.json()

    # request join community
    def request_join_community(self, ndc_Id, message: str = None):
        data = {"message": message, "ndcId": ndc_Id}
        request = requests.post(
            f"{self.api}/request_join",
            json=data,
            headers=self.headers)
        return request.json()

    # flag chat or user
    def report(
            self,
            ndc_Id,
            reason: str,
            flag_type: int,
            user_Id: str = None,
            blog_Id: str = None,
            wiki_Id: str = None,
            thread_Id: str = None):
        data = {
            "flagType": flag_type,
            "message": reason,
            "ndcId": f"x{ndc_Id}"}
        if user_Id:
            data["objectId"] = user_Id
            data["objectType"] = 0
        elif blog_Id:
            data["objectId"] = blog_Id
            data["objectType"] = 1
        elif wiki_Id:
            data["objectId"] = wiki_Id
            data["objectType"] = 2
        elif thread_Id:
            data["objectId"] = thread_Id
            data["objectType"] = 12
        request = requests.post(
            f"{self.api}/add-flag",
            json=data,
            headers=self.headers)
        return request.json()

    # send_active_object. VERY SLOW FUCK
    def send_active_object(self, ndc_Id):
        data = {"ndcId": ndc_Id}
        request = requests.post(
            f"{self.api}/community/stats/web-user-active-time",
            json=data,
            headers=self.headers)
        return request.json()

    # get websocket url
    def get_web_socket_url(self):
        request = requests.get(
            f"{self.api}/chat/web-socket-url",
            headers=self.headers)
        return request.json()

    # get link information
    def get_from_link(self, link: str):
        request = requests.get(
            f"{self.api_p}/g/s/link-resolution?q={link}",
            headers=self.headers).json()
        return objects.FromLink(request["linkInfoV2"]).FromLink

    # get blocked and blocker full list
    def block_full_list(self):
        request = requests.get(
            f"{self.api}/block/full-list",
            headers=self.headers)
        return request.json()

    # foulsc code - start chat with user or users
    def create_chat_thread(
            self,
            ndc_Id,
            user_Id: str,
            message: str,
            title: str = None,
            type: int = 0):
        data = {
            "ndcId": ndc_Id,
            "inviteeUids": user_Id,
            "initialMessageContent": message,
            "type": type
        }
        if title:
            data["title"] = title
        request = requests.post(
            f"{self.api}/create-chat-thread",
            json=data,
            headers=self.headers)
        return request.json()

    # thread check, useless function
    def thread_check(self, ndc_Id):
        data = {"ndcId": f"x{ndc_Id}"}
        request = requests.post(
            f"{self.api}/thread-check",
            json=data,
            headers=self.headers)
        return request.json()

    # get live layer
    def get_live_layer(self, ndc_Id):
        request = requests.get(
            f"{self.api}/x{ndc_Id}/s/live-layer/homepage?v=2",
            headers=self.headers)
        return request.json()

    # link translation
    def link_translation(
            self,
            ndc_Id,
            user_Id: str = None,
            blog_Id: str = None,
            wiki_Id: str = None,
            thread_Id: str = None):
        data = {"ndcId": f"x{ndc_Id}"}
        if user_Id:
            data["objectId"] = user_Id
            data["objectType"] = 0
        elif blog_Id:
            data["objectId"] = blog_Id
            data["objectType"] = 1
        elif wiki_Id:
            data["objectId"] = wiki_Id
            data["objectType"] = 2
        elif thread_Id:
            data["objectId"] = thread_Id
            data["objectType"] = 12
        request = requests.post(
            f"{self.api}/link-translation",
            json=data,
            headers=self.headers)
        return request.json()

    # get chat bubbles list
    def get_bubbles_list(self):
        request = requests.get(
            f"{self.api_p}/g/s/chat/chat-bubble",
            headers=self.headers)
        return request.json()

    # get chat bubbles templates list
    def get_bubbles_templates_list(self):
        request = requests.get(
            f"{self.api_p}/g/s/chat/chat-bubble/templates",
            headers=self.headers)
        return request.json()

    # get avatar frames list
    def get_avatar_frames_list(self, start: int = 0, size: int = 10):
        request = requests.get(
            f"{self.api_p}/g/s/avatar-frame?start={start}&size={size}",
            headers=self.headers)
        return request.json()

    # apply avatar frame
    def apply_avatar_frame(self, ndc_Id, frame_Id: str, apply_to_all: int = 0):
        data = {"frameId": frame_Id, "applyToAll": apply_to_all}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/avatar-frame/apply",
            json=data,
            headers=self.headers)
        return request.json()

    # edit profile
    def edit_profile(
            self,
            ndc_Id,
            nickname: str = None,
            content: str = None,
            icon: str = None,
            background_color: str = None):
        data = {}
        if nickname:
            data["nickname"] = nickname
        if content:
            data["content"] = content
        if icon:
            data["icon"] = icon
        if background_color:
            data["extensions"] = {
                "style": {
                    "backgroundColor": background_color}}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/user-profile/{self.user_Id}",
            json=data,
            headers=self.headers)
        return request.json()

    # delete chat
    def delete_thread(self, ndc_Id, thread_Id: str):
        request = requests.delete(
            f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}",
            headers=self.headers)
        return request.json()

    # get wallet coin history info
    def wallet_coin_history(self, start: int = 0, size: int = 10):
        request = requests.get(
            f"{self.api_p}/g/s/wallet/coin/history?start={start}&size={size}",
            headers=self.headers)
        return request.json()

    # edit thread(chat)
    def edit_thread(
            self,
            ndc_Id,
            thread_Id: str,
            title: str = None,
            content: str = None,
            fans_only: bool = None):
        data = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if fans_only:
            data["extensions"] = {"fansOnly": fans_only}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}",
            json=data,
            headers=self.headers)
        return request.json()

    # get account info
    def get_account_info(self):
        request = requests.get(
            f"{self.api_p}/g/s/account",
            headers=self.headers)
        return request.json()

    # get user followers
    def get_user_followers(
            self,
            ndc_Id,
            user_Id: str,
            start: int = 0,
            size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile/{user_Id}/member?start={start}&size={size}",
            headers=self.headers)
        return request.json()

    # get user following
    def get_user_following(
            self,
            ndc_Id,
            user_Id: str,
            start: int = 0,
            size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile/{user_Id}/joined?start={start}&size={size}",
            headers=self.headers)
        return request.json()

    # search user or users in community
    def search_users(
            self,
            ndc_Id,
            nickname: str,
            start: int = 0,
            size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile?type=name&q={nickname}&start={start}&size={size}",
            headers=self.headers)
        return request.json()

    # get blog categories
    def blog_category(self, ndc_Id: str):
        request = requests.get(
            f"{self.api}/get-blog-category?ndcId={ndc_Id}",
            headers=self.headers)
        return request.json()

    # get community info
    def community_info(self, ndc_Id: str):
        request = requests.get(
            f"{self.api_p}/g/s-x{ndc_Id}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount",
            headers=self.headers)
        return request.json()

    # post blog function. don't work (in development...)
    def create_blog(
            self,
            ndc_Id,
            title: str,
            content: str = None,
            categories_list: list = None,
            extensions: dict = None,
            fans_only: bool = False,
            type: int = 0):
        media_list = []
        data = {
            "postJSON":
                {"title": title,
                 "content": content,
                 "type": type,
                 "mediaList": media_list,
                 "extensions": extensions,
                 "ndcId": ndc_Id,
                 "recaptcha_challenge": self.generate_captcha()
                 }}
        if fans_only:
            data["extensions"] = {"fansOnly": fans_only}
        if categories_list:
            data["taggedBlogCategoryIdList"] = categories_list
        request = requests.post(
            f"{self.api}/blog",
            json=data,
            headers=self.headers)
        return request.json()

    # delete blog
    def delete_blog(self, ndc_Id: str, blog_Id: str):
        data = {
            "ndcId": f"x{ndc_Id}",
            "postId": blog_Id,
            "postType": "blog"
        }
        request = requests.post(
            f"{self.api}/post/delete",
            json=data,
            headers=self.headers)
        return request.json()

    # get members(users) in chat
    def members_in_thread(
            self,
            ndc_Id: str,
            thread_Id: str,
            type: str = "default",
            start: int = 0,
            size: int = 10):
        data = {
            "ndcId": f"x{ndc_Id}",
            "threadId": thread_Id,
            "type": type,
            "start": start,
            "size": size
        }
        request = requests.post(
            f"{self.api}/members-in-thread",
            json=data,
            headers=self.headers)
        return request.json()

    # get user visitors
    def get_user_visitors(self, ndc_Id: str, user_Id: str):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/user-profile/{user_Id}/visitors",
            headers=self.headers)
        return request.json()

    # configure account settings
    # gender: 1 = male, 2 = female, 255 = non-binary
    def configure_account(self, age: int, gender: int):
        data = {"age": age, "gender": gender}
        request = requests.post(
            f"{self.api_p}/g/s/persona/profile/basic",
            json=data,
            headers=self.headers)
        return request.json()

    # get chat messages
    def get_thread_messages(self, ndc_Id: str, thread_Id: str, size: int = 10):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}/message?v=2&pagingType=t&size={size}",
            headers=self.headers)
        return request.json()

    # set activity status
    # 1 - online, 2 - offline
    def set_activity_status(self, ndc_Id: str, status: int = 1):
        data = {"onlineStatus": status, "duration": 86400}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/user-profile/{self.user_Id}/online-status",
            json=data,
            headers=self.headers)
        return request.json()

    # invite user or users to chat
    def invite_to_thread(self, ndc_Id: str, thread_Id: str, user_Id: str):
        data = {"uids": user_Id}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}/member/invite",
            json=data,
            headers=self.headers)
        return request.json()

    # invite user or users to voice
    def invite_to_vc(self, ndc_Id: str, thread_Id: str, user_Id: str):
        data = {"uid": user_Id}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}/vvchat-presenter/invite",
            json=data,
            headers=self.headers)
        return request.json()

    # send coins to blog, chat, or object
    def send_coins(
            self,
            ndc_Id: str,
            coins: int,
            blog_Id: str = None,
            thread_Id: str = None,
            object_Id: str = None,
            transaction_Id: str = None):
        link = None
        if transaction_Id is None:
            transaction_Id = str(uuid4())
        data = {
            "coins": coins,
            "tippingContext": {
                "transactionId": transaction_Id}}
        if blog_Id is not None:
            link = f"{self.api_p}/x{ndc_Id}/s/blog/{blog_Id}/tipping"
        if thread_Id is not None:
            link = f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}/tipping"
        if object_Id is not None:
            data["objectId"] = object_Id
            data["objectType"] = 2
            link = f"{self.api_p}/x{ndc_Id}/s/tipping"
        if link is None:
            print("Dumbass you didn't fill out the link in send_coins")
        request = requests.post(link, json=data, headers=self.headers)
        return request.json()

    # invite user or users by host
    def invite_by_host(self, ndc_Id: str, thread_Id: str, user_Id: str):
        data = {"uidList": user_Id}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}/avchat-members",
            json=data,
            headers=self.headers)
        return request.json()

    # watch ad and get 2-3 coins.
    def watch_ad(self):
        request = requests.post(
            f"{self.api_p}/g/s/wallet/ads/video/start",
            headers=self.headers)
        return request.json()

    # get thread(chat)
    def get_thread(self, ndc_Id: str, thread_Id: str):
        request = requests.get(
            f"{self.api_p}/x{ndc_Id}/s/chat/thread/{thread_Id}",
            headers=self.headers)
        return request.json()

    # check in
    def check_In(self, ndc_Id: str, time_zone: int = -
                 int(time.timezone) // 1000):
        data = {"timezone": time_zone}
        request = requests.post(
            f"{self.api_p}/x{ndc_Id}/s/check-in",
            json=data,
            headers=self.headers)
        return request.json()

    # claim new user coupon
    def claim_new_user_coupon(self):
        request = requests.post(
            f"{self.api_p}/g/s/coupon/new-user-coupon/claim",
            headers=self.headers)
        return request.json()

    # get blog votes
    def get_blog_votes(self, ndc_Id: str, blog_Id: str):
        request = requests.get(
            f"{self.api}/x{ndc_Id}/blog/{blog_Id}/votes",
            headers=self.headers)
        return request.json()

    # poll option
    def poll_option(self, ndc_Id: str, blog_Id: str, option_Id: str):
        request = requests.post(
            f"{self.api}/poll-option/x{ndc_Id}/{blog_Id}/{option_Id}/vote",
            headers=self.headers)
        return request.json()

    # search community
    def search_community(self, title: str, start: int = 0, size: int = 10):
        data = {"q": title, "start": start, "size": size}
        request = requests.post(
            f"{self.api_p}/g/s/community/search?q={title}&start={start}&size={size}",
            json=data,
            headers=self.headers)
        return request.json()

        return request.json()
