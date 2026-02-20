from twilio.rest import Client
import twilio_confirguration
from twilio_confirguration import account_sid, auth_token, twilio_number


def smoke_test():
    client = Client(twilio_confirguration.account_sid, twilio_confirguration.auth_token)
    
    print(f"🚀 Attempting to send a single test message to 2088844...")
    
    try:
        message = client.messages.create(
            body="Smoke Test: Mr. Rafei, your Python script is officially talking to the world! 🚀",
            from_=twilio_number,
            to='+19162088844'
        )
        print(f"✅ SUCCESS! Message SID: {message.sid}")
        print("Check your phone now!")
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    smoke_test()