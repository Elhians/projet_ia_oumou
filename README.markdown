# LinguaLearn AI

LinguaLearn AI is an interactive language learning platform built with Streamlit, supporting English, French, and Arabic. It provides translation, grammar analysis, text correction, personalized exercises, and progress tracking.

## Features
- Translate sentences between English, French, and Arabic using MarianMT
- Grammar analysis using spaCy
- Automatic text correction with LanguageTool
- Adaptive quizzes based on user level
- Progress tracking with SQLite database
- User feedback collection

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd lingualearn-ai
```
2. Install dependencies:
```bash
pip install streamlit transformers spacy language-tool-python pandas sentencepiece
# Note: sqlite3 comes with Python by default

# Download required spaCy models
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
python -m spacy download xx_ent_wiki_sm

# Install PyTorch for translation models
pip install torch
```

3. Run the application:
```bash
# IMPORTANT: Always use streamlit run command (not python directly)
streamlit run app.py

# Or use the provided shell script which will install dependencies automatically
chmod +x run.sh
./run.sh
```

## Project Structure
- `app.py`: Main Streamlit application
- `nlp_utils.py`: NLP processing functions (translation, grammar analysis, correction)
- `exercises.py`: Quiz generation logic
- `lingualearn.db`: SQLite database for user progress

## Usage
1. Select source and target languages
2. Enter a sentence for translation and analysis
3. View translation, grammar analysis, and corrections
4. Take personalized quizzes to test your skills
5. Track your progress and provide feedback

## Notes
- Arabic support for grammar analysis and correction is limited
- Requires Java 17+ for LanguageTool text correction functionality
- Requires SentencePiece library for translations
- Ensure internet connection for downloading transformer models
- Always run the app using `streamlit run app.py`, not directly with Python

## Requirements
- Python 3.8+
- Streamlit
- Transformers (HuggingFace)
- SentencePiece
- spaCy
- LanguageTool
- Pandas
- SQLite3