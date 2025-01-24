def convertMorseToText(morse_code):
    morse_dict = {
        '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd',
        '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h',
        '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
        '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
        '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
        '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
        '-.--': 'y', '--..': 'z', '/': ' '
    }

    words = morse_code.strip().split(' / ')  # Split by words (using "/" for separation)
    translation = []

    for word in words:
        letters = word.split()  # Split letters within each word
        translated_word = ''.join(morse_dict.get(letter, '?') for letter in letters)
        translation.append(translated_word)

    return ' '.join(translation)






    
