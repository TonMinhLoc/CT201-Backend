from translate import Translator

translator = Translator(provider='libre', to_lang="vi")
text = "Enter a valid value."
translated_text = translator.translate(text)
print(translated_text)
