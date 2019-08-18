# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC663b0f839179ecb7f9564716807bf4a3'
auth_token = '846374aa0e4a6e7bfc2c6a491f5624e3'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+5521976319861',
                        from_='+552139579317'
                    )

print(call.sid)