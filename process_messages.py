import time
import gspread  # to connect to google sheets
from google.oauth2.service_account import Credentials


def process_messages(parrent_name, name, Note):
    sliced_name_parent = parrent_name.split(" ")[0]
    sliced_name_student = name.split(" ")[-1].capitalize()
    return f" Dear {sliced_name_parent},  {sliced_name_student}'s  Algebra success Teacher has a message for you. {Note}"


def send_message(phone, message_to_be_sent):
    # send the message to the parent using twilio
    print(f"Sending message to {phone}: {message_to_be_sent}")
    return True


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

for student in students:
    phone = student.get("Parent Number") or student.get("Parent number") or (list(student.values())[1] if len(student) > 1 else "")
    parrent_name = student.get("Parent Name") or student.get("Parent name") or (list(student.values())[3] if len(student) > 3 else "")
    name = student.get("Student Name") or student.get("Student name") or (list(student.values())[0] if student else "")
    Note = student.get("Custom Notes") or student.get("Notes") or (list(student.values())[2] if len(student) > 2 else "")

    if not name or not parrent_name:
        continue  # Skip header/metadata rows

    message_to_be_sent = process_messages(parrent_name, name, Note)
    print(message_to_be_sent)
    send_message(phone, message_to_be_sent)
    time.sleep(1)

