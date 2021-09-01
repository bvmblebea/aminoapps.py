#login
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")

#login with phonenumber
import AminoLab
client = AminoLab.Client()
client.auth(phone="phonenumber", password="password")

#login with email input
import AminoLab
client = AminoLab.Client()
email = input("Email >> ")
password = input("Password >> ")
client.auth(email=email, password=password)

#login with phonenumber input
import AminoLab
client = AminoLab.Client()
phonenumber = input("PhoneNumber >> ")
password = input("Password >> ")
client.auth(phone=phonenumber, password=password)

#follow user
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
client.follow_user(ndcId="ndcId", followee_id="userId")

#unfollow_user
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
client.unfollow_user(ndcId="ndcId", followee_id="userId")

#get public communities list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
clients = client.get_public_communities(language="en", size=100)
for x, name in enumerate(clients.name, 1):
	print(f"{x}.{name}")
ndcId = clients.ndcId[int(input("Select the community >> "))-1]

#get joined communities list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
clients = client.my_communities()
for x, name in enumerate(clients.name, 1):
	print(f"{x}.{name}")
ndcId = clients.ndcId[int(input("Select the community >> "))-1]

#get public chats list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
chats = client.get_public_chat_threads(ndcId="ndcId", size="size")
for z, title in enumerate(chats.title, 1):
	print(f"{z}.{title}")
chatx = chats.threadId[int(input("Select The Chat >> "))-1]

#get joined chats list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
chats = client.my_chat_threads(ndcId="ndcId", size="size")
for z, title in enumerate(chats.title, 1):
	print(f"{z}.{title}")
chatx = chats.threadId[int(input("Select The Chat >> "))-1]
