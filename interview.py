# interview.py - ITEL Future Learning Technologies Showcase Feedback
# Anthropic (Saving to Google Drive) - Standalone deployment, no Qualtrics integration

import streamlit as st
import time
from utils import (
    check_password,
    check_if_interview_completed,
    save_interview_data,
    save_interview_data_to_drive,
)
import os
import config
import pytz
import re

from datetime import datetime
import anthropic
from openai import OpenAI
api = "anthropic"  # Switch to "openai" for the OpenAI version

# ===== SINGLE QUESTION ENFORCEMENT =====
def count_questions(text):
    """Count the number of questions in a text response"""
    question_marks = text.count('?')

    question_patterns = [
        r'\bcan you tell me\b',
        r'\bcan you describe\b',
        r'\bwhat (?:do|did|does|is|are|was|were)\b',
        r'\bhow (?:do|did|does|is|are|was|were)\b',
        r'\bwhy (?:do|did|does)\b',
        r'\bcould you\b',
        r'\bwould you\b'
    ]

    pattern_count = sum(1 for pattern in question_patterns if re.search(pattern, text.lower()))
    return max(question_marks, pattern_count)

def enforce_single_question(response_text):
    """Force response to contain only one question by truncating after first question"""
    num_questions = count_questions(response_text)

    if num_questions > 1:
        parts = response_text.split('?')
        if len(parts) > 1:
            return parts[0] + '?'

    return response_text
# ===== END SINGLE QUESTION ENFORCEMENT =====

# Define timezone for timestamps
central_tz = pytz.timezone("America/Chicago")

# Set page title and icon
st.set_page_config(page_title="ITEL Showcase Feedback", page_icon=config.AVATAR_INTERVIEWER)

# Get current date and time in CT
current_datetime = datetime.now(central_tz).strftime("%Y-%m-%d_%H-%M-%S")

# Set the username with date and time (timestamp only — no Qualtrics UID)
if "username" not in st.session_state or st.session_state.username is None:
    st.session_state.username = f"Claude_{current_datetime}"
    st.session_state.interview_start_time = datetime.now(central_tz).strftime("%Y-%m-%d %H:%M:%S %Z")

# Create directories if they do not already exist
for directory in [config.TRANSCRIPTS_DIRECTORY, config.TIMES_DIRECTORY, config.BACKUPS_DIRECTORY]:
    os.makedirs(directory, exist_ok=True)

# Initialise session state
st.session_state.setdefault("interview_active", True)
st.session_state.setdefault("messages", [])

# Check if interview previously completed
interview_previously_completed = check_if_interview_completed(
    config.TRANSCRIPTS_DIRECTORY, st.session_state.username
    )

# If app started but interview was previously completed
if interview_previously_completed and not st.session_state.messages:
    st.session_state.interview_active = False

# Add 'Quit' button to dashboard
col1, col2 = st.columns([0.85, 0.15])
with col2:
    if st.session_state.interview_active and st.button("Quit", help="End the interview."):
        st.session_state.interview_active = False
        st.session_state.messages.append({"role": "assistant", "content": "You have cancelled the interview."})
        try:
            save_interview_data(st.session_state.username, config.TRANSCRIPTS_DIRECTORY)
        except Exception as e:
            st.error(f"Error saving data: {str(e)}")

# Display previous conversation (except system prompt)
for message in st.session_state.messages[1:]:
    avatar = config.AVATAR_INTERVIEWER if message["role"] == "assistant" else config.AVATAR_RESPONDENT
    if not any(code in message["content"] for code in config.CLOSING_MESSAGES.keys()):
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Load API key from environment variable
API_KEY = os.environ.get("API_KEY")

# Load API client
if api == "openai":
    client = OpenAI(api_key=API_KEY)
    api_kwargs = {"stream": True}
elif api == "anthropic":
    client = anthropic.Anthropic(api_key=API_KEY)
    api_kwargs = {"system": config.SYSTEM_PROMPT}

# API kwargs
api_kwargs.update({
    "messages": st.session_state.messages,
    "model": config.MODEL,
    "max_tokens": config.MAX_OUTPUT_TOKENS,
})
if config.TEMPERATURE is not None:
    api_kwargs["temperature"] = config.TEMPERATURE

# Initialize first system message if history is empty
if not st.session_state.messages:
    if api == "openai":
        st.session_state.messages.append({"role": "system", "content": config.SYSTEM_PROMPT})
        with st.chat_message("assistant", avatar=config.AVATAR_INTERVIEWER):
            try:
                stream = client.chat.completions.create(**api_kwargs)
                message_interviewer = st.write_stream(stream)
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                message_interviewer = "Sorry, there was an error connecting to the interview service. Please try again later."

    elif api == "anthropic":
        st.session_state.messages.append({"role": "user", "content": "Hi"})
        with st.chat_message("assistant", avatar=config.AVATAR_INTERVIEWER):
            message_placeholder = st.empty()
            message_interviewer = ""
            try:
                with client.messages.stream(**api_kwargs) as stream:
                    for text_delta in stream.text_stream:
                        if text_delta:
                            message_interviewer += text_delta
                        message_placeholder.markdown(message_interviewer + "▌")
                message_placeholder.markdown(message_interviewer)
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                message_interviewer = "Sorry, there was an error connecting to the interview service. Please try again later."
                message_placeholder.markdown(message_interviewer)

    st.session_state.messages.append({"role": "assistant", "content": message_interviewer})

    # Store initial backup
    try:
        save_interview_data(
            username=st.session_state.username,
            transcripts_directory=config.BACKUPS_DIRECTORY,
        )
    except Exception as e:
        st.error(f"Error saving backup: {str(e)}")

# Main chat if interview is active
if st.session_state.interview_active:
    if message_respondent := st.chat_input("Your message here"):
        st.session_state.messages.append({"role": "user", "content": message_respondent})

        with st.chat_message("user", avatar=config.AVATAR_RESPONDENT):
            st.markdown(message_respondent)

        with st.chat_message("assistant", avatar=config.AVATAR_INTERVIEWER):
            message_placeholder = st.empty()
            message_interviewer = ""

            try:
                if api == "openai":
                    stream = client.chat.completions.create(**api_kwargs)
                    for message in stream:
                        text_delta = message.choices[0].delta.content
                        if text_delta:
                            message_interviewer += text_delta
                        if len(message_interviewer) > 5:
                            message_placeholder.markdown(message_interviewer + "▌")
                        if any(code in message_interviewer for code in config.CLOSING_MESSAGES.keys()):
                            message_placeholder.empty()
                            break

                elif api == "anthropic":
                    with client.messages.stream(**api_kwargs) as stream:
                        for text_delta in stream.text_stream:
                            if text_delta:
                                message_interviewer += text_delta
                            if len(message_interviewer) > 5:
                                message_placeholder.markdown(message_interviewer + "▌")
                            if any(code in message_interviewer for code in config.CLOSING_MESSAGES.keys()):
                                message_placeholder.empty()
                                break
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                message_interviewer = "Sorry, there was an error. Your response was saved, but we couldn't generate a reply."

            # ===== ENFORCE SINGLE QUESTION =====
            if not any(code in message_interviewer for code in config.CLOSING_MESSAGES.keys()):
                is_conclusion = (
                    "To conclude" in message_interviewer or
                    "how well does" in message_interviewer.lower() or
                    "1 = poorly" in message_interviewer or
                    "scale of 1" in message_interviewer.lower()
                )
                if not is_conclusion:
                    message_interviewer = enforce_single_question(message_interviewer)
            # ===== END ENFORCEMENT =====

            if not any(code in message_interviewer for code in config.CLOSING_MESSAGES.keys()):
                message_placeholder.markdown(message_interviewer)
                st.session_state.messages.append({"role": "assistant", "content": message_interviewer})

                try:
                    save_interview_data(
                        username=st.session_state.username,
                        transcripts_directory=config.BACKUPS_DIRECTORY,
                    )
                except Exception as e:
                    st.warning(f"Failed to save backup: {str(e)}")

            for code in config.CLOSING_MESSAGES.keys():
                if code in message_interviewer:
                    display_message = config.CLOSING_MESSAGES[code]
                    st.session_state.messages.append({"role": "assistant", "content": display_message})
                    st.session_state.interview_active = False
                    st.markdown(display_message)

                    # ===== CLOSING MESSAGE =====
                    st.markdown("---")
                    st.success("🎉 Thank you for completing the feedback interview!")
                    st.markdown(config.CLOSING_NOTE)
                    st.markdown("---")
                    st.info("✅ You may now close this window.")
                    # ===== END CLOSING MESSAGE =====

                    final_transcript_stored = False
                    retries = 0
                    max_retries = 10
                    transcript_path = None

                    while not final_transcript_stored and retries < max_retries:
                        try:
                            transcript_path = save_interview_data(
                                username=st.session_state.username,
                                transcripts_directory=config.TRANSCRIPTS_DIRECTORY,
                            )
                            final_transcript_stored = check_if_interview_completed(config.TRANSCRIPTS_DIRECTORY, st.session_state.username)
                        except Exception as e:
                            st.warning(f"Retry {retries+1}/{max_retries}: Error saving transcript - {str(e)}")

                        time.sleep(0.1)
                        retries += 1

                    if retries == max_retries and not final_transcript_stored:
                        st.error("Error: Interview transcript could not be saved properly after multiple attempts!")

                        emergency_file = f"emergency_transcript_{st.session_state.username}.txt"
                        try:
                            with open(emergency_file, "w") as t:
                                for message in st.session_state.messages:
                                    if message.get('role') == 'system':
                                        continue
                                    speaker_label = "Claude" if (message['role'] == 'assistant' and api == "anthropic") else "ChatGPT" if (message['role'] == 'assistant') else "Attendee"
                                    t.write(f"{speaker_label}: {message['content']}\n\n")
                            transcript_path = emergency_file
                            st.success(f"Created emergency transcript: {emergency_file}")
                        except Exception as e:
                            st.error(f"Failed to create emergency transcript: {str(e)}")

                    if transcript_path:
                        try:
                            save_interview_data_to_drive(transcript_path)
                        except Exception as e:
                            st.error(f"Failed to upload to Google Drive: {str(e)}")
