import streamlit as st
import re
import requests
from random import randint
import time

st.set_page_config(page_title="DGA Transfer Numbers Generator", layout="wide")

# ---- Helper Functions ----
def RANDOM(n=8):
    return ''.join([str(randint(0, 9)) for _ in range(n)])

def RANDOMINT(n=5):
    return randint(10**(n-1), (10**n)-1)

def clean_phone(num):
    """Strip non-digits, return cleaned and +1 format"""
    clean = re.sub(r'\D', '', str(num))
    if not clean:
        return []
    results = [clean]
    if not clean.startswith("1"):
        results.append(f"+1{clean}")
    else:
        results.append(f"+{clean}")
    return results

def extract_allowed_numbers(obj):
    """Collects all possible phone numbers from obj"""
    fields = ['from_number', 'to_number', 'transfer_numbers', 'extra_numbers']
    all_nums = set()
    for f in fields:
        if f in obj:
            if isinstance(obj[f], list):
                for n in obj[f]:
                    for val in clean_phone(n):
                        all_nums.add(val)
            else:
                for val in clean_phone(obj[f]):
                    all_nums.add(val)
    return list(all_nums)

# ---- Streamlit UI ----
st.title("DGA Transfer Numbers Generator")

# Simulated inputs
params = {
    "phone_number": st.text_input("Incoming Phone Number", "7042302072"),
    "first_sentence": st.text_input("First Sentence", "Hello, how can I help you today?"),
    "objective": st.text_input("Objective", "Book a service appointment"),
    "tools": ["lookup_customer", "book_appointment"]
}

# Simulated object input (replace with real webhook data in production)
obj = {
    "from_number": params["phone_number"],
    "to_number": "7048381300",
    "transfer_numbers": ["7046597032", "7046597036"],
    "transcript": "Customer wants to book an appointment",
    "start_timestamp": time.time(),
    "end_timestamp": time.time() + 300,
    "recording_url": "https://example.com/recording.wav",
    "call_status": "completed",
    "functions": {"lookup": "ok"}
}

features = ['first_name', 'last_name', 'sentiment', 'email_address', 'vehicle_make', 'vehicle_model', 'vehicle_year',
            'appointment_date', 'summary', 'disposition', 'disposition_id', 'transportation_type', 'callback_time',
            'callback', 'has_multiple_accounts', 'book_appointment_error']

# Generate allowed numbers
allowedTransferNumbers = extract_allowed_numbers(obj)

# ---- Output Trigger ----
st.subheader("Generated Trigger Code:")
st.code(f"""@trigger voice.call_received(phoneNumber=params['phone_number'], start_function={{"name":"start_function","url":"https://randy-marion-buick-gmc.techwall.us/gs-appointment-api/lookupCustomer?dealerId=1","auth":{{"username":"dga_scheduler","password":"Green3Red4Blue"}}}}, allowedTransferNumbers={allowedTransferNumbers}, start_sentence=params["first_sentence"], objective=params["objective"], functions=params['tools'], voiceId="11labs-Cimo", model='gpt-4o', sensitivity="0.7", timezone="America/New_York", language='multi')
def wf(obj):
    data = extract.extract_from_features(obj=obj['transcript'], features=features, featuresToExtract={features})
    data["transcript"] = obj["transcript"]
    data['start_time'] = obj['start_timestamp']
    data['end_time'] = obj['end_timestamp']
    data["recording"] = obj["recording_url"]
    data["call_status"] = obj["call_status"]
    data['phone_number'] = obj['from_number']

    call_id = RANDOM(8)
    row_id = RANDOMINT(5)
    print(call_id)
    data['call_id'] = call_id
    insertRow(data)
    api.post_req(url="https://apps.dgaauto.com/lucyWebhookAlert/webhook", data={{"campaign_id":2620,"agent_comments":data['summary'],"call_back":data['callback'],"call_disposition_id":data["disposition_id"],"advisor":"","dealer_id":3075,"first_name":data['first_name'],"last_name":data["last_name"],"phone":data["phone_number"],"vehicle_year":data['vehicle_year'],"vehicle_model":data["vehicle_model"],"vehicle_make":data['vehicle_make']}})
    api.post_req(url="https://webhook.site/bcaf7914-929e-495e-bcff-5ab35a9f436c", data={{"campaign_id":2620,"agent_comments":data['summary'],"call_back":data['callback'],"call_disposition_id":data["disposition_id"],"advisor":"","dealer_id":3075,"first_name":data['first_name'],"last_name":data["last_name"],"phone":data["phone_number"],"vehicle_year":data['vehicle_year'],"vehicle_model":data["vehicle_model"],"vehicle_make":data['vehicle_make']}})
    console.log("reporting")
    reporting_res = api.post_req(url="https://apps.dgaauto.com/virtualAgentDataImport/webhook", headers={{"x-api-key":"$2a$11$5GHNF.BbEILij03XRr163eV0lrbRGu6Rq.jlycXAvB.fddAZkO5GK"}}, data={{"id":row_id,"campaign_id":2620,"recording":data["recording"],"transcript":data['transcript'],"api_logs":obj['functions'],"call_status":data['call_status'],"call_id":data['call_id'],"start_time":data['start_time'],"end_time":data['end_time'],"first_name":data["first_name"],"last_name":data["last_name"],"phone_number":data["phone_number"],"sentiment":data["sentiment"],"email_address":data["email_address"],"vehicle_make":data["vehicle_make"],"vehicle_model":data["vehicle_model"],"vehicle_year":data["vehicle_year"],"appointment_date":data["appointment_date"],"summary":data["summary"],"disposition":data["disposition"],"disposition_id":data["disposition_id"],"transportation_type":data["transportation_type"],"callback_time":data["callback_time"],"callback":data["callback"],"has_multiple_accounts":data["has_multiple_accounts"],"book_appointment_error":data["book_appointment_error"]}})
    console.log(reporting_res)
    s3.upload_file_from_url(url=obj["recording_url"], imageName=f"{{call_id}}-3075", fileExtension="wav")""", language="python")
