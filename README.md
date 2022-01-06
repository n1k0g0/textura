# Textura

*Инструмент комплексного анализа текста по дескриптивным и предиктивным показателям*

## I. Установка

### Mac/Linux

#### 1. Загрузить .ZIP архив:

**Code** -> **Download ZIP**

#### 2. Открыть загруженную папку в командной строке:

`cd .../<Downloads Folder>/textura-main`

#### 3. Подключить зависимости

```
python3 -m pip install --user --upgrade pip

python3 -m pip install --user virtualenv

python3 -m venv textura_env

source textura_env/bin/activate

pip install -r requirements.txt
```

### Windows

#### 1. Загрузить .ZIP архив:

**Code** -> **Download ZIP**

#### 2. Открыить загруженную папку в командной строке:

`cd ...\<Downloads Folder>\textura-main`

#### 3. Подключить зависимости

```
python -m pip install --upgrade pip

python -m pip install --user virtualenv

python -m venv textura_env

.\textura_env\Scripts\activate

pip install -r requirements.txt
```

## II. Запуск

`python run.py`

Также доступен ввод параметра-пути до анализируемого текста:

`python run.py <path/to/textfile>`

Для получения подсказок необходим параметр `-h`:

`python run.py -h`

## III. Использование

#### 1. Ввести путь до файла, например:

`tests/texts/mim.txt`

#### 2. Ввести команду, доступные команды:

`analyse`

`exit`

## IV. После использования

#### Отключение введенных настроек:

`deactivate`
