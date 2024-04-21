
import customtkinter as CTk
import tkinter as tk
from tkinter import filedialog
from Book import Book
import spacy
import random

class App:
    def reset(self):
        self.readingFrame.grid_remove()
        self.learningMenuFrame.grid_remove()
        self.reviewWordsFrame.grid_remove()
        self.learnFrame.grid_remove()
        self.returnToMenuButton.place_forget()
        self.inputFile = None
        self.cur = []
        self.i = -1
        self.googleTranslate = False
        self.hasRightClicked = False
        if self.hasLoadedLetterGame:
            for button in self.letterArr:
                button.grid_remove()
            self.questionMarkButton.grid_remove()
            self.backspaceButton.grid_remove()
            self.hasLoadedLetterGame = False
        self.mainMenuFrame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")

    def __init__(self, root):
        self.root = root
        CTk.set_appearance_mode("light")
        CTk.set_default_color_theme("blue")
        
        self.hasLoadedLetterGame = False
        
        self.KNOWARR = []
        self.DKNOWARR = []
        
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        
        self.KNOWFILE = open("know.txt", "r+", encoding = 'utf-8')
        self.DKNOWFILE = open("dknow.txt", "r+", encoding = 'utf-8')
        self.writeToArr()
        
        self.returnToMenuButton = CTk.CTkButton(root, text="Return to Menu", command=self.reset)
        
        self.mainMenuFrame = CTk.CTkFrame(master=self.root)
        self.mainLabel = CTk.CTkLabel(self.mainMenuFrame, text="Привет!", font=("Arial", 120))
        self.mainLabel.place(relx=.5, rely=.4, anchor="center")
        self.fileButton = CTk.CTkButton(self.mainMenuFrame, text = 'Open File', command=self.openFile, width=175, height=90, corner_radius=20, font=("Arial", 17))
        self.fileButton.place(relx=.66, rely=.7, anchor="center")
        self.startLearningButton = CTk.CTkButton(self.mainMenuFrame, text='Start Learning', command=self.startLearningMenu, width=175, height=90, corner_radius=20, font=("Arial", 17))
        self.startLearningButton.place(relx=.33, rely=.7, anchor="center")
        
        self.readingFrame = CTk.CTkFrame(master=self.root)
        self.currentBookLabel = CTk.CTkLabel(self.readingFrame, text="")
        self.currentBookLabel.place(relx=.5, rely=0, anchor="n")
        self.statusLabel = CTk.CTkLabel(self.readingFrame, text="", font=("Arial", 20))
        self.statusLabel.place(relx=.5, rely=.1, anchor="center")
        self.currentWordLabel = CTk.CTkLabel(self.readingFrame, text="", font=("Arial", 96))
        self.currentWordLabel.place(relx=.5, rely=.4, anchor="center")
        self.translationLabel = CTk.CTkLabel(self.readingFrame, text="", font=("Arial", 30))
        self.translationLabel.place(relx=.5, rely=.7, anchor="center")
        readingFrameElements = [self.currentBookLabel, self.statusLabel, self.currentWordLabel, self.translationLabel, self.readingFrame]
        for element in readingFrameElements:
            element.bind("<Button-1>", self.know)
            element.bind("<Button-3>", self.dknow)
            element.bind("<MouseWheel>", self.mouseWheel)
            
        self.learningMenuFrame = CTk.CTkFrame(master=self.root)
        self.reviewWordsButton = CTk.CTkButton(self.learningMenuFrame, text="Review Words", command=self.startReviewWords, width=175, height=90, corner_radius=20, font=("Arial", 17))
        self.reviewWordsButton.place(relx=.5, rely=.4, anchor="center")
        self.learnButton = CTk.CTkButton(self.learningMenuFrame, text="Learn", command=self.startLearn, width=175, height=90, corner_radius=20, font=("Arial", 17))
        self.learnButton.place(relx=.5, rely=.6, anchor="center")
        
        self.reviewWordsFrame = CTk.CTkFrame(master=self.root)
        
        self.learnFrame = CTk.CTkFrame(master=self.root)
        self.instructionLabel = CTk.CTkLabel(self.learnFrame, text="Type the correct translation", font=("Arial", 20))
        self.instructionLabel.place(relx=.5, rely=.05, anchor="center")
        self.currentLearningWordLabel = CTk.CTkLabel(self.learnFrame, text="", font=("Arial", 60))
        self.currentLearningWordLabel.place(relx=.5, rely=.3, anchor="center")
        self.correctAnswerLabel = CTk.CTkLabel(self.learnFrame, text="", font=("Arial", 30))
        self.currentAnswerEntry = CTk.CTkLabel(self.learnFrame, text="", font=("Arial", 30))
        self.currentAnswerEntry.place(relx=.5, rely=.45, anchor="center")
        self.nextWordButton = CTk.CTkButton(self.learnFrame, text="Play Again?", command=self.startLearn, width=175, height=90, corner_radius=20, font=("Arial", 17))
        
        self.reset()

    def openFile(self):
        self.inputFile = filedialog.askopenfile(mode = 'rb', filetypes = [('Text Documents', '*.txt')])
        if self.inputFile is not None:
            encodings_to_try = ['utf-8', 'latin-1', 'utf-16']
            for encoding in encodings_to_try:
                try:
                    self.inputFile.seek(0)
                    fileContent = self.inputFile.read().decode(encoding)
                    self.book = Book(fileContent, self.googleTranslate)
                    break
                except UnicodeDecodeError:
                    continue
            self.startReading()
        else:
            print("Unable to decode the file with any of the specified encodings.")

    def startReading(self):
        self.mainMenuFrame.grid_remove()
        self.readingFrame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")
        self.returnToMenuButton.place(relx=.9, rely=0.035, anchor="center")
        self.statusLabel.configure(text="")
        self.currentBookLabel.configure(text= "File: " + self.inputFile.name, font=("Arial", 12))
        self.i = 0
        self.cur = self.book.words[self.i]
        self.currentWordLabel.configure(text=self.cur[1])

    def startLearningMenu(self):
        self.returnToMenuButton.place(relx=.9, rely=0.035, anchor="center")
        self.mainMenuFrame.grid_remove()
        self.learningMenuFrame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")

    def startReviewWords(self):
        self.learningMenuFrame.grid_remove()
        self.reviewWordsFrame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")
        
    def startLearn(self):
        self.hasLoadedLetterGame = True
        self.learningMenuFrame.grid_remove()
        self.learnFrame.grid(row=0, column=0, padx=20, pady=60, sticky="nsew")
        self.keyboardFrame = CTk.CTkFrame(self.learnFrame, fg_color="#DBDBDB")
        self.nextWordButton.place_forget()
        self.keyboardFrame.place(relx=.5, rely=.8, anchor="center")
        self.correctAnswerLabel.configure(text="")
        self.currentAnswerEntry.configure(text="", text_color="#1A1A1A")
        wordsWithEnglishTrans = []
        for word in self.DKNOWARR:
            if not Book.findTranslation(word, False) == "":
                wordsWithEnglishTrans.append(word)
        self.currentLearningWord = random.choice(wordsWithEnglishTrans)
        self.currentLearningWordLabel.configure(text=Book.findTranslation(self.currentLearningWord, False))
        print(self.currentLearningWord)
        self.genLetters()
        

    def genLetters(self):
        self.questionMarkButton = CTk.CTkButton(self.keyboardFrame, text="?", command=self.questionGuess, width=80, height=80, corner_radius=10, fg_color="#242426", font=("Arial", 20, "bold"))
        self.backspaceButton = CTk.CTkButton(self.keyboardFrame, text=u"\u232B", command=self.backspace, width=80, height=80, corner_radius=10, fg_color="#242426", font=("Arial", 20, "bold"))
        self.lastGuessedButton = []
        if len(self.currentLearningWord) <= 10:
            self.oneLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.oneLetterButton.configure(command=lambda b=self.oneLetterButton: self.guess(b))
            self.oneLetterButton.grid(row=0, column=0, padx=2, pady=2)
            
            self.twoLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.twoLetterButton.configure(command=lambda b=self.twoLetterButton: self.guess(b))
            self.twoLetterButton.grid(row=0, column=1, padx=2, pady=2)
            
            self.threeLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.threeLetterButton.configure(command=lambda b=self.threeLetterButton: self.guess(b))
            self.threeLetterButton.grid(row=0, column=2, padx=2, pady=2)
            
            self.fourLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.fourLetterButton.configure(command=lambda b=self.fourLetterButton: self.guess(b))
            self.fourLetterButton.grid(row=0, column=3, padx=2, pady=2)
            
            self.fiveLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.fiveLetterButton.configure(command=lambda b=self.fiveLetterButton: self.guess(b))
            self.fiveLetterButton.grid(row=1, column=0, padx=2, pady=2)
            
            self.sixLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.sixLetterButton.configure(command=lambda b=self.sixLetterButton: self.guess(b))
            self.sixLetterButton.grid(row=1, column=1, padx=2, pady=2)
            
            self.sevenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.sevenLetterButton.configure(command=lambda b=self.sevenLetterButton: self.guess(b))
            self.sevenLetterButton.grid(row=1, column=2, padx=2, pady=2)
            
            self.eightLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.eightLetterButton.configure(command=lambda b=self.eightLetterButton: self.guess(b))
            self.eightLetterButton.grid(row=1, column=3, padx=2, pady=2)
            
            self.nineLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.nineLetterButton.configure(command=lambda b=self.nineLetterButton: self.guess(b))
            self.nineLetterButton.grid(row=2, column=0, padx=2, pady=2)
            
            self.tenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.tenLetterButton.configure(command=lambda b=self.tenLetterButton: self.guess(b))
            self.tenLetterButton.grid(row=2, column=1, padx=2, pady=2)
            
            self.questionMarkButton.grid(row=2, column=2, padx=2, pady=2)
            self.backspaceButton.grid(row=2, column=3, padx=2, pady=2)
            self.letterArr = [self.oneLetterButton, self.twoLetterButton, self.threeLetterButton, self.fourLetterButton, self.fiveLetterButton, self.sixLetterButton, self.sevenLetterButton, self.eightLetterButton, self.nineLetterButton, self.tenLetterButton]
        else:
            self.oneLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.oneLetterButton.configure(command=lambda b=self.oneLetterButton: self.guess(b))
            self.oneLetterButton.grid(row=0, column=0, padx=2, pady=2)
            
            self.twoLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.twoLetterButton.configure(command=lambda b=self.twoLetterButton: self.guess(b))
            self.twoLetterButton.grid(row=0, column=1, padx=2, pady=2)
            
            self.threeLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.threeLetterButton.configure(command=lambda b=self.threeLetterButton: self.guess(b))
            self.threeLetterButton.grid(row=0, column=2, padx=2, pady=2)
            
            self.fourLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.fourLetterButton.configure(command=lambda b=self.fourLetterButton: self.guess(b))
            self.fourLetterButton.grid(row=0, column=3, padx=2, pady=2)
            
            self.fiveLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.fiveLetterButton.configure(command=lambda b=self.fiveLetterButton: self.guess(b))
            self.fiveLetterButton.grid(row=0, column=4, padx=2, pady=2)
            
            self.sixLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.sixLetterButton.configure(command=lambda b=self.sixLetterButton: self.guess(b))
            self.sixLetterButton.grid(row=0, column=5, padx=2, pady=2)
            
            self.sevenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.sevenLetterButton.configure(command=lambda b=self.sevenLetterButton: self.guess(b))
            self.sevenLetterButton.grid(row=1, column=0, padx=2, pady=2)
            
            self.eightLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.eightLetterButton.configure(command=lambda b=self.eightLetterButton: self.guess(b))
            self.eightLetterButton.grid(row=1, column=1, padx=2, pady=2)
            
            self.nineLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.nineLetterButton.configure(command=lambda b=self.nineLetterButton: self.guess(b))
            self.nineLetterButton.grid(row=1, column=2, padx=2, pady=2)
            
            self.tenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.tenLetterButton.configure(command=lambda b=self.tenLetterButton: self.guess(b))
            self.tenLetterButton.grid(row=1, column=3, padx=2, pady=2)
            
            self.elevenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.elevenLetterButton.configure(command=lambda b=self.elevenLetterButton: self.guess(b))
            self.elevenLetterButton.grid(row=1, column=4, padx=2, pady=2)
            
            self.twelveLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.twelveLetterButton.configure(command=lambda b=self.twelveLetterButton: self.guess(b))
            self.twelveLetterButton.grid(row=1, column=6, padx=2, pady=2)
            
            self.thirteenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.thirteenLetterButton.configure(command=lambda b=self.thirteenLetterButton: self.guess(b))
            self.thirteenLetterButton.grid(row=2, column=0, padx=2, pady=2)
            
            self.fourteenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.fourteenLetterButton.configure(command=lambda b=self.fourteenLetterButton: self.guess(b))
            self.fourteenLetterButton.grid(row=2, column=1, padx=2, pady=2)
            
            self.fifteenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.fifteenLetterButton.configure(command=lambda b=self.fifteenLetterButton: self.guess(b))
            self.fifteenLetterButton.grid(row=2, column=2, padx=2, pady=2)
            
            self.sixteenLetterButton = CTk.CTkButton(self.keyboardFrame, text="")
            self.sixteenLetterButton.configure(command=lambda b=self.sixteenLetterButton: self.guess(b))
            self.sixteenLetterButton.grid(row=2, column=3, padx=2, pady=2)
            
            self.questionMarkButton.grid(row=2, column=4, padx=2, pady=2)
            self.backspaceButton.grid(row=2, column=5, padx=2, pady=2)
            
            self.letterArr = [self.oneLetterButton, self.twoLetterButton, self.threeLetterButton, self.fourLetterButton, self.fiveLetterButton, self.sixLetterButton, self.sevenLetterButton, self.eightLetterButton, self.nineLetterButton, self.tenLetterButton, self.elevenLetterButton, self.twelveLetterButton, self.thirteenLetterButton, self.fourteenLetterButton, self.fifteenLetterButton, self.sixteenLetterButton]

        copyWord = self.currentLearningWord
        if not len(self.currentLearningWord) == len(self.letterArr):
            for i in range(len(self.letterArr)-len(self.currentLearningWord)):
                copyWord += "."
        copyWord = ''.join(random.sample(list(copyWord), len(copyWord)))
        for button in self.letterArr:
            if copyWord[0] == ".":
                button.configure(text="", width=45, height=45, corner_radius=15, fg_color="#4a4a4a", state="disabled")
            else:
                button.configure(text=copyWord[0], width=80, height=80, corner_radius=25, fg_color="#242426", font=("Arial", 30, "bold"), state="normal")
            copyWord = copyWord[1:]
                
    def guess(self, clickedButton):
        clickedButton.configure(state="disabled")
        clickedButton.configure(font=("Arial", 25), fg_color="#313131")
        self.lastGuessedButton.append(clickedButton)
        self.currentAnswerEntry.configure(text=self.currentAnswerEntry.cget("text") + clickedButton.cget("text"))
        if len(self.currentAnswerEntry.cget("text")) == len(self.currentLearningWord):
            self.questionMarkButton.configure(state="disabled")
            self.backspaceButton.configure(state="disabled")
            if self.currentAnswerEntry.cget("text") == self.currentLearningWord:
                self.currentAnswerEntry.configure(text_color="green")
            else:
                self.currentAnswerEntry.configure(text_color="red")
                self.correctAnswerLabel.configure(text=self.currentLearningWord)
                self.correctAnswerLabel.place(relx=.5, rely=.5, anchor="center")
            self.keyboardFrame.place_forget()
            self.nextWordButton.place(relx=.5, rely=.8, anchor="center")
            
        
    def questionGuess(self):
        if len(self.currentAnswerEntry.cget("text")) < len(self.currentLearningWord):
            curIndex = len(self.currentAnswerEntry.cget("text"))
            correctLetter = self.currentLearningWord[curIndex]
            for button in self.letterArr:
                if button.cget("text") == correctLetter:
                    self.guess(button)
                    break

    def backspace(self):
        if not len(self.currentAnswerEntry.cget("text")) == 0:
            self.currentAnswerEntry.configure(text=self.currentAnswerEntry.cget("text")[:-1])
            print(len(self.lastGuessedButton))
            if len(self.lastGuessedButton) > 0:
                self.lastGuessedButton[len(self.lastGuessedButton) - 1].configure(state="normal", font=("Arial", 30), fg_color="#242426")
                self.lastGuessedButton.pop()

    def know(self, event):
        self.hasRightClicked = False
        if self.cur[2] not in self.KNOWARR and self.cur[2] not in self.DKNOWARR:
            self.KNOWARR.append(self.cur[2])
        self.increment()

    def dknow(self, event):
        if self.hasRightClicked:
            if self.cur[2] not in self.DKNOWARR and self.cur[2] not in self.KNOWARR:
                self.DKNOWARR.append(self.cur[2])
            self.hasRightClicked = False
            self.increment()
        else:
            self.translationLabel.configure(text=self.cur[3])
            self.hasRightClicked = True

    def increment(self):
        if not self.i == len(self.book.words) - 1:
            self.i += 1
            self.cur = self.book.words[self.i]
            self.currentWordLabel.configure(text=self.cur[1])
            self.translationLabel.configure(text="")
        else:
            self.statusLabel.configure(text="Reached end of file.")
            
    def decrement(self):
        if not self.i == 0:
            self.i -= 1
            self.cur = self.book.words[self.i]
            self.currentWordLabel.configure(text=self.cur[1])
            self.translationLabel.configure(text="")
            
    def mouseWheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.decrement()
        if event.num == 4 or event.delta == 120:
            self.increment()
            
    def writeToArr(self):
        known = self.KNOWFILE.read().split(",")
        dknown = self.DKNOWFILE.read().split(",")
        for word in known:
            self.KNOWARR.append(word)
        for word in dknown:
            self.DKNOWARR.append(word)

    def writeToFile(self):
        self.KNOWFILE.seek(0)
        self.DKNOWFILE.seek(0)
        self.KNOWFILE.truncate(0)
        self.DKNOWFILE.truncate(0)
        for word in self.KNOWARR:
            if not word == "":
                self.KNOWFILE.write(word + ",")
        for word in self.DKNOWARR:
            if not word == "":
                self.DKNOWFILE.write(word + ",")
        self.KNOWFILE.close()
        self.DKNOWFILE.close()
        print("Files closed")

if __name__ == "__main__":
    root = CTk.CTk()
    root.geometry("900x900")
    root.title("RuReader")
    app = App(root)
    root.mainloop()
    app.writeToFile()

print("Done")
