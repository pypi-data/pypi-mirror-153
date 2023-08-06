# Etpy
Etpy is a Reverse Engineering of MyEtisalat Masr android application
with this package you can control you etisalat number including cash wallet with python
```python
import from etpy import Client
client = Client("011xxxxxxxx") # here you must put your etisalat phone number
client.send_verification_code() # We are using this function to send verification code to procced the login request
client.login_with_code(input("Code ?  : ")) # here you must enter the verification code recevied on your phone
print(client.save_session) # Use this function to save session (for future login)
print(client.getbalance()) # Printing User Balance

```
## Installing Etpy
```console
$ python -m pip install etpy
```
## Suported Features
- OTP Login
- Session Login 
- Getting User Balance
- Rechage User Balance ``using scrach card``
- Getting Daily Gifts
- Redeeming Daily Gifts
- Getting Call Log 
- Getting Calling Numbers
- Getting ``011`` Offers
- Redeeming ``011`` Offers
- Cash Features
 - Getting Balance
 - Money Transfer
 - Waiting For Cash Payment
 - Getting Transcation History
### To do list
- Getting User usage and subscriptions
- Out of credit Service
    - Sallefny 3la nota 
    - Megabytes 3al nota
- Cash
    - Balance Rechrage
    - Generating Online Payments Cards
    - Cash Out
    - Purchase 
    - Bank to Wallet
 





