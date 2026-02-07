import streamlit as st
import json
import re

import requests

st.set_page_config(page_title="Code Editor Creator", layout="wide")

# ---------- Function to Extract Phone Numbers ----------
def extract_phone_numbers(text):
    # Finds phone numbers with optional +1 and strips spaces
    phone_pattern = r"(?:\+?1)?\d{10}"
    found_numbers = re.findall(phone_pattern, text.replace(" ", ""))

    # Preserve order & include both with +1 and without
    result = []
    seen = set()
    for num in found_numbers:
        base_num = num[-10:]  # last 10 digits
        variants = [base_num, f"+1{base_num}"]
        for v in variants:
            if v not in seen:
                result.append(v)
                seen.add(v)
    return result

# ---------- Home Page ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.title("Select Code Editor Creator")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("TechWall Code Editor Creator"):
            st.session_state.page = "techwall"
            st.rerun()
    with col2:
        if st.button("Xtime Code Editor Creator"):
            st.session_state.page = "xtime"
            st.rerun()
    with col3:
        if st.button("MyKaarma Code Editor Creator"):
            st.session_state.page = "mykaarma"
            st.rerun()

# ---------- TechWall Code Editor ----------
elif st.session_state.page == "techwall":
    st.title("TechWall Code Editor Creator")

    campaign_col, _ = st.columns([1, 3])
    with campaign_col:
        campaign_id = st.text_input(
            "Campaign ID",
            max_chars=4,
            placeholder="1234",
            help="Enter the 4-digit campaign ID for the webhook.",
        )
        
    raw_json = ""
    
    if st.button("Generate TW Code Editor"):
        if not campaign_id.strip():
            error_message = "Please enter a 4-digit campaign ID before generating."
        elif not campaign_id.isdigit() or len(campaign_id) != 4:
            error_message = "Campaign ID must be exactly 4 digits."
        else:
            try:
                response = requests.post(
                    "https://apps.dgaauto.com/virtualAgentData/webhook",
                    params={"campaign_id": campaign_id},
                    timeout=15,
                )
                response.raise_for_status()
                if response.headers.get("content-type", "").lower().startswith("application/json"):
                    raw_json = json.dumps(response.json())
                else:
                    raw_json = response.text
                    
            data = json.loads(raw_json)
            all_numbers = extract_phone_numbers(raw_json)

            trigger = f"""@trigger voice.call_received(wsBaseUrl="voicev1.onrender.com", phoneNumber=params['phone_number'], start_function={{"name":"start_function","url":"{data['virtual_agent_url']}/gs-appointment-api/lookupCustomer?dealerId={data['virtual_agent_dealer_code']}","auth":{{"username":"dga_scheduler","password":"Green3Red4Blue"}}}}, allowedTransferNumbers={all_numbers}, start_sentence=params["first_sentence"], objective=params["objective"], functions=params['tools'], voiceId="11labs-Cimo", model='gpt-4o', sensitivity="0.7", timezone="{data['dealership_timezone']}", language='multi')
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
    api.post_req(url ="https://apps.dgaauto.com/lucyWebhookAlert/webhook", data ={{"campaign_id": {data['campaign_id']}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {data['dealership_id']}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data["vehicle_make"]}})
    api.post_req(url ="https://webhook.site/bcaf7914-929e-495e-bcff-5ab35a9f436c", data ={{"campaign_id": {data['campaign_id']}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {data['dealership_id']}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data["vehicle_make"]}})
    console.log("reporting")
    reporting_res = api.post_req(url ="https://apps.dgaauto.com/virtualAgentDataImport/webhook", headers={{"x-api-key": "$2a$11$5GHNF.BbEILij03XRr163eV0lrbRGu6Rq.jlycXAvB.fddAZkO5GK"}}, data={{"id": row_id, "campaign_id": {data['campaign_id']}, "recording": data["recording"], "transcript": data['transcript'], "api_logs":obj['functions'], "call_status": data['call_status'], "call_id": data['call_id'], "start_time": data['start_time'], "end_time": data['end_time'], "first_name": data["first_name"], "last_name": data["last_name"], "phone_number": data["phone_number"], "sentiment": data["sentiment"], "email_address": data["email_address"], "vehicle_make": data["vehicle_make"], "vehicle_model": data["vehicle_model"], "vehicle_year": data["vehicle_year"], "appointment_date": data["appointment_date"], "summary": data["summary"], "disposition": data["disposition"], "disposition_id": data["disposition_id"], "transportation_type": data["transportation_type"], "callback_time": data["callback_time"], "callback": data["callback"], "has_multiple_accounts": data["has_multiple_accounts"], "book_appointment_error": data["book_appointment_error"]}})
    s3.upload_file_from_url(url=obj["recording_url"], imageName=f"{{call_id}}-{data['dealership_id']}", fileExtension="wav")"""
            st.code(trigger, language="python")
        except Exception as e:
            st.error(f"Error parsing JSON: {e}")

# ---------- Xtime Code Editor ----------
elif st.session_state.page == "xtime":
    st.title("Xtime Code Editor Creator")
    input_json = st.text_area("Paste JSON Input Here", height=400)
    if st.button("Generate Xtime Trigger"):
        try:
            data = json.loads(input_json)
            all_numbers = extract_phone_numbers(input_json)

            trigger = f"""@trigger voice.call_received(wsBaseUrl="voicev1.onrender.com", start_function=params['start_function'], generateBearerToken=params['bearer_token'], phoneNumber=params['phone_number'], allowedTransferNumbers={all_numbers}, start_sentence=params["first_sentence"], objective=params["objective"], functions=params['tools'], voiceId="11labs-Cimo", model='gpt-4o', sensitivity="0.7", timezone="America/New_York", language='multi')
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
    api.post_req(url ="https://apps.dgaauto.com/lucyWebhookAlert/webhook", data ={{"campaign_id": {data['campaign_id']}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {data['dealership_id']}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data["vehicle_make"]}})
    api.post_req(url ="https://webhook.site/bcaf7914-929e-495e-bcff-5ab35a9f436c", data ={{"campaign_id": {data['campaign_id']}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {data['dealership_id']}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data["vehicle_make"]}})
    reporting_res = api.post_req(url ="https://apps.dgaauto.com/virtualAgentDataImport/webhook", headers={{"x-api-key": "$2a$11$5GHNF.BbEILij03XRr163eV0lrbRGu6Rq.jlycXAvB.fddAZkO5GK"}}, data={{"id": row_id, "campaign_id": {data['campaign_id']}, "recording": data["recording"], "transcript": data['transcript'], "api_logs":obj['functions'], "call_status": data['call_status'], "call_id": data['call_id'], "start_time": data['start_time'], "end_time": data['end_time'], "first_name": data["first_name"], "last_name": data["last_name"], "phone_number": data["phone_number"], "sentiment": data["sentiment"], "email_address": data["email_address"], "vehicle_make": data["vehicle_make"], "vehicle_model": data["vehicle_model"], "vehicle_year": data["vehicle_year"], "appointment_date": data["appointment_date"], "summary": data["summary"], "disposition": data["disposition"], "disposition_id": data["disposition_id"], "transportation_type": data["transportation_type"], "callback_time": data["callback_time"], "callback": data["callback"], "has_multiple_accounts": data["has_multiple_accounts"], "book_appointment_error": data["book_appointment_error"]}})
    s3.upload_file_from_url(url=obj["recording_url"], imageName=f"{{call_id}}-3065", fileExtension="wav")"""
            st.code(trigger, language="python")
        except Exception as e:
            st.error(f"Error parsing JSON: {e}")
