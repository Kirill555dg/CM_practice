
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

