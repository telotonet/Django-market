'''
1. Создай главную папку и положи в нее одну папку с фул этим проектом.
2. Зайди в эту главную папку через консоль  и пропиши python -m venv venv, 
эта команда установит виртуальное окружение в папке, смежной с папкой в которой весь проект
3. затем выбери в визуал коде venv/Scripts/python.exe как интерпретатор.
4. перезапусти консоль, у тебя автоматически вставится команда в консоль которая запустит venv. Если не запустится, то надо прописать полный путь от диска C прям до файла activate.ps1 в той же папке venv/Scripts
5. после запуска venv, пиши в консоли pip install django
6. pip install pillow

7. Чтобы запустить проект, в консоли перейди в папку в которой хранится manage.py

например консоль говорит что ты сейчас в magaz/ , а тебе надо в magaz/market =>
cd market
python manage.py runserver


'''


'''НИЖЕ ПО ХОДУ СОЗДАНИЯ ПРОЕКТА БУДУТ ОБНОВЛЯТЬСЯ БИБЛИОТЕКИ, КОТОРЫЕ НАДО ДОУСТАНОВИТЬ'''


"""
1. pip install django
2. pip install pillow
3. pip install stripe

"""


'ПУБЛИЧНЫЙ КЛЮЧ СТРАЙП'
"pk_test_51JOQm5Faw5MMBhhd20AkSufrvwbK47nk4WW3k489cWeAkKT5o42dqLdBa4YB7wltQio3RNDRznxvtBMaxT56g4Kd00eQX4tznK"

'СЕКРЕТНЫЙ КЛЮЧ СТРАЙП'
"sk_test_51JOQm5Faw5MMBhhdWTgtpl7aQMmxYoKGBfkK55Im9ePD7a0iL73SIEOmG80ghCP8Bb68273CRcvx6LdKlSMh1v2u00mjfLJdUG"