#!/bin/bash

echo "Starting LinguaLearn AI application setup..."

# Install required dependencies
echo "Installing required Python dependencies..."
pip install sentencepiece torch

# Make sure we have all necessary spaCy models
echo "Checking for required spaCy models..."
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
python -m spacy download xx_ent_wiki_sm

# Run the Streamlit application
echo "Launching Streamlit application..."
streamlit run app.py

echo "Application stopped."
