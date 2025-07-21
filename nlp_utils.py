from transformers import MarianMTModel, MarianTokenizer
import spacy
import language_tool_python
import sys

# Translation models
model_names = {
    'English-Arabic': 'Helsinki-NLP/opus-mt-en-ar',
    'Arabic-English': 'Helsinki-NLP/opus-mt-ar-en',
    'English-French': 'Helsinki-NLP/opus-mt-en-fr',
    'French-English': 'Helsinki-NLP/opus-mt-fr-en',
    'French-Arabic': 'Helsinki-NLP/opus-mt-fr-ar',
    'Arabic-French': 'Helsinki-NLP/opus-mt-ar-fr'
}

# Initialize spaCy models
spacy_models = {
    'English': 'en_core_web_sm',
    'French': 'fr_core_news_sm',
    'Arabic': 'xx_ent_wiki_sm'  # Using multilingual model with some Arabic support
}

# Load spaCy models with error handling
nlp_models = {}
for lang, model in spacy_models.items():
    try:
        nlp_models[lang] = spacy.load(model)
    except IOError:
        print(f"Warning: Could not load spaCy model for {lang}. Some features will be limited.")
        try:
            # Try loading a small multilingual model as fallback
            if lang == 'Arabic':
                # Install the model if you haven't yet: python -m spacy download xx_ent_wiki_sm
                nlp_models[lang] = spacy.load("xx_ent_wiki_sm")
            else:
                nlp_models[lang] = None
        except:
            nlp_models[lang] = None

# Initialize LanguageTool with error handling
tools = {}
try:
    # Try to initialize LanguageTool for each language
    for lang, code in {'English': 'en-US', 'French': 'fr'}.items():
        try:
            tools[lang] = language_tool_python.LanguageTool(code)
        except Exception as e:
            print(f"Warning: Could not initialize LanguageTool for {lang}: {e}")
            tools[lang] = None
    
    # Arabic has limited LanguageTool support
    tools['Arabic'] = None
except Exception as e:
    print(f"Warning: LanguageTool initialization failed. Text correction will be disabled.\nError: {e}")
    print("To fix this issue, install Java 17 or higher (current version is too old).")
    # Set all tools to None if global initialization fails
    tools = {lang: None for lang in ['English', 'French', 'Arabic']}

def translate_text(text, source_lang, target_lang):
    if source_lang == target_lang:
        return text
    
    model_key = f"{source_lang}-{target_lang}"
    if model_key not in model_names:
        return "Translation not supported for this language pair"
    
    try:
        model_name = model_names[model_key]
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    except ImportError as e:
        if "sentencepiece" in str(e).lower():
            return "ERROR: Missing SentencePiece library. Please run: pip install sentencepiece"
        else:
            return f"ERROR: {str(e)}"
    except Exception as e:
        return f"Translation error: {str(e)}"

def analyze_grammar(text, language):
    if language not in nlp_models or nlp_models[language] is None:
        return "Grammar analysis not available for this language"
    
    nlp = nlp_models[language]
    doc = nlp(text)
    
    analysis = []
    for token in doc:
        analysis.append(f"Word: {token.text}, POS: {token.pos_}, Dependency: {token.dep_}")
    return "\n".join(analysis)

def correct_text(text, language):
    if language not in tools or tools[language] is None:
        return text, ["Text correction not available. LanguageTool requires Java 17+ (you have an older version)."]
    
    try:
        tool = tools[language]
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        
        corrections = [f"Original: {m.context} -> Suggested: {m.replacements[0] if m.replacements else 'N/A'}" 
                      for m in matches]
        return corrected, corrections
    except Exception as e:
        return text, [f"Error during text correction: {str(e)}"]