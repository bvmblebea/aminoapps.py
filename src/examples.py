#login
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")

#login with phonenumber
import AminoLab
client = AminoLab.Client()
client.auth(phone="phone_number", password="password")

#login with email input
import AminoLab
client = AminoLab.Client()
email = input("Email >> ")
password = input("Password >> ")
client.auth(email=email, password=password)

#login with phonenumber input
import AminoLab
client = AminoLab.Client()
phone_number = input("Phone Number >> ")
password = input("Password >> ")
client.auth(phone=phone_number, password=password)

#follow user
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
client.follow_user(ndc_Id="ndc_Id", user_Id="user_Id")

#unfollow_user
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
client.unfollow_user(ndc_Id="ndc_Id", user_Id="user_Id")

#get public communities list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
clients = client.get_public_communities(language="en", size=100)
for x, name in enumerate(clients.name, 1):
	print(f"{x}.{name}")
ndc_Id = clients.ndc_Id[int(input("Select the community >> "))-1]

#get joined communities list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
clients = client.my_communities()
for x, name in enumerate(clients.name, 1):
	print(f"{x}.{name}")
ndc_Id = clients.ndc_Id[int(input("Select the community >> "))-1]

#get public chats list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
chats = client.get_public_chat_threads(ndc_Id="ndc_Id", size="size")
for z, title in enumerate(chats.title, 1):
	print(f"{z}.{title}")
thread_Id = chats.thread_Id[int(input("Select The Chat >> "))-1]

#get joined chats list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
chats = client.my_chat_threads(ndc_Id="ndc_Id", size="size")
for z, title in enumerate(chats.title, 1):
	print(f"{z}.{title}")
thread_Id = chats.thread_Id[int(input("Select The Chat >> "))-1]
