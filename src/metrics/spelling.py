from spellchecker import SpellChecker
from nltk.stem.snowball import SnowballStemmer

from natasha import MorphVocab, Doc, NewsNERTagger, NewsMorphTagger, NewsEmbedding, Segmenter

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)
morph_tagger = NewsMorphTagger(emb)

spell = SpellChecker(language='ru')
stemmer = SnowballStemmer("russian")

# find those words that may be misspelled


def count_spelling_mistakes(text):
    """
    For a given document, return the average sentence length.
    """

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    lemmas = []

    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        lemmas.append(token.lemma)

    misspelled = spell.unknown(lemmas)

    return f'{len(misspelled)} из {len(lemmas)} слов нет в словаре'


