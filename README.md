# Примеры автотестов учебного проекта Pokémon Battle

Репозиторий содержит примеры автотестов для веб‑проекта **Pokémon Battle**.  
Тесты демонстрируют работу как с REST API, так и с пользовательским интерфейсом сайта
[pokemonbattle‑stage.ru](https://pokemonbattle-stage.ru/) и выполнены с использованием
фреймворка **pytest**, библиотеки **requests** для HTTP‑запросов, **Selenium WebDriver**
для браузерных тестов, библиотеки **loguru** для логирования и **Allure** для
генерации отчётов.  
Хранение конфиденциальных данных (логин, пароль, токен и ID
тренера) вынесено в отдельный модуль `common/conf.py`.   

## Требования

* **Python 3.10+** – убедитесь, что Python установлен и добавлен в `PATH`.
* **pip** – менеджер пакетов Python.
* **Google Chrome** или другой поддерживаемый браузер. Начиная с Selenium 4.6
  «Selenium Manager» автоматически обнаруживает, скачивает и кэширует нужные
  драйверы, когда они отсутствуют. Это избавляет от
  необходимости вручную загружать `chromedriver`.
* **Действующие учётные данные** для сайта pokemonbattle‑stage.ru и API: адрес
  электронной почты, пароль, идентификатор тренера (`TRAINER_ID`) и токен
  тренера (`TRAINER_TOKEN`). Эти значения необходимо указать в
  файле `common/conf.py`.

## Установка и настройка

1. **Клонирование репозитория**:

   ```bash
   git clone https://github.com/Reliqum/python_autotests.git
   cd python_autotests
   ```

2. **Создание и активация виртуального окружения**:

   ```bash
   python -m venv venv
   # Linux/MacOS
   source venv/bin/activate
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```
   В некоторых версиях PowerShell выполнение скриптов может быть запрещено. В этом
   случае выполнить команду `Set‑ExecutionPolicy Bypass -Scope Process` или
   активировать окружение через `cmd.exe`: `venv\Scripts\activate.bat`.

3. **Установка зависимостей**:

   ```bash
   pip install -r requirements.txt
   ```

   Файл `requirements.txt` содержит библиотеки **pytest**, **requests**,
   **selenium**, **allure‑pytest**, **loguru** и другие, необходимые для запуска
   тестов.  
   После установки рекомендуется убедиться, что `pytest` корректно
   установлен, выполнив `pytest --version`.

4. **Настройка данных для тестов**:

   Открыть файл [`common/conf.py`](common/conf.py) и заменить значения
   по умолчанию в полях `VALID`, `INVALID`, `TRAINER_ID` и `TRAINER_TOKEN` на
   реальные учётные данные. Конфигурационный класс `Cfg` хранит базовые URL
   сайта и API, поэтому при необходимости можно изменить их на другие.

## Запуск тестов

Фреймворк **pytest** автоматически обнаруживает все файлы, начинающиеся на
`test_` или заканчивающиеся на `_test.py`, в текущем каталоге и его
подкаталогах. Запустить тесты можно следующими
командами:

* **Все тесты**:

  ```bash
  pytest -v
  ```

* **Только API‑тесты**:

  ```bash
  pytest -v tests/api
  ```

* **Только Web‑тесты**:

  ```bash
  pytest -v tests/web
  ```


## Генерация отчётов Allure

Для создания наглядных отчётов используется **Allure**. Интеграция с
pytest осуществляется через плагин `allure‑pytest`. Процесс состоит из
двух этапов:

1. **Запуск тестов с указанием директории для результатов**. Передайте
   аргумент `--alluredir=<директория>` при запуске `pytest`, чтобы
   сохранить промежуточные данные отчёта. Например:

   ```bash
   pytest -v --alluredir=allure-results
   ```

2. **Генерация и просмотр HTML‑отчёта**. После того как результаты
   сохранены, преобразовать их в HTML‑отчёт:

   ```bash
   allure generate .\allure_results\
   allure open .\allure-report\
   ```

   Команда `allure generate` создаёт каталог `allure-report` и сохраняет в
   нём HTML‑версию отчёта, а `allure open` открывает отчёт в браузере.

### Пример отчёта Allure

![image](https://raw.githubusercontent.com/Reliqum/python_autotests/main/report.jpg)

## Структура проекта

```
python_autotests/
├── common/
│   └── conf.py             # конфигурация: URL сайта, API и учётные данные
├── tests/
│   ├── api/
│   │   └── test_pokemon_api.py   # тесты REST API
│   └── web/
│       ├── test_pokemon_web.py   # Web‑тесты на Selenium
│       └── conftest.py           # фикстуры для Selenium и сброса покемонов
├── report.jpg                # скриншот отчёта Allure
├── requirements.txt          # список зависимостей
└── README.md                 # документация
```

## Используемые технологии

* **Python** – основной язык программирования.
* **pytest** – фреймворк для тестирования.
* **requests** – библиотека для выполнения HTTP‑запросов.
* **Selenium WebDriver** – инструмент для автоматизации браузера.
* **loguru** – библиотека для удобного и наглядного логирования.
* **allure‑pytest** – инструмент для генерации отчётов;

