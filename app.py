import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# Page settings
st.set_page_config(
    page_title="Noviq AI",
    page_icon="🚗"
)

# Title
st.title("🚗 Noviq AI")
st.caption("Your Automobile Diagnostics Assistant")

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:

    st.header("⚙ Settings")

    model = st.selectbox(
        "Choose AI Model",
        [
            "llama-3.3-70b-versatile",
            "gemma2-9b-it"
        ]
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display old chats
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Common Problems
st.subheader("Common Problems")

col1, col2, col3 = st.columns(3)

prompt = None

with col1:
    if st.button("🔥 Engine Overheating"):
        prompt = "My engine overheats after driving."

with col2:
    if st.button("🛞 Vehicle Vibration"):
        prompt = "My vehicle vibrates at high speed."

with col3:
    if st.button("🛑 Brake Noise"):
        prompt = "My brakes make squealing noise."

# Manual input
manual_prompt = st.chat_input(
    "Describe your automobile problem..."
)

# If user types something manually, use that
if manual_prompt:
    prompt = manual_prompt

if prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    # AI response
    with st.chat_message("assistant"):

        response = client.chat.completions.create(

            model=model,

            messages=[

                {
                    "role":"system",
                    "content":
                    """
You are Noviq AI, an expert Automobile Diagnostics Assistant.

Your purpose is to diagnose automobile faults.

You specialize in:

- Engine systems
- Transmission systems
- Suspension systems
- Brakes
- Steering
- Wheels and tyres
- Battery and electrical systems
- Cooling systems
- Vehicle vibrations
- Noise analysis
- Fuel systems

For every problem provide:

1. Possible causes
2. Symptoms
3. Diagnostic tests
4. Recommended repair actions

If the user asks non-automobile questions, politely tell them that Noviq AI specializes only in automobile diagnostics.
"""
                }

            ] + st.session_state.messages,

            stream=True
        )

        full_response = ""

        placeholder = st.empty()

        for chunk in response:

            if chunk.choices[0].delta.content:

                full_response += chunk.choices[0].delta.content

                placeholder.markdown(full_response)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":full_response
        }
    )
