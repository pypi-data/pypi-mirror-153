from enum import Enum


class Languages(str, Enum):
    en = 'en'
    pt_br = 'pt-br'


class Translate:
    @staticmethod
    def translate(text: str, language: Languages) -> str:
        languages = {
            'pt-br': '{number} min leitura',
        }

        if language.value in languages:
            number = text.split()[0]
            return languages[language.value].format(number=number)

        return text
