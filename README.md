# AminoLab
AminoLab Api For https://aminoapps.com
using https://aminoapps.com/api

![AminoLab](https://play-lh.googleusercontent.com/DxURGS6RxF4zwTczWWsPwvaCAHcFUdaJH2JufTAq4fmq6vP4g1ec-U0UweTO-mNtXA=h500)

### Installing
`pip install AminoLab`

### Example
```python3
#Login
import AminoLab
client = AminoLab.Client()
email = input("Email >> ")
password = input("Password >> ")
client.auth(email=email, password=password)
```
