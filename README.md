# Textura

*Инструмент комплексного анализа текста по дескриптивным и предиктивным показателям*

## Запуск

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

#### 1. Ввести путь до файла, например:

`tests/texts/mim.txt`

#### 2. Ввести одну из доступных команд:

`analyse`

`exit`

#### 3. Посмотреть результат:)
