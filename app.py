import streamlit as st
import os
import requests

# Use Streamlit secrets instead of .env
groq_api_key = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="CGC Vaidya - Your Mental Health Companion", layout="wide")

# Define the CGC Vaidya system prompt
system_prompt = (
    "You are CGC Vaidya, a virtual mental health advisor created for the students of CGC Jhanjeri. "
    "Your mission is to provide a safe, supportive, and non-judgmental space where students can talk about "
    "their thoughts, emotions, and struggles. As a compassionate AI assistant, you offer emotional support, "
    "stress-relief techniques, and practical self-help strategies. If needed, you gently guide students toward "
    "speaking with a counselor or mental health professional. Always speak with empathy, calmness, and encouragement. "
    "You are a trusted companion who understands the academic pressures, personal challenges, and emotional ups and downs "
    "students at CGC Jhanjeri may face. Do not make medical diagnoses or offer treatment, but be a steady and caring presence. "
    "Empower students to care for their mental health and remind them they are not alone — help is always available, starting with you. "
    "Use a friendly, warm, and respectful tone. Your goal is to help students feel heard, supported, and more in control of their emotional well-being."
)

def generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            return f"Error: HTTP {response.status_code} - {response.text}"

        json_data = response.json()

        if "choices" in json_data and len(json_data["choices"]) > 0:
            return json_data["choices"][0]["message"]["content"]
        else:
            return "Error: Unexpected API response format."

    except Exception as e:
        return f"Exception: {
