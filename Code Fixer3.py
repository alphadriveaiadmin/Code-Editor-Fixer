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
ob
