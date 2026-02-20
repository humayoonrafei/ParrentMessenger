import time
import gspread  # to connect to google sheets
from google.oauth2.service_account import Credentials
from twilio.rest import Client
import twilio_confirguration
from twilio_confirguration import account_sid, auth_token, twilio_number

def process_messages(parrent_name, name, Note):
    sliced_name_parent = parrent_name.split(" ")[0]
    sliced_name_student = name.split(" ")[-1].capitalize()
    return f" Dear {sliced_name_parent},  {sliced_name_student}'s  Algebra success Teacher has a message for you. {Note}"


def send_message(phone, message_to_be_sent):
    twilio_client = Client(twilio_confirguration.account_sid, twilio_confirguration.auth_token)   
    try:
     twilio_client.messages.create(
        to=phone,
        from_=twilio_confirguration.twilio_number,
        body=message_to_be_sent,
    )
   
  
    except Exception as e:
        print(f"Error sending message to {phone}: {e}")
        return False

# Connect to Google Sheets
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("parent-messenger-487820-03c4e4e5a294.json", scopes=scopes)
client = gspread.authorize(creds)

worksheet_name = "Student_Automation"
sheet_name_parent = "Parent Contact Info"
sheet = client.open(worksheet_name).worksheet(sheet_name_parent)


# get the data from the sheet
# if the header row has duplicates, use the raw data by column index
# if the header row has no duplicates, use the get_all_records() method

try:
    students = sheet.get_all_records()
except Exception:
    # Fallback when header row has duplicates - use raw data by column index
    data = sheet.get_all_values()
    students = []
    if len(data) > 1:
        for row in data[1:]:
            if len(row) >= 4 and row[0]:  # Has student name
                students.append({
                    "Student Name": row[0], "Parent Number": row[1],
                    "Notes": row[2], "Parent Name": row[3]
                })

def run_parent_alerts():
    # 1. Get the data
    try:
        students = sheet.get_all_records()
    except Exception:
        # (Your fallback logic here...)
        pass

    # 2. Process the loop
    for i, student in enumerate(students, start=2):
        # We use i to keep track of the ROW number for updating later
        
        status = student.get("Message_Status") or student.get("Status")
        
        if status != "Pending":
            print(f"Skipping {student.get('sliced_name_student')} - Already {status}")
            continue

        # Extract data
        phone = student.get("Parent Number")
        parent_name = student.get("Parent Name")
        student_name = student.get("Student Name")
        note = student.get("Notes")

        if not student_name or not parent_name:
            continue

        # Generate and Send
        message = process_messages(parent_name, student_name, note)
        print(f"Sending to {student_name}'s parent...")
        
        success = send_message(phone, message)

        # 3. Update the Status
        if success:
            # Change '5' to the actual column number of your Status column
            sheet.update_cell(i, 5, "Sent")
            print("Status updated to Sent.")

        time.sleep(1)

# This is the "Entry Point" of your program
if __name__ == "__main__":
    print("🚀 Starting Automation...")
    run_parent_alerts()
    print("✅ All done!")