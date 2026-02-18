import gspread
from google.oauth2.service_account import Credentials

# 1. Define what we are allowed to do (Scopes)
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 2. Tell Python where your "ID Card" (the JSON file) is
# Make sure the filename matches exactly what is in your folder!
creds = Credentials.from_service_account_file("parent-messenger-487820-03c4e4e5a294.json", scopes=scopes)
client = gspread.authorize(creds)

# 3. Open the sheet by its name
# Replace "Student_Automation" with the EXACT name of your Google Sheet
worksheet_name = "Student_Automation"
sheet_name_parent = "Parent Contact Info"
sheet = client.open(worksheet_name).worksheet(sheet_name_parent)




# 4. Pull the data and print it
print("--- Connection Successful! ---")
try:
    students = sheet.get_all_records()
    for student in students:
        name = student.get("Student_Name") or student.get("Student Name") or list(student.values())[0]
     
        phone = student.get("Parent Number") or student.get("Parent number") or list(student.values())[1]
        Note = student.get("Custom Notes") or student.get("Notes") or list(student.values())[2]

        parrent_name = student.get("Parent Name") or student.get("Parent name") or list(student.values())[3]
        
        # take the first name of the parent
        sliced_name_parent = parrent_name.split(" ")[0]
        # take the first name of the student and capitalize it and if it is more than two names take the first name.
        sliced_name_student = name.split(" ")[-1].capitalize()

        message_to_be_sent = f" Dear {sliced_name_parent},  {sliced_name_student}'s  Algebera success Teacher has a message for you. {Note}"
        print(message_to_be_sent)
    
    
except Exception as e:
    # Fallback if header row has duplicates - get raw data
    data = sheet.get_all_values()
    if len(data) > 1:
        for row in data[1:]:  # Skip header
            if row:
                print(f"Found Student: {row[0]}")
    else:
        print(f"(Sheet structure note: {e})")
    