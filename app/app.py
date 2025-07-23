import streamlit as st
import sqlite3
import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
import spacy
import language_tool_python
from nlp_utils import translate_text, analyze_grammar, correct_text
from exercises import generate_quiz
import uuid

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'level' not in st.session_state:
    st.session_state.level = 'Beginner'
if 'translation' not in st.session_state:
    st.session_state.translation = ""

# Additional session state variables for quiz tracking
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0

# Database setup
def init_db():
    conn = sqlite3.connect('lingualearn.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                (user_id TEXT, level TEXT, progress INTEGER, last_quiz_score INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Save user progress
def save_progress(user_id, level, progress, quiz_score):
    conn = sqlite3.connect('lingualearn.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)',
              (user_id, level, progress, quiz_score))
    conn.commit()
    conn.close()

# Main app
st.title("LinguaLearn AI 🌍")
st.write("Interactive Language Learning Platform")

# Language selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", ["English", "French", "Arabic"])
with col2:
    target_lang = st.selectbox("Target Language", ["English", "French", "Arabic"])

# Text input
user_input = st.text_area("Enter a sentence to translate and analyze:")

# Translation section with dedicated button
col1, col2 = st.columns([1, 3])
with col1:
    translate_button = st.button("Translate")
with col2:
    analyze_button = st.button("Analyze Grammar & Correct")

# Display translation when button is clicked
if translate_button and user_input:
    with st.spinner("Translating..."):
        translation = translate_text(user_input, source_lang, target_lang)
        st.session_state.translation = translation

# Translation result field
if st.session_state.translation:
    st.subheader("Translation")
    st.text_area("Translated text:", value=st.session_state.translation, height=100, disabled=True)

# Grammar analysis and correction only when analyze button is clicked
if analyze_button and user_input:
    # Grammar analysis
    with st.spinner("Analyzing grammar..."):
        grammar_analysis = analyze_grammar(user_input, source_lang)
    st.subheader("Grammar Analysis")
    st.write(grammar_analysis)
    
    # Text correction
    with st.spinner("Checking for errors..."):
        corrected_text, corrections = correct_text(user_input, source_lang)
    st.subheader("Corrections")
    if corrections:
        st.write(f"Corrected: {corrected_text}")
        st.write("Corrections made:")
        for correction in corrections:
            st.write(f"- {correction}")
    else:
        st.write("No corrections needed!")

# Exercises section
st.subheader("Personalized Exercises")

# Generate quiz button - only show if no quiz is active
if not st.session_state.quiz_active:
    if st.button("Generate Quiz"):
        st.session_state.quiz_active = True
        st.session_state.quiz_submitted = False
        # Generate quiz questions with debugging
        quiz_questions = generate_quiz(st.session_state.level, source_lang, target_lang)
        st.session_state.quiz_questions = quiz_questions
        st.session_state.quiz_total = len(quiz_questions)
        
        # Debug output - can be removed later
        if len(quiz_questions) == 0:
            st.error("No questions were generated! Check language pair compatibility.")
            # Force at least one sample question
            st.session_state.quiz_questions = [{
                'question': f'Sample question: Translate "Hello" from {source_lang} to {target_lang}:',
                'options': ['Hello', 'Bonjour', 'مرحبا', 'Hola'],
                'correct_answer': 'Bonjour' if target_lang == 'French' else 'مرحبا' if target_lang == 'Arabic' else 'Hello'
            }]
            st.session_state.quiz_total = 1
        
        st.rerun()

# Display quiz if active
if st.session_state.quiz_active:
    # Display quiz form
    with st.form("quiz_form"):
        if len(st.session_state.quiz_questions) == 0:
            st.warning("No questions available for this language pair. Please try a different language combination.")
            submitted = st.form_submit_button("Back to Language Selection")
            if submitted:
                st.session_state.quiz_active = False
                st.rerun()
        else:
            answers = []
            # Show how many questions are available
            st.write(f"**{len(st.session_state.quiz_questions)} questions in this quiz:**")
            
            for i, q in enumerate(st.session_state.quiz_questions):
                st.write(f"Question {i+1}: {q['question']}")
                # Make sure options are not empty
                if not q['options']:
                    q['options'] = ["No options available"]
                
                # Add an empty first option to avoid default selection
                options = [""] + q['options'] if "" not in q['options'] else q['options']
                answer = st.radio(
                    f"Select answer for question {i+1}", 
                    options,
                    index=0,  # Default to the empty option
                    key=f"q{i}"
                )
                answers.append(answer)
            
            submitted = st.form_submit_button("Submit Quiz")
            
            # Handle quiz submission
            if submitted:
                st.session_state.quiz_submitted = True
                score = 0
                
                # Only count non-empty answers
                for i, q in enumerate(st.session_state.quiz_questions):
                    if answers[i] == q['correct_answer']:
                        score += 1
                
                st.session_state.quiz_score = score
                st.rerun()  # Updated from experimental_rerun

    # Display results after submission (outside the form)
    if st.session_state.quiz_submitted:
        score = st.session_state.quiz_score
        total = st.session_state.quiz_total
        score_percentage = (score / total) * 100 if total > 0 else 0
        
        # Update progress
        old_progress = st.session_state.progress
        st.session_state.progress = min(old_progress + 10, 100)  # Add fixed 10% progress per quiz
        
        # Update level based on score
        if score_percentage > 80:
            st.session_state.level = "Advanced"
        elif score_percentage > 50:
            st.session_state.level = "Intermediate"
        
        # Save to database
        save_progress(st.session_state.user_id, st.session_state.level, 
                     st.session_state.progress, score_percentage)
        
        # Display results with animation
        st.success(f"Your score: {score}/{total} ({score_percentage:.0f}%)")
        
        # Show progress increase
        st.info(f"Progress increased from {old_progress:.0f}% to {st.session_state.progress:.0f}%")
        st.write(f"Current Level: {st.session_state.level}")
        
        # Display rating with stars
        if score_percentage == 100:
            st.balloons()
            st.markdown("### Rating: ⭐⭐⭐⭐⭐")
            st.markdown("**Excellent!** Perfect score! You've mastered this level.")
        elif score_percentage >= 80:
            st.markdown("### Rating: ⭐⭐⭐⭐")
            st.markdown("**Great job!** You're showing strong language skills.")
        elif score_percentage >= 60:
            st.markdown("### Rating: ⭐⭐⭐")
            st.markdown("**Good work!** Keep practicing to improve further.")
        elif score_percentage >= 40:
            st.markdown("### Rating: ⭐⭐")
            st.markdown("**Nice effort!** More practice will help solidify these concepts.")
        else:
            st.markdown("### Rating: ⭐")
            st.markdown("**Keep going!** Language learning takes time. Try reviewing the basics.")
        
        # Add recommendation
        if st.session_state.level == "Beginner":
            if score_percentage < 50:
                st.info("📚 Recommendation: Focus on basic vocabulary and simple sentences.")
            else:
                st.info("📚 Recommendation: You're ready to try some more complex phrases!")
        elif st.session_state.level == "Intermediate":
            if score_percentage < 60:
                st.info("📚 Recommendation: Review intermediate grammar patterns and vocabulary.")
            else:
                st.info("📚 Recommendation: Challenge yourself with more advanced content!")
        else:  # Advanced
            if score_percentage < 70:
                st.info("📚 Recommendation: Review complex grammar and expand your vocabulary.")
            else:
                st.info("📚 Recommendation: You're doing great! Try native-level content next.")
        
        # Button to start a new quiz
        if st.button("Try Another Quiz"):
            st.session_state.quiz_active = False
            st.session_state.quiz_submitted = False
            st.rerun()  # Updated from experimental_rerun

# Progress tracking
st.subheader("Your Progress")
st.progress(st.session_state.progress / 100)
st.write(f"Current Level: {st.session_state.level}")

# Feedback form
with st.form("feedback_form"):
    st.subheader("Feedback")
    rating = st.radio("Rate your experience", [1, 2, 3, 4, 5])
    comments = st.text_area("Additional comments")
    feedback_submitted = st.form_submit_button("Submit Feedback")
    if feedback_submitted:
        st.success("Thank you for your feedback!")