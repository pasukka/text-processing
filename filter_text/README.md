# Обработка текстового файла

✔ Python

✔ BeautifulSoup

✔ NLTK

✔ PyMorphy2

✔ Collections

## Описание задачи

Была поставлена задача обработки текста: удаление стоп-слов и символов, удаление из корпуса текстов, где есть ключевые слова, создание одного файла из нескольких.

## Описание работы программы

Обрабатывать можно как и отдельные тексты, так и целый корпус. 

## Пример использования для сортировки текстов по ключевым словам

```
excludeCommonWords = ["картинка",  "изображение", "image"]
excludeWords = ["голос", "голосовой", "ассистент"]
includeWords = ["текст", "корпус", "nlp", "language", "чат-бот"]

ft = FilterText()
ft.makeCorpusFromHtml(self, text)  # текст будет находиться в self.text
isToInclude = ft.textIsToInclude(excludeWords=excludeWords, includeWords=includeWords, excludeCommonWords=excludeCommonWords)  # если text пустой, то обработает self.text
```