function generate() {
  try {
    const input = document.getElementById('jsonInput').value;
    const jsonData = JSON.parse(input);
    const campaignId = document.getElementById('campaignId').value;
    const dealerId = document.getElementById('dealerId').value;

    // Extract phone numbers recursively
    const phones = new Set();
    (function extract(obj) {
      if (typeof obj === 'object' && obj !== null) {
        Object.values(obj).forEach(v => {
          if (typeof v === 'string' && /^\d{10}$/.test(v)) phones.add(v);
          else if (typeof v === 'object') extract(v);
        });
      }
    })(jsonData);

    // Build allowedTransferNumbers array (raw and +1 format)
    const allowedTransferNumbers = Array.from(phones).flatMap(p => [p, `+1${p}`]);

    // Final output string with language='multi'
    const output = `@trigger voice.call_received(phoneNumber=params['phone_number'], start_function={"name":"start_function","url":"https://randy-marion-chevrolet-cadillac.techwall.us/gs-appointment-api/lookupCustomer?dealerId=1","auth":{"username":"dga_scheduler","password":"Green3Red4Blue"}}, allowedTransferNumbers=[${allowedTransferNumbers.map(n => `"${n}"`).join(',')}], start_sentence=params["first_sentence"], objective=params["objective"], functions=params['tools'], voiceId="11labs-Cimo", model='gpt-4o', sensitivity="0.7", timezone="America/New_York", language="multi")\nfunction wf(obj) { /* your full script here with ${campaignId} & ${dealerId} */ }`;

    document.getElementById('output').textContent = output;
  } catch (err) {
    document.getElementById('output').textContent = "Invalid JSON!";
  }
}
