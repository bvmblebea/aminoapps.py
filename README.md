# AminoLab
AminoLab Api For AminoApps using aminoapps.com/api

### Installing
`pip install AminoLab`

### Example
```python3
#Login
import aminolab
client = aminolab.Client()
email = input("Email >> ")
password = input("Password >> ")
client.auth(email=email, password=password)
```
