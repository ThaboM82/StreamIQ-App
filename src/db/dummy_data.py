# src/db/dummy_data.py
# Centralized dummy datasets for demo fallback (South African context, polished)

# --- Call Center ---
dummy_callcenter = [
    {"CallID": "C001", "Agent": "Thabo M.", "Customer": "Nomsa K.", "Duration": "6 min", "Issue": "Loan repayment query"},
    {"CallID": "C002", "Agent": "Lerato P.", "Customer": "Sipho D.", "Duration": "8 min", "Issue": "Credit card limit increase"},
    {"CallID": "C003", "Agent": "Mandla S.", "Customer": "Ayanda N.", "Duration": "5 min", "Issue": "Insurance claim follow‑up"},
    {"CallID": "C004", "Agent": "Thabo M.", "Customer": "Kabelo R.", "Duration": "7 min", "Issue": "Account balance enquiry"},
    {"CallID": "C005", "Agent": "Lerato P.", "Customer": "Zanele T.", "Duration": "9 min", "Issue": "Home loan application"},
]

# --- Claims (Amounts in South African Rand) ---
dummy_claims = [
    {"ClaimID": "CL001", "ClaimType": "Auto", "Amount": "R 12,500.00", "Status": "Pending", "Customer": "Nomsa K."},
    {"ClaimID": "CL002", "ClaimType": "Health", "Amount": "R 8,000.00", "Status": "Approved", "Customer": "Sipho D."},
    {"ClaimID": "CL003", "ClaimType": "Home", "Amount": "R 20,000.00", "Status": "Rejected", "Customer": "Ayanda N."},
    {"ClaimID": "CL004", "ClaimType": "Auto", "Amount": "R 15,750.00", "Status": "Pending", "Customer": "Kabelo R."},
    {"ClaimID": "CL005", "ClaimType": "Health", "Amount": "R 9,500.00", "Status": "Approved", "Customer": "Zanele T."},
]

# --- Big Data ---
dummy_bigdata = [
    {"RecordID": "R001", "Category": "Finance", "Value": "R 250.00"},
    {"RecordID": "R002", "Category": "Retail", "Value": "R 120.00"},
    {"RecordID": "R003", "Category": "Insurance", "Value": "R 300.00"},
    {"RecordID": "R004", "Category": "Banking", "Value": "R 450.00"},
    {"RecordID": "R005", "Category": "Telecom", "Value": "R 200.00"},
    {"RecordID": "R006", "Category": "Mining", "Value": "R 180.00"},
    {"RecordID": "R007", "Category": "Insurance", "Value": "R 275.00"},
    {"RecordID": "R008", "Category": "Banking", "Value": "R 500.00"},
]

# --- Multilingual (South African languages + English) ---
dummy_multilingual = [
    {"Text": "Hello, how are you?", "Language": "English"},
    {"Text": "Sawubona, unjani?", "Language": "isiZulu"},
    {"Text": "Dumelang, le kae?", "Language": "Sepedi"},
    {"Text": "Xewani, ku njhani?", "Language": "Xitsonga"},
    {"Text": "Ngiyabonga kakhulu", "Language": "isiZulu"},
    {"Text": "Ke a leboga", "Language": "Sepedi"},
    {"Text": "Ndza khensa ngopfu", "Language": "Xitsonga"},
    {"Text": "Goeie môre", "Language": "Afrikaans"},
    {"Text": "Molo, unjani?", "Language": "isiXhosa"},
    {"Text": "Dumelang bagaetsho", "Language": "Setswana"},
]

# --- Speech-to-Text ---
dummy_transcriptions = [
    {"timestamp": "2026-04-29 06:15:00", "file_name": "demo.wav", "transcription": "Hello, this is a demo call."},
    {"timestamp": "2026-04-29 06:16:00", "file_name": "meeting.mp3", "transcription": "We need to finalize the report by Friday."},
    {"timestamp": "2026-04-29 06:17:00", "file_name": "customer.m4a", "transcription": "The customer requested a refund for the last order."},
    {"timestamp": "2026-04-29 06:18:00", "file_name": "isiZulu_sample.wav", "transcription": "Sawubona, ngicela usizo."},
]

# --- Audit Logs ---
dummy_auditlogs = [
    {"timestamp": "2026-04-29 06:00:00", "event": "Login", "user": "Percy", "ip": "192.168.1.10"},
    {"timestamp": "2026-04-29 06:05:00", "event": "Viewed Call Center Demo", "user": "Percy", "ip": "192.168.1.10"},
    {"timestamp": "2026-04-29 06:10:00", "event": "Viewed Claims Demo", "user": "Percy", "ip": "192.168.1.10"},
    {"timestamp": "2026-04-29 06:15:00", "event": "Viewed Big Data Demo", "user": "Percy", "ip": "192.168.1.10"},
    {"timestamp": "2026-04-29 06:20:00", "event": "Transcribed Audio", "user": "Percy", "ip": "192.168.1.10"},
]

# --- Banking / Insurance / Call Center NLP samples ---
dummy_bank_records = [
    {"CustomerID": "B001", "AccountType": "Savings", "Balance": "R 5,000.00"},
    {"CustomerID": "B002", "AccountType": "Checking", "Balance": "R 1,200.00"},
    {"CustomerID": "B003", "AccountType": "Loan", "Balance": "R -15,000.00"},
]

dummy_insurance_records = [
    {"PolicyID": "P001", "PolicyType": "Life", "Premium": "R 450.00"},
    {"PolicyID": "P002", "PolicyType": "Auto", "Premium": "R 300.00"},
    {"PolicyID": "P003", "PolicyType": "Health", "Premium": "R 600.00"},
]

dummy_callcenter_nlp = [
    {"TranscriptID": "T001", "Text": "Customer asked about loan repayment options."},
    {"TranscriptID": "T002", "Text": "Caller reported a car accident claim."},
    {"TranscriptID": "T003", "Text": "Agent explained savings account interest rates."},
]
