import spacy
from googletrans import Translator

loadModel = spacy.load('ru_core_news_sm', disable = ['parser', 'ner'])

TRANSFILE = open(r"data\updatedTranslations.csv", "r", encoding = 'utf-8')
WORDSFILE = open(r"data\words.csv", "r", encoding = 'utf-8')
transContents = TRANSFILE.readlines()
wordsContents = WORDSFILE.readlines()


class Book():
    def __init__(self, contents, googleTranslate):
        self.googleTranslate = googleTranslate
        self.words = self.filterContents(contents)

    def filterContents(self, contents):
        contents = contents.split()
        output = []
        puncutation = ",.;?!«»"
        wordArr = []
        for word in contents:
            word = word.strip()
            newWord = ""
            for char in word:
                if not char in puncutation:
                    newWord += char
            if "-" in newWord:
                transWord = ""
                copyWord = newWord
                while "-" in copyWord:
                    dashIndex = copyWord.find("-")
                    tempWord = loadModel(copyWord[:dashIndex])
                    transWord += tempWord[0].lemma_ + "-"
                    copyWord = copyWord[dashIndex + 1:]
                    if not "-" in copyWord:
                        tempWord = loadModel(copyWord)
                        transWord += tempWord[0].lemma_
                output.append([newWord, word, transWord, self.findTranslation(transWord, self.googleTranslate)])
            else:
                transWord = loadModel(newWord.lower())
                output.append([newWord, word, transWord[0].lemma_, self.findTranslation(transWord[0].lemma_, self.googleTranslate)])
        return output
   
    @staticmethod
    def findTranslation(untranslatedWord, googleTranslate):
        if googleTranslate:
            translator = Translator()
            word = translator.translate(untranslatedWord)
            print(word.text)
            return word.text
        else:
            wordIndex = -1
            for line in wordsContents:
                innerContents = line.split(",")
                if innerContents[2] == untranslatedWord:
                    wordIndex = innerContents[0]
                    break
            if not wordIndex == -1:
                translation = ""
                for line in transContents:
                    innerContents = line.split(",")
                    if innerContents[2] == wordIndex:
                        if len(innerContents) == 8:
                            translation += innerContents[4] + "\n"
                        else:
                            for i in range(4, len(innerContents) - 3):
                                translation += innerContents[i] + ", "
                            translation = (translation[:-3] + "\n").replace('"', "")
                    if not translation == "" and not innerContents[2] == wordIndex:
                        break
                return translation
            else:
                return ""