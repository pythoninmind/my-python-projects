***
Features i want to add: 
Filter for bills
PDF-recognition
automatically moving to directory
Dashboard with Streamlit
***
import imaplib
import email
from email.header import decode_header
import os
import pandas as pd

# ===== Konfiguration =====
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "your_email@gmail.com"
EMAIL_PASSWORD = "app_passwort"

ATTACHMENT_FOLDER = "attachments"

# create directory
os.makedirs(ATTACHMENT_FOLDER, exist_ok=True)

# establish connection
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

mail.select("INBOX")

status, messages = mail.search(None, "ALL")

email_ids = messages[0].split()

report_data = []

for email_id in email_ids[-20:]:

    status, msg_data = mail.fetch(email_id, "(RFC822)")

    for response_part in msg_data:

        if isinstance(response_part, tuple):

            msg = email.message_from_bytes(response_part[1])

            subject = msg["Subject"]
            sender = msg["From"]
            date = msg["Date"]

            if subject:
                decoded_subject, encoding = decode_header(subject)[0]

                if isinstance(decoded_subject, bytes):
                    subject = decoded_subject.decode(
                        encoding if encoding else "utf-8",
                        errors="ignore"
                    )

            attachment_count = 0

            for part in msg.walk():

                filename = part.get_filename()

                if filename:

                    attachment_count += 1

                    filepath = os.path.join(
                        ATTACHMENT_FOLDER,
                        filename
                    )

                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))

            report_data.append({
                "Sender": sender,
                "Subject": subject,
                "Date": date,
                "Attachments": attachment_count
            })

# create excel-report
df = pd.DataFrame(report_data)

excel_file = "email_report.xlsx"

with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False,
        sheet_name="E-Mail Report"
    )

print(
    f"Report created: {excel_file}"
)

mail.logout()
