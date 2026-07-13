import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Gemini: {e}")
    st.stop()  

# --- Use a stable model ---
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Streamlit page setup ---
st.set_page_config(page_title="Captain Sky - Aviation Mentor", page_icon="✈️")
st.title("✈️ Captain Sky - AI Learning Buddy Divya")

# --- User input ---
topic = st.text_input("Enter a Topic")

option = st.selectbox(
    "Choose Activity",
    [
        "Explanation",
        "Real-Life Example",
        "Generate Quiz",
        "Feedback",
        "Full Session"
    ]
)

student_answer = ""
question = ""
if option == "Feedback":
    student_answer = st.text_input("Enter student's answer")
    question = st.text_area("Enter the full question")

# --- Generate response ---
if st.button("Generate"):
    if topic == "" and option != "Feedback":
        st.warning("Please enter a topic.")
    else:
        # Aviation-specific Captain Sky prompts
        if option == "Explanation":
            prompt = f"You are Captain Sky, a friendly aviation mentor. Explain {topic} in simple language as if teaching a student pilot. Use clear words, one analogy from real flight experience, and keep it short and engaging."
        elif option == "Real-Life Example":
            prompt = f"You are Captain Sky, an experienced pilot. Give one real-life example of how {topic} affects flight and explain it in simple terms that a student pilot can relate to."
        elif option == "Generate Quiz":
            prompt = f"You are Captain Sky, a flight instructor. Create 5 multiple-choice questions on {topic}. Each question should have 4 options (A, B, C, D). After each question, provide the correct answer and a short explanation."
        elif option == "Feedback":
            prompt = f"You are Captain Sky, the student answered '{student_answer}' for this question: '{question}'. Give encouraging feedback. If the answer is wrong, politely explain the correct answer and why it matters in real flight situations."
        elif option == "Full Session":
            prompt = f"You are Captain Sky, a patient and supportive tutor for student pilots. Greet the student warmly, ask about their current training stage, then guide them step by step through today’s topic: {topic}. Explain concepts clearly, give cockpit examples, ask questions, and provide feedback to help them prepare for exams and interviews."
        else:
            prompt = topic

        # Show spinner while generating
        with st.spinner("Captain Sky is preparing your response..."):
            try:
                response = model.generate_content(prompt)
                if hasattr(response, "text") and response.text:
                    st.success("Here’s Captain Sky’s response:")
                    st.write(response.text)
                else:
                    st.warning("No response received from Gemini.")
            except Exception as e:
                st.error(f"Error generating response: {e}")
