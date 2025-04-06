import streamlit as st
import os
from groq import Groq
from streamlit_chat import message

# Securely get the API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = api_key

# Initialize Groq client
client = Groq(api_key=api_key)

st.set_page_config(page_title="🧠 CGC Vaidya", layout="wide")

# Set up layout: left for input, right for chat
left_col, right_col = st.columns([1.5, 2])

# Sidebar prompt
with left_col:
    st.markdown("<h1 style='color: #4CAF50;'>🧘 CGC Vaidya</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style='font-size: 16px;'>
        Your personal AI mental health companion. Type how you feel and let me help you navigate through it 💬
        </p>
    """, unsafe_allow_html=True)

    # Session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_area("How are you feeling today?", key="user_input", height=100)

    if st.button("Send"):
        if user_input.strip() != "":
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Call Groq API
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are CGC Vaidya, an empathetic AI mental health companion "
                                "designed to support students of CGC Jhanjeri. Be calm, supportive, and encouraging. "
                                "Use gentle language. Suggest relaxation, self-help, or direct them to professional support if needed."
                            ),
                        },
                        *st.session_state.messages
                    ],
                    model="mixtral-8x7b-32768",  # Replace with a supported model if needed
                )

                bot_reply = chat_completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Bot: Error: {str(e)}"})

# Display chat on right
with right_col:
    st.markdown(
        """
        <div style='height: 600px; overflow-y: auto; padding: 10px; background-color: #1e1e1e; border-radius: 12px;'>
        """,
        unsafe_allow_html=True,
    )

    for msg in st.session_state.messages:
        is_user = msg["role"] == "user"
        message(
            msg["content"],
            is_user=is_user,
            key=f"{msg['role']}_{msg['content'][:10]}",
            avatar_style="thumbs" if is_user else "bottts",
            seed="CGC" if not is_user else None,
        )

    st.markdown("</div>", unsafe_allow_html=True)
