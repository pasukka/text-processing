import os
from os import listdir
from os.path import isfile, join
import codecs
import shutil

class Decode:
    def __init__(self):
        self.sourceDirName = "./"
        self.targetDirName = "./changed_files/"
        self.format_in = 'utf-8'
        self.format_out = 'cp1251'
        self.listErrorFiles = []

    def setFormatInput(self, format_input):
        self.format_in = format_input

    def setFormatOutput(self, format_output):
        self.format_out = format_output

    def setSourceDirName(self, name):
        self.sourceDirName = name

    def setTargeDirName(self, name):
        self.targetDirName = name

    def codec_file(self, fileName):
        path = self.targetDirName + fileName
        if not isfile(path):
            f = codecs.open(self.sourceDirName + fileName, 'rb', self.format_in)
            try:
                u = f.read()  # the contents have been transformed to a Unicode string
                out = codecs.open(path, 'w', self.format_out)
                out.write(u)  # the contents have been output as UTF-8
            except UnicodeDecodeError:
                self.listErrorFiles.append(fileName)
                pass
    
    def change_codec(self, path):
        filesList = [f for f in listdir(path) if isfile(join(path, f))]
        for file in filesList:
            self.codec_file(file)

    def move_error_files(self):
        for file_name in self.listErrorFiles:
            path = self.sourceDirName + file_name
            if isfile(path):
                shutil.move(self.sourceDirName + file_name, self.targetDirName)

    def remove_files(self, mypath):
        if os.path.isdir:
            filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            for text in filesList:
                os.remove(mypath + text)


d = Decode()
mypath = './change_codecs/txt/'
d.change_codec(mypath)