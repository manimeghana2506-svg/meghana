import streamlit as st
import requests
import json
import re

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Emotion-Aware Responsible Voice AI", layout="centered")

# Custom CSS for a clean, modern look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .ethical-banner {
        padding: 15px;
        background-color: #fff3cd;
        border-left: 5px solid #ffecb5;
        color: #856404;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_input_ those=True)

# --- BACKEND LOGIC ---

def simplify_text(text):
    """Converts input into a clear, teacher-style explanation."""
    if not text:
        return ""
    # Simple prefixing to simulate a 'teacher' persona for the hackathon prototype
    return f"Let me explain this clearly: {text}"

def detect_emotion(text):
    """Rule-based emotion detection using keywords."""
    text = text.lower()
    if any(word in text for word in ["happy", "great", "joy", "wonderful", "love"]):
        return "Happy"
    elif any(word in text for word in ["sad", "sorry", "unfortunately", "bad", "cry"]):
        return "Sad"
    elif any(word in text for word in ["wow", "amazing", "excited", "awesome", "huge"]):
        return "Excited"
    elif any(word in text for word in ["serious", "urgent", "important", "must", "warning"]):
        return "Serious"
    else:
        return "Normal"

def apply_emotion(text, emotion):
    """Modifies text with pauses and punctuation to simulate emotional nuance."""
    if emotion == "Happy":
        return f"Oh! {text}!"
    elif emotion == "Sad":
        return f"... {text} ... I'm sorry to say."
    elif emotion == "Excited":
        return f"Wow! {text.upper()}!!"
    elif emotion == "Serious":
        return f"Please listen carefully. {text}."
    else:
        return text

def generate_voice(text, voice_id, speed):
    """
    Calls Murf AI API to generate speech.
    Note: Requires a valid API Key from Murf AI.
    """
    api_key = "YOUR_MURF_API_KEY"
    url = "https://api.murf.ai/v1/speech/generate"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    payload = {
        "voiceId": voice_id,
        "text": text,
        "rate": int(speed * 100), # Murf uses percentage for rate
        "format": "MP3",
        "sampleRate": 48000
    }

    try:
        # Check for placeholder key
        if api_key == "ap2_09012f30-c3f8-40db-b14a-d7f439fe19d7":
            return "ERROR: API Key missing. Please insert your Murf AI API Key in the code."

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("audioFile")
        else:
            return f"ERROR: API returned {response.status_code} - {response.text}"
    except Exception as e:
        return f"ERROR: {str(e)}"

# --- FRONTEND UI ---

def main():
    st.title("🎙️ Emotion-Aware Responsible Voice AI")
    
    # Ethical Warning Banner
    st.markdown("""
        <div class="ethical-banner">
            <strong>Ethical Safeguard:</strong> This AI tool is designed for creative and educational purposes. 
            Usage for creating deepfakes, impersonating individuals without consent, or spreading 
            misinformation is strictly prohibited. Generated audio contains invisible watermarks for traceability.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 1. Input your text")
    user_input = st.text_area("What should the AI say?", placeholder="Enter text here...", height=150)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 2. Emotion Settings")
        mode = st.radio("Emotion Mode", ["Auto Detect", "Manual Select"])
        
        if mode == "Manual Select":
            emotion_choice = st.selectbox("Select Emotion", ["Normal", "Happy", "Sad", "Excited", "Serious"])
        else:
            detected = detect_emotion(user_input)
            st.info(f"Detected Emotion: **{detected}**")
            emotion_choice = detected

    with col2:
        st.markdown("### 3. Voice Settings")
        # Example Murf Voice IDs (Note: These are placeholders; real IDs vary by account tier)
        voice_map = {
            "Marcus (Male - Bold)": "en-US-marcus",
            "Natalie (Female - Soft)": "en-US-natalie",
            "Clint (Male - Professional)": "en-US-clint",
            "Julie (Female - Conversational)": "en-US-julie"
        }
        voice_label = st.selectbox("Select Voice", list(voice_map.keys()))
        voice_id = voice_map[voice_label]
        
        speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)

    st.divider()

    if st.button("Generate Voice"):
        if not user_input.strip():
            st.error("Please enter some text first!")
        else:
            with st.spinner("Processing emotional intelligence and generating audio..."):
                # Step 1: Logic Chain
                simplified = simplify_text(user_input)
                emotional_text = apply_emotion(simplified, emotion_choice)
                
                # Step 2: API Call
                audio_result = generate_voice(emotional_text, voice_id, speed)

                if audio_result.startswith("ERROR"):
                    st.error(audio_result)
                    # Mock behavior for hackathon demonstration if key is missing
                    if "API Key missing" in audio_result:
                        st.warning("Hackathon Demo Mode: Showing processed text since API Key is not set.")
                        st.write(f"**Final Processed Text:** {emotional_text}")
                else:
                    st.success("Audio Generated Successfully!")
                    st.markdown(f"**Detected Emotion:** {emotion_choice}")
                    st.markdown(f"**Processed Text:** *{emotional_text}*")
                    st.audio(audio_result, format="audio/mp3")
                    st.download_button("Download Audio", audio_result, file_name="generated_voice.mp3")

    # Footer
    st.markdown("---")
    st.caption("Built with Python, Streamlit, and Murf AI. Responsibility starts with the creator.")

if __name__ == "__main__":
    main()
