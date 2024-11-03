# Практическое задание №4. Системы контроля версий

П.Н. Советов, РТУ МИРЭА

Работа с Git.

## Задача 1

На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.

![image](https://github.com/user-attachments/assets/14f5a594-10a1-45a4-91d9-166765fab5c3)

### Решение:

![image](https://github.com/user-attachments/assets/f629b939-5d12-4ae1-ad6a-1c148c209014)


## Задача 2

Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.

Решение:


![image](https://github.com/user-attachments/assets/b09bec9c-8cdb-4e6e-8bcf-d732ad75165c)
![image](https://github.com/user-attachments/assets/750acf87-1923-4204-bc35-c3160b2b9304)
![image](https://github.com/user-attachments/assets/bb06d83e-e83b-439b-991c-2097f68dabd7)


## Задача 3

Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

Пример лога коммитов:

```
*   commit a457d748f0dab75b4c642e964172887de3ef4e3e
|\  Merge: 48ce283 d731ba8
| | Author: Coder 2 <coder2@corp.com>
| | Date:   Sun Oct 11 11:27:09 2020 +0300
| | 
| |     readme fix
| | 
| * commit d731ba84014d603384cc3287a8ea9062dbb92303
| | Author: Coder 1 <coder1@corp.com>
| | Date:   Sun Oct 11 11:22:52 2020 +0300
| | 
| |     coder 1 info
| | 
* | commit 48ce28336e6b3b983cbd6323500af8ec598626f1
|/  Author: Coder 2 <coder2@corp.com>
|   Date:   Sun Oct 11 11:24:00 2020 +0300
|   
|       coder 2 info
| 
* commit ba9dfe9cb24316694808a347e8c36f8383d81bbe
| Author: Coder 2 <coder2@corp.com>
| Date:   Sun Oct 11 11:21:26 2020 +0300
| 
|     docs
| 
* commit 227d84c89e60e09eebbce6c0b94b41004a4541a4
  Author: Coder 1 <coder1@corp.com>
  Date:   Sun Oct 11 11:11:46 2020 +0300
  
      first commit
```

### Решение:

![image](https://github.com/user-attachments/assets/d140aaea-8bd1-4b91-b53a-283595d7b813)
![image](https://github.com/user-attachments/assets/beb7bc07-b72f-4f70-9570-a9195308e007)
![image](https://github.com/user-attachments/assets/d7c62e54-ab3e-4991-97b3-e9ed96571ec9)
![image](https://github.com/user-attachments/assets/4286e60d-0469-46bc-8f41-4f39f039bbb2)
![image](https://github.com/user-attachments/assets/682a951a-822f-4fe0-b6f2-1b4e99fc7c56)
![image](https://github.com/user-attachments/assets/1db3e397-fad2-4dd2-ab7c-9563d2f0d716)


## Задача 4

Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.
