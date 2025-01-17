---
date: 31 марта 2024 года
author: Е.А. Роганов и Д.О. Оберемок
title: Проект «Выпуклая оболочка»
main_version: 2
---

### Постановка задачи

Вычисляется площадь части выпуклой оболочки, 
расположенной внутри заданного стандартного 
замкнутого прямоугольника — прямоугольника 
со сторонами, параллельными осям координат. 
Прямоугольник задаётся двумя его
противоположными вершинами — 
различными точками плоскости.

### Краткий комментарий к решению

- Ключевое понятие проекта: *освещённость ребра из точки* 
- Вспомогательные классы:
    - `R2Point` — точка на плоскости
    - `Deq` — контейнер дек (double ended queue)
- Основные классы:
    - `Figure` — «абстрактная» фигура
    - `Void` — нульугольник
    - `Point` — одноугольник
    - `Segment` — двуугольник
    - `Polygon` — многоугольник
- Файлы проекта:
    - `README.md` — данный файл
    - `r2point.py` — реализация класса `R2Point`
    - `deq.py` — реализация класса `Deq`
    - `convex.py` — реализация основных классов
    - `run_convex.py` — файл запуска
    - `tk_drawer.py` — интерфейс к графической библиотеке
    - `run_tk_convex.py` — файл запуска с использованием графики
    - `tests/test_r2point.py` — тесты к классу `R2Point`
    - `tests/test_convex.py` — тесты к основным классам

Файлы `run_tk_convex.py` и `run_tk_convex.py` являются исполняемыми (они имеют
бит `x`), в первой строке каждого из них используется [шебанг](https://ru.wikipedia.org/wiki/%D0%A8%D0%B5%D0%B1%D0%B0%D0%BD%D0%B3_(Unix)) и команда `env` с
опцией (ключом) `-S`. Это обеспечивает передачу интерпретатору языка Python
опции (ключа) `-B`, отменяющего генерацию `pyc`-файлов в директории
`__pycache__`.

### Соблюдение соглашений о стиле программного кода

Для языка Python существуют [соглашения о стиле
кода](https://www.python.org/dev/peps/pep-0008/). Они являются лишь
рекомендациями (интерпретатор игнорирует их нарушение), но основную их
часть при написании программ целесообразно соблюдать. Существует простой
способ проверить соблюдение считающегося правильным
стиля записи кода с помощью утилиты (программы) `pycodestyle`. Утилита
`yapf` позволяет даже изменить код в соответствии с этими соглашениями.

Команда 

    pycodestyle r2point.py

позволяет, например, проверить соблюдение стиля для файла `r2point.py`.
С помощью очень мощной и часто используемой утилиты `find` проверить
корректность стиля всех файлов проекта можно так:

    find . -name '*.py' -exec pycodestyle {} \;

Эта команда находит все файлы с расширением `py` и запускает программу
`pycodestyle` последовательно для каждого из них.

### Запуск тестов

Команда

    python -B -m unittest discover tests

запускает unit-тесты, выполняя все начинающиеся с `test` методы классов,
имена которых начинаются с `Test`, содержащиеся во всех файлах `test_*.py`
директории `tests`.

Вот как примерно может выглядеть результат запуска этой команды:

~~~
[roganov@aorus convex]$ python -m unittest discover tests
...............................................
----------------------------------------------------------------------
Ran 47 tests in 0.001s

OK
~~~

### Проверка покрытия тестами кода программы

Для языка Python почти стандартом проверки покрытия является библиотека
[`coverage`](https://coverage.readthedocs.io/en/7.3.2/). Вот как можно
её использовать:

~~~
[roganov@aorus convex]$ python -B -m coverage run -m unittest discover tests
................................................
----------------------------------------------------------------------
Ran 48 tests in 0.005s

OK
[roganov@aorus convex]$ python -m coverage report; rm -f .coverage
Name                    Stmts   Miss  Cover
-------------------------------------------
convex.py                  66      0   100%
deq.py                     17      0   100%
r2point.py                 25      0   100%
tests/test_convex.py       87      0   100%
tests/test_r2point.py      55      0   100%
-------------------------------------------
TOTAL                     250      0   100%
~~~


> Вышеприведённая команда выполняет последовательно три действия:
>    - `coverage` запускает тесты;
>    - в случае их успешного завершения печатается отчёт `coverage`;
>    - и удаляется файл `.coverage`

Также можно создать отчёт о тестовом покрытии в формате HTML. Для этого
вместо команды `python -m coverage report` нужно выполнить команду 
`python -m coverage html`. В результате будет создана директория `htmlcov`, 
содержащая подробные HTML-версии отчётов по каждому файлу.

Для просмотра отчёта следует открыть файл `htmlconv/index.html` в браузере.

### Запуск программы

`./run_convex.py`

### Запуск программы с графическим интерфейсом

`./run_tk_convex.py`


### Модификация программы:
В программе требовалось ввести две точки прямоугольника и посчитать точки
выпуклой оболочки внутри него.

Рассматривалось несколько случаев, в частности, случаи, когда все
три точки рассматриваемого треугольника лежат в прямоугольнике;
когда лежат две точки, в таком случае рассматривается количество
пересечений и расположение этих пересечений; то же проверяем с одной точкой
внутри прямоугольника; в конце концов рассматривается случай, когда
ни одна точка не лежит внутри прямоугольника, в таком случае рассматривается
количество пересечений и расположение этих пересечений.

Решение является индуктивным, так как для нахождения площади выпуклой
оболочки требуется знать лишь новую точку, площадь предыдущей
выпуклой оболочки и точки, которые освещены из только что введённой точки.
