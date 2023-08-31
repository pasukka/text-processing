from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import pymorphy2
from collections import Counter
import string
import shutil
import os
from os import path


class FilterText:

    def __init__(self):
        self.fileName = ''
        self.text = ''
        self.charsToRemove = []
        self.textLem = []
        self.filteredText = []
        self.textWithouChars = ''
        self.textTokenized

    def removeCharsFromText(self, text: list, charsToRemove: list):
        self.textWithouChars = "".join([ch for ch in text if ch not in charsToRemove])
        return self.textWithouChars

    def makeCorpusFromHtml(self, fileName):
        self.fileName = fileName
        with open(fileName, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, features="lxml")
            self.text = soup.get_text()
        return self.text
    
    def lemmatize(self):
        morph = pymorphy2.MorphAnalyzer()
        for word in self.text:
            wordNew = morph.parse(word)[0].normal_form
            self.textLem.append(wordNew)
        return self.textLem

    def filterCorpus(self, listOfAdditionalStopwords=['это', 'также']):
        listOfStopwords = stopwords.words("russian") + stopwords.words("english")
        listOfStopwords.extend(listOfAdditionalStopwords)
        self.filteredText = [word for word in self.text if word not in listOfStopwords]
        return self.filteredText

    def tokenize(self, corpus):
        corpus = corpus.lower()
        specificChars = string.punctuation + '№#–\n\xa0«»\t—…-abcdefghijklmnopqrstuvwxyz'
        corpus = self.removeCharsFromText(corpus, specificChars)
        corpus = self.removeCharsFromText(corpus, string.digits)

        textTokens = word_tokenize(corpus)
        self.textTokenized = nltk.Text(textTokens)

        cyrillic = [chr(i) for i in range(ord('а'), ord('я') + 1)]
        self.textTokenized = [word for word in self.textTokenized if word not in cyrillic]
        return self.textTokenized
    
    def makeListFromDict(self, dict_common):
        listNew = []
        for i in dict_common:
            listNew.append(i[0])
        return listNew

    def textHasCommonWords(self, commonWords, dictCommon):
        inCommonWords = False
        for i in commonWords:
            dictWords = self.makeListFromDict(dictCommon)
            if i in dictWords:
                inCommonWords = True
                break
        return inCommonWords

    def textIsToInclude(self, text='', excludeWords=[], includeWords=[], excludeCommonWords=[], includeCommonWords=[]):
        if not text:
            countWords = Counter(self.text)
        else:
            countWords = Counter(text)
        dict_common = countWords.most_common(10)
        toInclude = 0
        if self.textHasCommonWords(excludeCommonWords, dict_common) == 1:  # to exclude
            toInclude = 0
        elif self.textHasCommonWords(includeCommonWords, dict_common) == 1:  # to include
            toInclude = 1
        else:
            for i in includeWords:
                if i in countWords:  # to include
                    toInclude = 1
                    break
            for i in excludeWords:
                if i in countWords:  # to exclude
                    toInclude = 0
                    break
            toInclude = 0  # not find
        return toInclude
    

class FilterCorpora:  # from html

    def __init__(self, path):
        self.path = path
        self.listOfTexts = []
        if not os.path.isdir(path):
            self.listOfTexts = [f for f in listdir(path) if isfile(join(path, f))]
            self.countTexts = len(self.listOfTexts)
        self.countTexts = 0
        self.corpora = ''
        self.includeTexts = []

    def sortTexts(self, excludeWords=[], includeWords=[], excludeCommonWords=[], includeCommonWords=[]):
        for text in self.listOfTexts:
            ft = FilterText()
            ft.makeCorpusFromHtml(self, text)
            toInclude = ft.sortText(excludeWords, includeWords, excludeCommonWords, includeCommonWords)
            if toInclude:
                self.includeTexts.append(ft)

    def moveFile(self, destinationPath):
        if path.exists(self.path):
            self.path = shutil.move(self.path, destinationPath)

    def copyFile(self, fileName, destinationPath):
        pathNew = destinationPath + fileName
        if not isfile(pathNew) and isfile(self.path + fileName):
            shutil.copy(self.path + fileName, pathNew)

    def extension(self, text, ext):
        isExtansion = False
        filename, fileExtension = os.path.splitext(self.path + text)
        if fileExtension == ext:
            isExtansion = True
        return isExtansion

    def writeToFile(self, path, text, specifier: string):
        with open(path, specifier, encoding="utf-8") as file:
            file.writelines(text)

    def makeCorpora(self, path=''):
        if not path:
            path = self.path
        with open(path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, features="lxml")
            self.corpora = soup.get_text()

    def makeOneFile(self, path, specifier='txt'):
        for text in self.listOfTexts:
            path_input = path + text
            self.makeCorpora(path_input)
            self.writeToFile("{}/{}.{}".format(path, path.splitext(text)[0], specifier), self.corpora, 'w')

    def makePathIfNot(self, targetPath):
        if not os.path.isdir(targetPath):
            os.mkdir(targetPath)
    
    def process_texts(self, excludeWords=[], includeWords=[], excludeCommonWords=[], includeCommonWords=[]):
        for text in self.listOfTexts:
            ft = FilterText()
            try:
                path_ = self.path + text
                ft.makeCorpusFromHtml(path_)
                ft.tokenize(ft.text)
                ft.lemmatize(ft.textTokenized)
                text = ft.filterCorpus(ft.Lem)
                toInclude = ft.textIsToInclude(text, excludeWords, includeWords, excludeCommonWords, includeCommonWords)
                if toInclude:
                    self.includeTexts.append(ft)
            except UnicodeDecodeError:
                pass