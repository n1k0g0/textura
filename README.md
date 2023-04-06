# Textura WEB

### Инструмент комплексного анализа текста по относительным числовым показателям

Textura – консольное приложение для гуманитарного исследования текста в цифровых метриках, позволяющее оценить показатели произвольного текста в сравнении с текстами НКРЯ и спрогнозировать наиболее близкую подгруппу корпуса в одном из разрезов НКРЯ (по эпохе создания, типу текста,...)

Проект нацелен на помощь цифровым гуманитарным исследователям, литературоведам и другим пользователям, заинтересованным в исследовании гуманитарных свойств текстов. 

Более полное описание TEXTURA доступно в [официальной статье](https://docs.google.com/document/d/1gi-7A69SDtH7Pp8TjVJWitFL3kkwZhgcatr2nBVNuz4/edit#heading=h.b92faztiq4z2), посвященной проекту. 

Над проектом работали:
- Николай Горбачев
- Татьяна Чечельницкая

## Установка

### Mac/Linux

1. Загрузить .ZIP архив: **Code** -> **Download ZIP**

2. Перейти в загруженную папку в терминале:

`cd .../<Downloads Folder>/textura-main`

3. Ввести в терминале:

`sh mac-install.sh`

`sh mac-run.sh`

### Windows

1. Загрузить .ZIP архив: **Code** -> **Download ZIP**

2. Перейти в загруженную папку в командной строке:

`cd .../<Downloads Folder>/textura-main`

3. Скопировать и вставить в командной строке:

`python -m pip install --upgrade pip && python -m pip install --user virtualenv && python -m venv textura_env && .\textura_env\Scripts\activate && pip install -r requirements.txt && deactivate`

`.\textura_env\Scripts\activate && python run.py && deactivate`

## Использование



## Результат работы

Результат работы – классификация пользовательского текста в одну из групп по выбранной группировке на основе выбранной метрики. 