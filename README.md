# Textura

Textura -- инструмент комплексного анализа текста по дескриптивным и предиктивным показателям

### Установка

#### Mac/Linux

1. Загрузить .ZIP архив:

(**Code** -> **ZIP**)

2. Открыить загруженную папку в командной строке:

`cd .../<Downloads Folder>/textura-main`

3. Подключить зависимости

`python3 -m pip install --user --upgrade pip`

`python3 -m pip install --user virtualenv`

`python3 -m venv textura_env`

`source textura_env/bin/activate`

`pip install -r requirements.txt`

#### Windows

1. Загрузить .ZIP архив:

(**Code** -> **ZIP**)

2. Открыить загруженную папку в командной строке:

`cd ...\<Downloads Folder>\textura-main`

3. Подключить зависимости

`py -m pip install --upgrade pip`

`py -m pip install --user virtualenv`

`py -m venv textura_env`

`.\textura_env\Scripts\activate`

`pip install -r requirements.txt`

### Запуск

`python run.py`

Также доступен ввод параметра-пути до анализируемого текста:

`python run.py <path/to/textfile>`

### После использования

Отключение введенных настроек:

`deactivate`
