import pymorphy2
import logging
from spellchecker import SpellChecker
from typing import Optional
from field_aliases import field_aliases

logger = logging.getLogger(__name__)

class SynonymAgent:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.spell = SpellChecker(language='ru')
        self.synonym_map = field_aliases

    def normalize_word(self, word: str) -> str:
        parsed = self.morph.parse(word)
        if parsed and parsed[0]:
            lemma = parsed[0].normal_form
            logger.debug(f"Нормализовано '{word}' -> '{lemma}'")
            return lemma
        return word

    def correct_word(self, word: str) -> str:
        if word not in self.spell:
            corrected = self.spell.correction(word)
            if corrected != word:
                logger.debug(f"Исправлено '{word}' -> '{corrected}'")
            return corrected
        return word

    def find_field(self, text: str) -> Optional[str]:
        text_lower = text.lower().strip()

        # Сначала ищем по полной фразе
        for field, synonyms in self.synonym_map.items():
            if text_lower in synonyms:
                logger.debug(f"Найдено поле '{field}' по целому выражению: '{text_lower}'")
                return field

        # Потом ищем по словам
        words = text_lower.split()
        for word in words:
            corrected_word = self.correct_word(word)
            norm_word = self.normalize_word(corrected_word)
            for field, synonyms in self.synonym_map.items():
                if norm_word in synonyms or corrected_word in synonyms:
                    logger.debug(f"Найдено поле '{field}' по слову '{word}' (исправлено: '{corrected_word}', нормализация: '{norm_word}')")
                    return field

        return None
