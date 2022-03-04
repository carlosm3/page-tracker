from twilio.rest import Client

from keys import twilio as tw

account_sid = tw["account"]
auth_token = tw["token"]
client = Client(account_sid, auth_token)


def sms(message):
    client.messages.create(
        body=message,
        from_='',
        to=''
    )
