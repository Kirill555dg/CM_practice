
## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

Решение:
```
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
```
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
```
![image](https://github.com/user-attachments/assets/8cff1223-52e6-4075-9392-d40807e7fe57)

