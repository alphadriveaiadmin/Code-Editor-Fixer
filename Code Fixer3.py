import streamlit as st
import json
import re

st.set_page_config(page_title="Voice Call Trigger", layout="wide")

st.title("Voice Call Trigger Generator")

# Text area for JSON input
input_json = st.text_area("Paste JSON Input Here", height=400)

if st.button("Generate Trigger"):
    try:
        data = json.loads(input_json)

        # Convert entire JSON to string for scanning
        raw_text = json.dumps(data)

        # Regex: find 10-digit phone numbers anywhere (with optional +1, optional spaces)
        phone_numbers = re.findall(r'\+?1?\s?(\d{10})', raw_text)

        # Clean numbers (strip spaces, ensure uniqueness)
        unique_numbers = set(num.strip() for num in phone_numbers)

        # Create both plain and +1 formats
        allowed_numbers = []
        for num in unique_numbers:
            allowed_numbers.append(num)
            allowed_numbers.append(f"+1{num}" if not num.startswith("+1") else num)

        trigger = f"""@trigger voice.call_received(phoneNumber=params['phone_number'], start_function={{"name":"start_function","url":"{data['virtual_agent_url']}/gs-appointment-api/lookupCustomer?dealerId={data['virtual_agent_dealer_code']}","auth":{{"username":"dga_scheduler","password":"Green3Red4Blue"}}}}, allowedTransferNumbers={allowed_numbers}, start_sentence=params["first_sentence"], objective=params["objective"], functions=params['tools'], voiceId="11labs-Cimo", model='gpt-4o', sensitivity="0.7", timezone="{data['dealership_timezone']}", language='multi')
def wf(obj):
    data = extract.extract_from_features(obj=obj['transcript'], features=features, featuresToExtract=['first_name', 'last_name', 'sentiment', 'email_address', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'appointment_date', 'summary', 'disposition', 'disposition_id', 'transportation_type',  'callback_time', 'callback', 'has_multiple_accounts', 'book_appointment_error'])
    data["transcript"] = obj["transcript"]
    data['start_time'] = obj['start_timestamp']
    data['end_time'] = obj['end_timestamp']
    data["recording"] = obj["recording_url"]
    data["call_status"] = obj["call_status"]
    data['phone_number'] = obj['from_number']

    call_id = RANDOM(8).generate()
    row_id = RANDOMINT(5).generate()
    print(call_id)
    data['call_id'] = call_id
    insertRow(data)
    api.post_req(url ="https://apps.dgaauto.com/lucyWebhookAlert/webhook", data ={{"campaign_id": {data['campaign_id']}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {data['dealership_id']}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data['vehicle_make']}})
    api.post_req(url ="https://webhook.site/bcaf7914-929e-495e-bcff-5ab35a9f436c", data ={{"campaign_id": {data['campaign_id']}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {data['dealership_id']}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data['vehicle_make']}})
    console.log("reporting")
    reporting_res = api.post_req(url ="https://apps.dgaauto.com/virtualAgentDataImport/webhook", headers={{"x-api-key": "$2a$11$5GHNF.BbEILij03XRr163eV0lrbRGu6Rq.jlycXAvB.fddAZkO5GK"}}, data={{"id": row_id, "campaign_id": {data['campaign_id']},  "recording": data["recording"], "transcript": data['transcript'], "api_logs":obj['functions'], "call_status": data['call_status'], "call_id": data['call_id'], "start_time": data['start_time'], "end_time": data['end_time'], "first_name": data["first_name"], "last_name": data["last_name"], "phone_number": data["phone_number"], "sentiment": data["sentiment"], "email_address": data["email_address"], "vehicle_make": data["vehicle_make"], "vehicle_model": data["vehicle_model"], "vehicle_year": data["vehicle_year"], "appointment_date": data["appointment_date"], "summary": data["summary"], "disposition": data["disposition"], "disposition_id": data["disposition_id"], "transportation_type": data["transportation_type"], "callback_time": data["callback_time"], "callback": data["callback"], "has_multiple_accounts": data["has_multiple_accounts"], "book_appointment_error": data["book_appointment_error"]}})
    console.log(reporting_res)
    s3.upload_file_from_url(url=obj["recording_url"], imageName=f"{{call_id}}-{data['dealership_id']}", fileExtension="wav")"""

        st.code(trigger, language="python")
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
