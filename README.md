# Создать программу-поисковик
## Цель: 

### В этой самостоятельной работе тренируем умения:
1. Писать "чистый код"
2. Собирать пакеты Чтобы: Применять принципы написания чистого кода и сборку пакетов

## Задача:
Создать программу поисковик (консольную) Пользователь вводит текст запроса, поисковую систему (google.com, yandex.ru, ...), количество результатов, рекурсивный поиск или нет, формат вывода (в консоль, в файл json, в csv) Программа находит в интернете начиная от стартовой точки все ссылки на веб-странице в заданном количестве (название ссылки и саму ссылку) Если поиск не рекурсивный, то берем ссылки только из поисковика, если рекурсивный, то берем первую ссылку, переходим, находим там ссылки, переходим, ... В зависимости от выбранного формата вывода сохраняем результат (текст ссылки: ссылка) либо в консоль либо в файл выбранного формата

0. Создать репозиторий для нового проекта (gitlab, github, ...)

1. Решить задачу
2. Обратить внимание на следующие принципы:

    1. декомпозиция сверху вниз
    2. srp - принцип единственной ответственности
    3. термины предметной области
    4. уменьшение зависимости
    5. чистые функции
    6. цикломатическая сложность
        ```
        python3 -m mccabe --min 5 module.py
        flake8 --max-complexity 5
        ```
    7. понятные названия у переменных, функций, классов, модулей
    8. контекст ближе к коду (привязка к комитам, тикетам, комменты, документация, вики)
    9. разумное использование фишек python
    10. код на английском а не на python
    11. фичеризм - не слишком гибко, не слишком жестко, обобщать когда используется 2 раза
    12. тесты демонстрирующие не очевидное поведение
    13. статический анализ кода pycodestyle, flake8, ast

4. Добавить setup.py для сборки программы в пакет

5. Сдать дз в виде ссылки на репозиторий
## Критерии оценки:
### Задание считается выполненным, когда:
Код запускается без ошибок и программа может получать ссылки по заданному запросу. Есть возможность сборки пакета - 4 баллов

### Дополнительно:
* Проверки flake8 и flake8 --max-complexity 5 не выдают ошибок 1 балл
* Работает рекурсивный поиск 1 балл
* Есть возможность выбора:
    * поисковой системы 1 балл
    * количества результатов 1 балл
    * рекурсивный поиск или нет 1 балл
    * вариант вывода (консоль, json, csv) 1 балл

Итого:4 + 1 + 1 + 1 + 1 + 1 + 1 = 10 баллов
Рекомендуем сдать до: **07.06.2020**

TODO:
- [X] Код запускается без ошибок и программа может получать ссылки по заданному запросу. Есть возможность сборки пакета
- [X] Проверки flake8 и flake8 --max-complexity 5 не выдают ошибок 1 балл
- [X] Работает рекурсивный поиск 1 балл
- [X] поисковой системы 1 балл
- [X] количества результатов 1 балл
- [X] рекурсивный поиск или нет 1 балл
- [X] вариант вывода (консоль, json, csv) 1 балл

