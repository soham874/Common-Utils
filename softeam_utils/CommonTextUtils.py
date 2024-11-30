import re

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def clean_text_dynamic(raw_text):
    
    cleaned_text = re.sub(r'\s+', ' ', raw_text)

    cleaned_text = re.sub(r'[^a-zA-Z0-9 ,.]', '', cleaned_text)
    return cleaned_text.strip()

def summarize_using_lsa(
    text, 
    num_sentences = 3
):
    parser = PlaintextParser.from_string(text, Tokenizer(language="english"))  # Added the language parameter
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    
    return [str(sentence) for sentence in summary]