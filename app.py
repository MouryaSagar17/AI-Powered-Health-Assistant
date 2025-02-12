import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Cache the models to optimize performance
@st.cache_resource
def load_qa_model():
    return pipeline("question-answering", model="deepset/roberta-base-squad2")

@st.cache_resource
def load_chatbot_model():
    return pipeline("text-generation", model="distilgpt2")

qa_pipeline = load_qa_model()
chatbot = load_chatbot_model()

# Expanded list of symptoms and suggested medications
medication_suggestions = {
    "fever": "Paracetamol (Crocin, Tylenol) can help reduce fever. Stay hydrated and rest.",
    "headache": "Ibuprofen (Advil) or Paracetamol can help. If persistent, consult a doctor.",
    "cold": "Antihistamines like Cetirizine (Zyrtec) or decongestants like Phenylephrine may provide relief.",
    "cough": "Dextromethorphan (Benadryl) or honey-based syrups can soothe a cough.",
    "nausea": "Domperidone or Ondansetron can help. Avoid oily foods.",
    "stomach pain": "Antacids like Pantoprazole or Ranitidine can help with acidity-related pain.",
    "diarrhea": "ORS (Oral Rehydration Solution) and Loperamide (Imodium) may help. Stay hydrated.",
    "constipation": "Increase fiber intake. Mild laxatives like Lactulose or Isabgol can help.",
    "vomiting": "Ondansetron (Zofran) can help control vomiting. Drink plenty of fluids.",
    "sore throat": "Saltwater gargles and lozenges (Strepsils) can help. Ibuprofen may reduce pain.",
    "body pain": "Ibuprofen (Brufen) or Naproxen can help relieve body aches.",
    "allergy": "Antihistamines like Loratadine (Claritin) or Cetirizine can reduce allergic reactions.",
    "acidity": "Pantoprazole or Omeprazole can help relieve acid reflux symptoms.",
    "anxiety": "Practicing deep breathing and meditation may help. Consult a doctor if severe.",
    "depression": "Exercise and therapy are beneficial. Consult a mental health professional.",
    "high blood pressure": "Reduce salt intake. Medications like Amlodipine or Losartan may be prescribed by a doctor.",
    "low blood pressure": "Drink more fluids and eat small, frequent meals. Salt intake can be increased slightly."
}

# Define chatbot logic with medication suggestions
def healthcare_chatbot(user_input):
    user_input = user_input.lower()
    
    # Check if the user input matches any symptom and suggest a remedy
    for symptom, suggestion in medication_suggestions.items():
        if symptom in user_input:
            return f"It seems like you have {symptom}. {suggestion} Always consult a doctor before taking any medication."
    
    # Rule-based responses for common medical queries
    if "symptom" in user_input:
        return "It seems like you're experiencing symptoms. Please consult a doctor for accurate advice."
    elif "appointment" in user_input:
        return "Would you like me to schedule an appointment with a doctor?"
    elif "medication" in user_input:
        return "It's important to take your prescribed medications regularly. If you have concerns, consult your doctor."
    elif "appointment" in user_input:
        return "I can't book appointments directly, but you can visit [hospital website] or call [phone number] to schedule one."

    if "hydration" in user_input or "stress" in user_input:
        return chatbot(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']

    # AI-generated response for other medical queries
    context = "Painkillers, also known as analgesics, can have side effects such as drowsiness, dizziness, nausea, constipation, and stomach irritation. Some stronger painkillers may cause dependency if used long-term. If you experience severe side effects, consult a doctor immediately."
    response = qa_pipeline(question=user_input, context=context)
    return response['answer'] if response else chatbot(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']

# Streamlit Web App Interface
def main():
    st.title("Healthcare Assistant Chatbot")
    user_input = st.text_input("How can I assist you today?", "")

    if st.button("Submit"):
        if user_input.strip():
            response = healthcare_chatbot(user_input)
            st.write("**Healthcare Assistant:**", response)
        else:
            st.write("Please enter a valid query.")

if __name__ == "__main__":
    main()
