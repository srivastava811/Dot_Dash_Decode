# Define a dictionary for Morse code translation
morse_dict = {
    '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd',
    '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h',
    '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
    '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
    '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
    '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
    '-.--': 'y', '--..': 'z', '/': ' '  # '/' represents a space between words
}

# Function to convert Morse code to English text
def convertMorseToText(morse_code):
    """
    Converts a Morse code string into English text.
    Each letter is separated by a space, and each word by a '/'.
    
    :param morse_code: A string containing Morse code.
    :return: The English translation of the Morse code.
    """
    # Split the Morse code into words using ' / '
    words = morse_code.strip().split(' / ')
    translation = []

    # Translate each word
    for word in words:
        letters = word.split()  # Split letters within the word
        translated_word = ''.join(morse_dict.get(letter, '?') for letter in letters)
        translation.append(translated_word)

    return ' '.join(translation)
