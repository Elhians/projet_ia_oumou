#!/bin/bash

echo "Installing spaCy models..."
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
python -m spacy download xx_ent_wiki_sm

echo "Setup completed."
