import streamlit as st
from groq import Groq
import PyPDF2
import io
import json

st.set_page_config(page_title="🧠 AI Flashcard Generator", page_icon="🧠", layout="centered")

st.title("🧠 AI Flashcard Generator")
st.markdown("Paste text or upload a PDF and get instant study flashcards!")

api_key = st.text_input("Your Groq API Key", type="password")
text = st.text_area("Paste your text here...", height=200)
st.markdown("— or upload a PDF —")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

def extract_pdf(file):
    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if st.button("Generate Flashcards 🚀"):
    if not api_key:
        st.warning("Please enter your Groq API key.")
    elif not text and not uploaded_file:
        st.warning("Please provide text or upload a PDF.")
    else:
        with st.spinner("Generating flashcards..."):
            content = extract_pdf(uploaded_file) if uploaded_file else text

            client = Groq(api_key=api_key)
            prompt = f"""
You are a study assistant. Based on the following content, generate 10 flashcards.
Return ONLY a JSON array, no explanation, no markdown, just raw JSON.

Format:
[
  {{"question": "...", "answer": "..."}},
  ...
]

Content:
{content}
"""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content
            flashcards = json.loads(result)

        st.success(f"{len(flashcards)} flashcards generated!")
        st.markdown("---")

        for i, card in enumerate(flashcards):
            with st.expander(f"📌 Card {i+1}: {card['question']}"):
                st.markdown(f"**Answer:** {card['answer']}")
