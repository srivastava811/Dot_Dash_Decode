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






    
# def convertMorseToText(s):

#     morseDict={
#         '' : 'Check', #empty inputs
#     '.-': 'a',
#     '-...': 'b',
#     '-.-.': 'c',
#     '-..': 'd',
#     '.': 'e',
#     '..-.': 'f',
#     '--.': 'g',
#     '....': 'h',
#     '..': 'i',
#     '.---': 'j',
#     '-.-': 'k',
#     '.-..': 'l',
#     '--': 'm',
#     '-.': 'n',
#     '---': 'o',
#     '.--.': 'p',
#     '--.-': 'q',
#     '.-.': 'r',
#     '...': 's',
#     '-': 't',
#     '..-': 'u',
#     '...-': 'v',
#     '.--': 'w',
#     '-..-': 'x',
#     '-.--': 'y',
#     '--..': 'z',
#     '.-.-': ' '
#     }

#     if morseDict.get(s)!='Check':  #morseDict.get(s) attempts to retrieve the value for the key s from the dictionary.
#        return (morseDict.get(s))   #If s is not found in the dictionar , get() returns None.

# def convertMorseToText(morse_code):
#     morse_dict = {
#         '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', 
#         '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h', 
#         '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', 
#         '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', 
#         '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', 
#         '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', 
#         '-.--': 'y', '--..': 'z', '': ' ', '/': ' '
#     }

#     # Split the Morse code by spaces and convert to text
#     words = morse_code.strip().split('   ')  # Triple space between words
#     translation = []

#     for word in words:
#         letters = word.split()
#         translated_word = ''.join(morse_dict.get(letter, '?') for letter in letters)
#         translation.append(translated_word)

#     return ' '.join(translation)
