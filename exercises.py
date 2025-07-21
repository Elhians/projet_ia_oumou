import random

def generate_quiz(level, source_lang, target_lang):
    # Language-specific vocabulary with proper translations
    vocabulary = {
        'English': {
            'Hello': {'French': 'Bonjour', 'Arabic': 'مرحبا'},
            'Book': {'French': 'Livre', 'Arabic': 'كتاب'},
            'Thank you': {'French': 'Merci', 'Arabic': 'شكرا'},
            'Yes': {'French': 'Oui', 'Arabic': 'نعم'},
            'No': {'French': 'Non', 'Arabic': 'لا'},
            'Goodbye': {'French': 'Au revoir', 'Arabic': 'وداعا'},
            'I am learning': {'French': 'J\'apprends', 'Arabic': 'أنا أتعلم'},
            'The book is on the table': {'French': 'Le livre est sur la table', 'Arabic': 'الكتاب على الطاولة'},
        },
        'French': {
            'Bonjour': {'English': 'Hello', 'Arabic': 'مرحبا'},
            'Livre': {'English': 'Book', 'Arabic': 'كتاب'},
            'Merci': {'English': 'Thank you', 'Arabic': 'شكرا'},
            'Oui': {'English': 'Yes', 'Arabic': 'نعم'},
            'Non': {'English': 'No', 'Arabic': 'لا'},
            'Au revoir': {'English': 'Goodbye', 'Arabic': 'وداعا'},
            'J\'apprends': {'English': 'I am learning', 'Arabic': 'أنا أتعلم'},
            'Le livre est sur la table': {'English': 'The book is on the table', 'Arabic': 'الكتاب على الطاولة'},
        },
        'Arabic': {
            'مرحبا': {'English': 'Hello', 'French': 'Bonjour'},
            'كتاب': {'English': 'Book', 'French': 'Livre'},
            'شكرا': {'English': 'Thank you', 'French': 'Merci'},
            'نعم': {'English': 'Yes', 'French': 'Oui'},
            'لا': {'English': 'No', 'French': 'Non'},
            'وداعا': {'English': 'Goodbye', 'French': 'Au revoir'},
            'أنا أتعلم': {'English': 'I am learning', 'French': 'J\'apprends'},
            'الكتاب على الطاولة': {'English': 'The book is on the table', 'French': 'Le livre est sur la table'},
        }
    }
    
    # Different question types
    question_types = [
        "translation",  # Basic translation
        "fill_blank",   # Fill in the blank
        "match"         # Match the word to its meaning
    ]
    
    # If source language vocabulary is not available, default to English
    if source_lang not in vocabulary:
        source_lang = "English"
    
    # Get appropriate words based on level
    if level == "Beginner":
        word_count = 5  # Use first 5 words for beginners
        question_types = ["translation"]  # Only simple translations for beginners
    elif level == "Intermediate":
        word_count = 7  # Use more words for intermediate
    else:  # Advanced
        word_count = len(vocabulary[source_lang])  # Use all words
    
    # Select a subset of words based on level
    source_words = list(vocabulary[source_lang].keys())[:word_count]
    
    # Generate questions
    questions = []
    for question_type in question_types:
        if question_type == "translation" and len(questions) < 3:  # Limit to 3 translation questions
            # Create translation questions - ensure we get at least some words
            sample_words = random.sample(source_words, min(2, len(source_words)))
            
            # Debug check - if no words, add some defaults
            if not sample_words:
                if source_lang == "English":
                    sample_words = ["Hello", "Thank you"]
                elif source_lang == "French":
                    sample_words = ["Bonjour", "Merci"]
                else:  # Arabic or other
                    sample_words = ["مرحبا", "شكرا"]
            
            for word in sample_words:
                # First check if this word has a translation
                if target_lang in vocabulary.get(source_lang, {}).get(word, {}):
                    correct_answer = vocabulary[source_lang][word][target_lang]
                    
                    # Get wrong options from target language vocabulary
                    target_vocab = list(vocabulary.get(target_lang, {}).keys())
                    if not target_vocab:  # If no vocab available
                        if target_lang == "English":
                            wrong_options = ["House", "Car", "Tree"]
                        elif target_lang == "French":
                            wrong_options = ["Maison", "Voiture", "Arbre"]
                        else:  # Arabic or other
                            wrong_options = ["بيت", "سيارة", "شجرة"]
                    else:
                        # Filter out the correct answer if it's in the list
                        wrong_options_pool = [w for w in target_vocab if str(w) != str(correct_answer)]
                        wrong_options = random.sample(wrong_options_pool, min(3, len(wrong_options_pool)))
                    
                    # Create question with context
                    context = ""
                    if len(word.split()) > 1:  # It's a phrase
                        context = f" (in a conversation)"
                    
                    questions.append({
                        'question': f'Translate "{word}" from {source_lang} to {target_lang}{context}:',
                        'options': [correct_answer] + wrong_options,
                        'correct_answer': correct_answer
                    })
                else:
                    # Fallback for missing translation - create a generic question
                    questions.append({
                        'question': f'Which word means "Hello" in {target_lang}?',
                        'options': ['Bonjour' if target_lang == 'French' else 'مرحبا' if target_lang == 'Arabic' else 'Hello', 
                                   'Merci' if target_lang == 'French' else 'شكرا' if target_lang == 'Arabic' else 'Thank you',
                                   'Au revoir' if target_lang == 'French' else 'وداعا' if target_lang == 'Arabic' else 'Goodbye'],
                        'correct_answer': 'Bonjour' if target_lang == 'French' else 'مرحبا' if target_lang == 'Arabic' else 'Hello'
                    })
    
    # Always ensure we have at least one question
    if not questions:
        questions.append({
            'question': f'Which word means "Hello" in {target_lang}?',
            'options': ['Bonjour' if target_lang == 'French' else 'مرحبا' if target_lang == 'Arabic' else 'Hello', 
                       'Merci' if target_lang == 'French' else 'شكرا' if target_lang == 'Arabic' else 'Thank you',
                       'Au revoir' if target_lang == 'French' else 'وداعا' if target_lang == 'Arabic' else 'Goodbye'],
            'correct_answer': 'Bonjour' if target_lang == 'French' else 'مرحبا' if target_lang == 'Arabic' else 'Hello'
        })
    
    # If we need more questions, add fill-in-the-blank for intermediate/advanced
    if level != "Beginner" and len(questions) < 4:
        # Add fill-in-the-blank questions for intermediate and advanced levels
        sentences = {
            'English': [
                "I ___ going to the store",
                "She ___ a new book yesterday",
                "They ___ learning a new language",
                "Please ___ me with this exercise"
            ],
            'French': [
                "Je ___ à la bibliothèque",
                "Elle ___ un nouveau livre",
                "Ils ___ une nouvelle langue",
                "S'il vous plaît, ___ moi avec cet exercice"
            ],
            'Arabic': [
                "أنا ___ إلى المتجر",
                "هي ___ كتابًا جديدًا بالأمس",
                "هم ___ لغة جديدة",
                "من فضلك ___ في هذا التمرين"
            ]
        }
        
        fill_options = {
            'English': {
                'am': ['am', 'is', 'are', 'be'],
                'bought': ['bought', 'buy', 'buys', 'buying'],
                'are': ['are', 'is', 'am', 'be'],
                'help': ['help', 'assist', 'aid', 'support']
            },
            'French': {
                'vais': ['vais', 'va', 'allons', 'allez'],
                'achète': ['achète', 'achetez', 'achètes', 'achètent'],
                'apprennent': ['apprennent', 'apprend', 'apprenons', 'apprenez'],
                'aidez': ['aidez', 'aide', 'aident', 'aidons']
            },
            'Arabic': {
                'أذهب': ['أذهب', 'تذهب', 'يذهب', 'نذهب'],
                'اشترت': ['اشترت', 'اشترى', 'تشتري', 'يشتري'],
                'يتعلمون': ['يتعلمون', 'يتعلم', 'تتعلم', 'نتعلم'],
                'ساعدني': ['ساعدني', 'ساعد', 'يساعد', 'تساعد']
            }
        }
        
        # Select a sentence for the target language
        if len(sentences.get(target_lang, [])) > 0:
            # Pick a random sentence index
            idx = random.randint(0, min(3, len(sentences[target_lang])-1))
            sentence = sentences[target_lang][idx]
            
            # Get the corresponding word options
            word_key = list(fill_options[target_lang].keys())[idx]
            options = fill_options[target_lang][word_key]
            correct_answer = options[0]  # First option is always correct
            
            # Create the question
            questions.append({
                'question': f'Complete the sentence in {target_lang}: "{sentence}"',
                'options': options.copy(),  # Copy to avoid modifying original
                'correct_answer': correct_answer
            })
    
    # Randomize the order of options for each question
    for q in questions:
        random.shuffle(q['options'])
    
    return questions