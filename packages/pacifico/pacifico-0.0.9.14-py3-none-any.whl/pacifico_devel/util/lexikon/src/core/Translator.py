import typing as typ
import deepl

from pacifico_devel.util.lexikon.src.util.Enumerations import Language
from pacifico_devel.util.cfg import Configuration


class Translator:
    """
    Class that implements language translator (probably with deep learning).
    """
    _KEY_NAME = "deepl_translator_key"

    @classmethod
    def translate(cls,
                  text: typ.Union[str, typ.Iterable[str]],
                  languageInput: Language,
                  languageOutput: Language) -> typ.Union[str, typ.List[str]]:
        """

        Args:
            text:
            languageInput:
            languageOutput:

        Returns: translated text

        """

        translator = deepl.Translator(cls._getKey())
        print(f"SOURCE LANG: {languageInput.deeplStringOutput}")
        print(f"TARGET LANG: {languageOutput.deeplStringOutput}")
        if isinstance(text, str):
            if languageInput is languageOutput:
                return text
            result = translator.translate_text(text=text,
                                               source_lang=languageInput.deeplStringInput,
                                               target_lang=languageOutput.deeplStringOutput)
            return result.text
        elif hasattr(text, "__iter__"):
            if languageInput is languageOutput:
                return list(text)
            result = translator.translate_text(text=text,
                                               source_lang=languageInput.deeplStringInput,
                                               target_lang=languageOutput.deeplStringOutput)
            return [res.text for res in result]

        raise ValueError(f"Invalid input: {text} of type {type(text)}. Must be of type str or an iterable of str.")

    @classmethod
    def _getKey(cls):
        """ Returns key from key-keeper"""
        return Configuration.get(cls._KEY_NAME)


if __name__ == '__main__':
    text = """Aumentamos nuestra proyección de IPC de marzo desde 0.94 % hasta 1.08 % sin consecuencias relevantes para el acumulado del año. El seguimiento
    a productos como cigarrillos y gas por red nos llevó a adelantar la variación mensual que esperábamos ocurriera en el segundo trimestre. Para el caso
del precio del gas licuado empiezan a materializarse los riesgos al alza: desde la proyección inicial del mes preveíamos aumentos significativos, pero
el seguimiento de precios nos llevó a proyectar un incremento aún mayor. Todo lo anterior se vio parcialmente compensado por una mayor caída
proyectada para el pasaje en bus interurbano."""

    translation = Translator.translate(text=text,
                                       languageInput=Language.English_US,
                                       languageOutput=Language.Spanish)

    print(f"ORIGINAL TEXT: {text}")
    print(f"TRANSLATED TEXT: {translation}")
