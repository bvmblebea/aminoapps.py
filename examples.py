#login
import aminolab
client = aminolab.Client()
client.auth(email="email", password="password")

#login with input
import aminolab
client = aminolab.Client()
email = input("Email >> ")
password = input("Password >> ")
client.auth(email=email, password=password)

#follow user
import aminolab
client = aminolab.Client()
client.auth(email=email, password=password)
client.follow_user(ndcId="ndcId", followee_id="userId")

#unfollow_user
import aminolab
client = aminolab.Client()
client.auth(email=email, password=password)
client.unfollow_user(ndcId="ndcId", followee_id="userId")
