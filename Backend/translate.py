from deep_translator import GoogleTranslator

text = "How can I help you?"

translated = GoogleTranslator(
    source='auto',
    target='en'
).translate(text)

print(translated)