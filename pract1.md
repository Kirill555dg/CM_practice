
## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

Решение:
```bash
grep -o '^[^:]*' /etc/passwd | sort
```
![image](https://github.com/user-attachments/assets/afaf371f-97b3-48a6-8cc5-f3977dd0c26d)


## Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:

```
[root@localhost etc]# cat /etc/protocols ...
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```

Решение:
```bash
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
```
![image](https://github.com/user-attachments/assets/8cff1223-52e6-4075-9392-d40807e7fe57)

## Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

```
[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

Перед отправкой решения проверьте его в ShellCheck на предупреждения.

Решение:
```bash
#!/bin/bash
text=$1
size=${#text}
echo -n "+"
for ((i = -2; i < size; i++))
do
echo -n "-"
done
echo "+"
echo "| $text |"
echo -n "+"
for ((i = -2; i < size; i++))
do
echo -n "-"
done
echo "+"
```
![image](https://github.com/user-attachments/assets/e9f16f9e-1db4-4f13-b656-e5b7165aef78)


## Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Пример для hello.c:

```
h hello include int main n printf return stdio void world
```

Решение:
```bash
grep -o '\b[_A-Za-z][_A-Za-z0-9]*\b' hello.cpp | sort | uniq
```
![image](https://github.com/user-attachments/assets/7944c18e-b95c-4060-9bc5-e8cdd2149b59)

## Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Например, пусть программа называется reg:

```
./reg banner
```

В результате для banner задаются правильные права доступа и сам banner копируется в /usr/local/bin.

Решение:
```bash
#!/bin/bash

chmod 755 "$1"
sudo cp "$1" /usr/local/bin/

```
![image](https://github.com/user-attachments/assets/9a0badb0-4b36-40fd-940c-c9df3eeeed2e)


## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

Решение:
```bash
for file in "$@"; do
  if [[ "$file" =~ \.(c|js|py)$ ]]; then
    first_line=$(head -n 1 "$file")
    if [[ "$first_line" =~ ^\/[*\/]{1}|#|\'{3} ]]; then
  echo "$file has a comment in the first line."
    else
      echo "$file doesn't have a comment in the first line."
    fi
  fi
done
```
![image](https://github.com/user-attachments/assets/e49f5d31-81df-46b7-b417-781938001dd0)


## Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).

Решение: 
```bash
find "$1" -type f -exec md5sum {} + | sort | uniq -w32 -dD
```
![image](https://github.com/user-attachments/assets/65dc855f-0ef5-4d99-820c-0489ddfecd45)


## Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

Решение: 
```bash
find . -name "*.$1" -print0 | tar -czvf archive.tar.gz --null -T -
```
![image](https://github.com/user-attachments/assets/646c844d-bfcc-4305-a4e3-344f9a8e6afe)


## Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

Решение:
```bash
sed 's/    /\t/g' "$1" > "$2"
```
![image](https://github.com/user-attachments/assets/9445eb86-6264-4149-bba7-9542bed600a2)

## Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром. 

Решение:
```bash
find "$1" -type f -empty -name "*.txt"
```
![image](https://github.com/user-attachments/assets/1ae2294d-b4aa-4b99-8bba-20f0053ef2e9)
