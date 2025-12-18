import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from google import genai
import streamlit as st

#################### CONFIGURATION ####################
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

client = genai.Client(api_key=GEMINI_API_KEY)

#################### STATE MANAGEMENT ####################
if 'page' not in st.session_state:
    st.session_state['page'] = 'input'

def reset_app():
    for key in ['subject', 'body', 'last_receiver', 'ballons_done']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state['page'] = 'input'
    st.rerun()

#################### AI GENERATION LOGIC ####################
def generate_email_content(prompt_data):
    try:
        with st.spinner("Generating subject and body..."):
            sub_prompt = f"Write one short, catchy email subject for: {prompt_data['desc']}. Tone: {prompt_data['tone']}. Return only the subject text."
            sub_res = client.models.generate_content(model="gemini-2.5-flash", contents=sub_prompt)
            st.session_state['subject'] = sub_res.text.strip()

            body_prompt = f"Write a {prompt_data['length']} email body. Topic: {prompt_data['desc']}. Tone: {prompt_data['tone']}. From: {prompt_data['s_name']}. To: {prompt_data['r_name']}. Do not include a subject line."
            body_res = client.models.generate_content(model="gemini-2.5-flash", contents=body_prompt)
            st.session_state['body'] = body_res.text.strip()
        st.success("Email generated!")
    except Exception as e:
        st.error(f"AI Generation Error: {e}")

#################### EMAIL SENDING LOGIC ####################
def send_email(subject, body, sender, receiver):
    try:
        with st.spinner("Connecting to mail server..."):
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = receiver

            with smtplib.SMTP("smtp.gmail.com", port=587) as server:
                server.starttls()
                server.login(user=sender, password=EMAIL_PASSWORD)
                server.send_message(msg)
        
        st.session_state['last_receiver'] = receiver
        st.session_state['page'] = 'success'
        st.rerun()
    except Exception as e:
        st.error(f"Failed to send email: {e}")

#################### UI - INPUT PAGE ####################
if st.session_state['page'] == 'input':
    st.title("📧 AI Email Generator")

    with st.form("email_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_name = st.text_input("Your Name")
            s_mail = st.text_input("Your Email")
        with col2:
            r_name = st.text_input("Recipient Name")
            r_mail = st.text_input("Recipient Email")

        tone = st.selectbox("Tone", ["Professional", "Formal", "Casual"])
        length = st.selectbox("Length", ["Short", "Medium", "Long"])
        desc = st.text_area("What is the email about?")
        
        submit_button = st.form_submit_button("Generate Email")

    if submit_button:
        if all([s_name, s_mail, r_name, r_mail, desc]):
            data = {"s_name": s_name, "r_name": r_name, "desc": desc, "tone": tone, "length": length}
            generate_email_content(data)
        else:
            st.warning("Please fill in all fields.")

    # --- PREVIEW SECTION ---
    if 'subject' in st.session_state:
        st.divider()
        st.subheader("Preview & Send")
        final_subject = st.text_input("Subject", value=st.session_state['subject'])
        final_body = st.text_area("Body", value=st.session_state['body'], height=300)

        if st.button("Send Email"):
            send_email(final_subject, final_body, s_mail, r_mail)

#################### UI - SUCCESS PAGE ####################
elif st.session_state['page'] == 'success':
    if 'ballons_done' not in st.session_state:
        st.balloons()
        st.session_state['ballons_done'] = True

    st.success(f"Email sent successfully to {st.session_state['last_receiver']}!")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Send Another"):
            reset_app()
    with c2:
        if st.button("Exit"):
            st.info("You may now close this tab.")
            st.stop()