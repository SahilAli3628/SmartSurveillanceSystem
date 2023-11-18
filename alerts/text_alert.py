from twilio.rest import Client

def text_alert(msg):
	client = Client("AC5be4774cd9efd92f16f757c83abbf719", "604a168faa92f2551821a81e9302ceaa")

	client.messages.create(to = ["<mobile number with country code>"], from_ = "+16065352966", body = msg)


