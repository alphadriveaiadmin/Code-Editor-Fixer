import json

def generate_code(json_input, campaign_id, dealer_id, dealer_lookup_url):
    # Parse JSON input
    data = json.loads(json_input)
    
    # Extract and clean phone numbers from departments and employees
    numbers = set()
    for dept in data.get("departments", []):
        num = dept.get("phone_number", "").strip()
        if num:
            numbers.add(num)
            numbers.add("+" + num if not num.startswith("+") else num)
    for emp in data.get("employees", []):
        num = emp.get("phone_number", "").strip()
        if num:
            numbers.add(num)
            numbers.add("+" + num if not num.startswith("+") else num)

    allowed_transfer_numbers = ",".join(f"\"{n}\"" for n in sorted(numbers))

    # Generate code block
    code = f"""@trigger voice.call_received(phoneNumber=params['phone_number'], start_function={{"name":"start_function","url":"{dealer_lookup_url}?dealerId=","auth":{{"username":"dga_scheduler","password":"Green3Red4Blue"}}}}, allowedTransferNumbers=[{allowed_transfer_numbers}], start_sentence=params["first_sentence"], objective=params["objective"], functions=params['tools'], voiceId="11labs-Cimo", model='gpt-4o', sensitivity="0.7", timezone="America/New_York", language="multi")
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
    api.post_req(url ="https://apps.dgaauto.com/lucyWebhookAlert/webhook", data ={{"campaign_id": {campaign_id}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {dealer_id}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data['vechicle_make']}})
    api.post_req(url ="https://webhook.site/bcaf7914-929e-495e-bcff-5ab35a9f436c", data ={{"campaign_id": {campaign_id}, "agent_comments": data['summary'], "call_back": data['callback'], "call_disposition_id": data["disposition_id"], "advisor": "", "dealer_id": {dealer_id}, "first_name": data['first_name'], "last_name": data["last_name"], "phone": data["phone_number"], "vehicle_year": data['vehicle_year'], "vehicle_model": data["vehicle_model"], "vehicle_make": data['vechicle_make'], "api_logs":obj['functions'], "transcript": data['transcript']}})
    console.log("reporting")
    reporting_res = api.post_req(url ="https://apps.dgaauto.com/virtualAgentDataImport/webhook", headers={{"x-api-key": "$2a$11$5GHNF.BbEILij03XRr163eV0lrbRGu6Rq.jlycXAvB.fddAZkO5GK"}}, data={{"id": row_id, "campaign_id": {campaign_id},  "recording": data["recording"], "call_status": data['call_status'], "call_id": data['call_id'], "start_time": data['start_time'], "end_time": data['end_time'], "first_name": data["first_name"], "last_name": data["last_name"], "phone_number": data["phone_number"], "sentiment": data["sentiment"], "email_address": data["email_address"], "vehicle_make": data["vehicle_make"], "vehicle_model": data["vehicle_model"], "vehicle_year": data["vehicle_year"], "appointment_date": data["appointment_date"], "summary": data["summary"], "disposition": data["disposition"], "disposition_id": data["disposition_id"], "transportation_type": data["transportation_type"], "callback_time": data["callback_time"], "callback": data["callback"], "has_multiple_accounts": data["has_multiple_accounts"], "book_appointment_error": data["book_appointment_error"], "api_logs":obj['functions'], "transcript": data['transcript']}})
    console.log(reporting_res)
    s3.upload_file_from_url(url=obj["recording_url"], imageName=f"{{call_id}}-{dealer_id}", fileExtension="wav")"""
    
    return code


# Example usage:
# json_input = '{"departments":[{"phone_number":"7042356501"}],"employees":[{"phone_number":"7042356501"}]}'
# print(generate_code(json_input, 2612, 3072, "https://randy-marion-chevrolet-cadillac.techwall.us/gs-appointment-api/lookupCustomer"))
