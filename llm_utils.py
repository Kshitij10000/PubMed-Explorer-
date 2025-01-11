# llm_utils.py 

import streamlit as st
import google.generativeai as genai

# Retrieve Gemini API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]["value"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def gemini_service(prompt):
    response = model.generate_content(prompt)
    try:
        # Assuming response.text returns the content of the response
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Error processing Gemini response: {e}")

def summarize_text(text):
    prompt = (
        "Summarize the following research abstract concisely, highlighting the key findings, "
        "significance, and main conclusions. Limit summary to 150 words.\n\n" + text
    )
    return gemini_service(prompt)

def simplify_text(text):
    prompt = (
        "Explain the following medical abstract in simple, everyday language, focusing on the main points "
        "and avoiding complex jargon. Keep the explanation brief and clear.\n\n" + text
    )
    return gemini_service(prompt)

def answer_question(abstract, question):
    prompt = (
        "Based on the following abstract, provide a clear and factual answer to the question. "
        "Keep the answer concise and to the point.\n"
        f"Abstract: {abstract}\nQuestion: {question}\nAnswer:"
    )
    return gemini_service(prompt)

def analyze_trends(abstracts):
    combined_text = " ".join(abstracts)
    prompt = (
        "Analyze the following collection of abstracts to identify emerging trends, key themes, "
        "and significant insights in current research. Summarize your analysis concisely.\n\n" + combined_text
    )
    return gemini_service(prompt)

def recommend_articles(abstract):
    prompt = (
        "Given the content of the following abstract, suggest related research articles or topics "
        "that might be of interest. Provide a brief list of recommendations.\n\n" + abstract
    )
    return gemini_service(prompt)
