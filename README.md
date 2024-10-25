# Snake
Это классическая игра "Змейка", выполненная с использованием библиотеки *Pygame* и принципов объектно-ориентированного программирования (ООП). В игре игрок управляет змейкой, цель которой — собирать еду, увеличиваясь в длину, при этом избегая столкновений с собственным телом.

## Стек технологий
- **Python** — основной язык программирования проекта
- **Pygame** — библиотека для создания игр, использована для реализации графики и игровой логики
- **ООП** — все ключевые элементы игры, такие как змейка и еда, реализованы как объекты, что обеспечивает чистую и масштабируемую архитектуру проекта

## Правила игры
- Змейка состоит из сегментов
- Змейка движется в одном из четырёх направлений — вверх, вниз, влево или вправо. Игрок управляет направлением движения, но змейка не может остановиться или двигаться назад
- Каждый раз, когда змейка съедает яблоко, она увеличивается в длину на один сегмент
- В классической версии игры столкновение змейки с границей игрового поля приводит к проигрышу. Однако в этой вариации змейка может проходить сквозь стену и появляться с противоположной стороны поля
- Если змейка столкнётся сама с собой — игра начинается с начала

## Как запустить проект

* Клонировать репозиторий и перейти в него в командной строке
```
git clone https://github.com/ovienrait/Snake/
```
```
cd Snake
```
* В корневой директории проекта создайте виртуальное окружение

для Windows
```
python -m venv venv
```
для Linux/MacOS
```
python3 -m venv venv
```
* Активируйте виртуальное окружение, находясь в корневой директории

для Windows
```
source venv/Scripts/activate
```
для Linux/MacOS
```
source venv/bin/activate
```
* Обновите пакетный менеджер, находясь в корневой директории

для Windows
```
python -m pip install --upgrade pip
```
для Linux/MacOS
```
python3 -m pip install --upgrade pip
```
* Установите зависимости проекта, находясь в корневой директории
```
pip install -r requirements.txt
```
* Запустить проект

для Windows
```
python the_snake.py
```
для Linux/MacOS
```
python3 the_snake.py
```
