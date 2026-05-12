import re
import string


class NLPProcessor:

    
    def __init__(self):
        self.nlp = None
        self._load_spacy()
    
    def _load_spacy(self):
        try:
            import spacy
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
                self.nlp = spacy.load("en_core_web_sm")
        except ImportError:
            print("spaCy not installed")
            self.nlp = None
    
    def process(self, text):
        if not text:
            return {
                'original': '',
                'cleaned': '',
                'tokens': [],
                'entities': [],
                'sentences': []
            }
        
        cleaned_text = self._clean_text(text)
        
        if self.nlp:
            doc = self.nlp(cleaned_text)
            
            tokens = [token.text.lower() for token in doc 
                     if not token.is_stop and not token.is_punct and token.text.strip()]
            
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            
            sentences = [sent.text for sent in doc.sents]
            
            return {
                'original': text,
                'cleaned': cleaned_text,
                'tokens': tokens,
                'entities': entities,
                'sentences': sentences,
                'doc': doc
            }
        else:
            tokens = self._simple_tokenize(cleaned_text)
            return {
                'original': text,
                'cleaned': cleaned_text,
                'tokens': tokens,
                'entities': [],
                'sentences': cleaned_text.split('.')
            }
    
    def _clean_text(self, text):
        text = text.lower()
        
        text = re.sub(r'http\S+|www\S+', '', text)
        
        text = re.sub(r'\S+@\S+', ' EMAIL ', text)
        
        text = re.sub(r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}', ' PHONE ', text)
        
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'[^\w\s\.\,\-\+\#]', ' ', text)
        
        return text.strip()
    
    def _simple_tokenize(self, text):

        text = text.translate(str.maketrans('', '', string.punctuation))
        
        tokens = text.split()
        
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
                     'dare', 'ought', 'used', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        
        tokens = [t for t in tokens if t.lower() not in stop_words and len(t) > 1]
        
        return tokens
    
    def extract_noun_phrases(self, doc):

        if not doc:
            return []
        
        return [chunk.text for chunk in doc.noun_chunks]
    
    def get_pos_tags(self, doc):

        if not doc:
            return []
        
        return [(token.text, token.pos_) for token in doc]