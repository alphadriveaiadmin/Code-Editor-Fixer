import streamlit as st
import json

# Set Streamlit page config
st.set_page_config(page_title="DGA Transfer Numbers Generator", layout="wide")
language = "multi"  # Default language as requested

# --- UI ---
st.title("DGA Transfer Numbers Generator")

timezone = st.text_input("Timezone", "America/New_York")
campaign_id = st.text_input("Campaign ID")
dealer_id = st.text_input("Dealer ID")

json_input = st.text_area("Paste your JSON here", height=250)

if st.button("Generate"):
    if not json_input:
        st.error("Please paste your JSON input first.")
    else:
        try:
            obj = json.loads(json_input)

            # --- Clean phone numbers ---
            if "phone_numbers" in obj:
                raw_numbers = obj["phone_numbers"]
                cleaned = []
                for num in raw_numbers:
                    n = num.replace(" ", "").strip()
                    if n not in cleaned:
                        cleaned.append(n)
                obj["phone_numbers"] = cleaned

            # --- Apply campaign_id & dealer_id to all webhooks ---
            if "webhooks" in obj and isinstance(obj["webhooks"], list):
                for webhook in obj["webhooks"]:
                    webhook["campaign_id"] = campaign_id
                    webhook["dealer_id"] = dealer_id

            # --- Add api_logs & transcript ---
            obj["api_logs"] = obj.get("functions", [])
            obj["transcript"] = obj.get("data", {}).get("transcript", "")

            # --- Final Output ---
            st.success("Generated JSON:")
            st.code(json.dumps(obj, indent=2), language="json")

        except Exception as e:
            st.error(f"Error parsing JSON: {e}")

