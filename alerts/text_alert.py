from twilio.rest import Client

def text_alert(msg):
	client = Client("<key1>", "<key2>")

	client.messages.create(to = ["<mobile number with country code>"], from_ = "<dummy client number>", body = msg)


