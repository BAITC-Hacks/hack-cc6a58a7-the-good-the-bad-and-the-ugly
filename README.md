# Есть дефект или нет

Небольшое решение задания по компьютерному зрению. Скрипт получает путь к
изображению и печатает ровно `OK` или `DEFECT`.

По условию кейса используется простое объяснимое правило: если красные пиксели
занимают не меньше 20% изображения, результат — `DEFECT`, иначе — `OK`.

## Быстрый запуск

Нужен Python 3.10 или новее.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Если виртуальное окружение уже настроено, достаточно установить зависимости:

```powershell
python -m pip install -r requirements.txt
```

Примеры изображений уже находятся в папке `images`. При необходимости их можно
пересоздать:

```powershell
python generate_samples.py
```

Запуск классификации:

```powershell
python defect_detector.py images/ok.png
# OK

python defect_detector.py images/defect.png
# DEFECT
```

Для проверки расчётной доли красного можно добавить `--show-ratio`:

```powershell
python defect_detector.py images/defect.png --show-ratio
# DEFECT (red_ratio=0.663)
```

Для дополнительной проверки можно создать набор тестовых изображений и
прогнать их все:

```powershell
python generate_test_cases.py
Get-ChildItem images/test_cases/*.png | ForEach-Object {
    python defect_detector.py $_.FullName --show-ratio
}
```

В наборе есть изображения с 0%, 15%, ровно 20%, 25% и 77% красного. Ровно
20% уже считается дефектом, потому что проверка использует `>= 0.20`.

Скрипт принимает обычные растровые форматы, которые поддерживает Pillow,
включая PNG и JPEG.

## Как работает алгоритм

1. Изображение переводится в RGB.
2. Красным считается пиксель, у которого `R >= 120`, а красный канал минимум
   в 1.2 раза сильнее зелёного и синего.
3. Доля красных пикселей сравнивается с порогом `0.20`.

Пороговые значения можно изменить параметрами `--red-min`, `--dominance` и
`--defect-ratio`. ML-модель для этого учебного кейса не требуется.

## Тесты

```powershell
python -m unittest discover -s tests -v
```

Тесты проверяют зелёное изображение, красное изображение, небольшую красную
область, пользовательский порог и формат вывода CLI.

## Структура проекта

```text
defect-detector/
├── defect_detector.py       # CLI и алгоритм классификации
├── generate_samples.py      # генератор demo-изображений
├── generate_test_cases.py   # генератор дополнительных тестов
├── requirements.txt         # Pillow
├── images/
│   ├── ok.png
│   ├── defect.png
│   └── test_cases/
└── tests/
    └── test_detector.py
```
