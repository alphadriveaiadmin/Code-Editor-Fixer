def wf(obj):
    data = extract.extract_from_features(
        obj=obj['transcript'],
        features=features,
        featuresToExtract=[
            'first_name','last_name','sentiment','email_address',
            'vehicle_make','vehicle_model','vehicle_year',
            'appointment_date','summary','disposition','disposition_id',
            'transportation_type','callback_time','callback',
            'has_multiple_accounts','book_appointment_error'
        ]
    )

    data["transcript"] = obj["transcript"]
    data['start_time'] = obj['start_timestamp']
    data['end_time'] = obj['end_timestamp']
    data["recording"] = obj["recording_url"]
    data["call_status"] = obj["call_status"]

    # Parse ALL phone numbers (incoming, outgoing, transferred)
    data['phone_numbers'] = list(set([
        obj.get('from_number',''),
        obj.get('to_number',''),
        obj.get('caller_id',''),
        obj.get('forwarded_from',''),
        obj.get('customer_number','')
    ]))

    # Use primary inbound number as 'phone_number'
    data['phone_number'] = obj.get('from_number','')

    call_id = RANDOM(8).generate()
    row_id = RANDOMINT(5).generate()
    print(call_id)
    data['call_id'] = call_id
    insertRow(data)

    # Send to Webhooks
    api.post_req(
        url="https://apps.dgaauto.com/lucyWebhookAlert/webhook",
        data={
            "campaign_id": 2620, "agent_comments": data['summary'],
            "call_back": data['callback'], "call_disposition_id": data["disposition_id"],
            "advisor": "", "dealer_id": 3075,
            "first_name": data['first_name'], "last_name": data["last_name"],
            "phone": data["phone_number"],
            "vehicle_year": data['vehicle_year'],
            "vehicle_model": data["vehicle_model"],
            "vehicle_make": data['vehicle_make']
        }
    )

    api.post_req(
        url="https://webhook.site/bcaf7914-929e-495e-bcff-5ab35a9f436c",
        data={
            "campaign_id": 2620, "agent_comments": data['summary'],
            "call_back": data['callback'], "call_disposition_id": data["disposition_id"],
            "advisor": "", "dealer_id": 3075,
            "first_name": data['first_name'], "last_name": data["last_name"],
            "phone": data["phone_number"],
            "vehicle_year": data['vehicle_year'],
            "vehicle_model": data["vehicle_model"],
            "vehicle_make": data['vehicle_make']
        }
    )

    console.log("reporting")
    reporting_res = api.post_req(
        url="https://apps.dgaauto.com/virtualAgentDataImport/webhook",
        headers={"x-api-key": "$2a$11$5GHNF.BbEILij03XRr163eV0lrbRGu6Rq.jlycXAvB.fddAZkO5GK"},
        data={
            "id": row_id, "campaign_id": 2620,
            "recording": data["recording"], "transcript": data['transcript'],
            "api_logs": obj['functions'], "call_status": data['call_status'],
            "call_id": data['call_id'], "start_time": data['start_time'],
            "end_time": data['end_time'], "first_name": data["first_name"],
            "last_name": data["last_name"], "phone_numbers": data["phone_numbers"],
            "sentiment": data["sentiment"], "email_address": data["email_address"],
            "vehicle_make": data["vehicle_make"], "vehicle_model": data["vehicle_model"],
            "vehicle_year": data["vehicle_year"], "appointment_date": data["appointment_date"],
            "summary": data["summary"], "disposition": data["disposition"],
            "disposition_id": data["disposition_id"],
            "transportation_type": data["transportation_type"],
            "callback_time": data["callback_time"], "callback": data["callback"],
            "has_multiple_accounts": data["has_multiple_accounts"],
            "book_appointment_error": data["book_appointment_error"]
        }
    )
    console.log(reporting_res)

    s3.upload_file_from_url(
        url=obj["recording_url"],
        imageName=f"{call_id}-3075",
        fileExtension="wav"
    )
