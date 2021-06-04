from math import log2, sqrt
import matplotlib.pyplot as plt

# Вариант 5: 6 97 82 16 62 16 1 25 1 56 32 84 96 36 81 97 18 71 91 35 71 13 8 81 87
inp = input('Введите числа через пробел: ')
a = list(map(int, inp.split()))
a = sorted(a)
n = len(a)
print(f'Количество чисел: {n}')
print(f'Ранжированные числа: {a}')
xmax = max(a)
xmin = min(a)
print(f'Максимальное: {xmax} Минимальное: {xmin}')
h = round((xmax - xmin) / (1 + log2(n)))
print(f'H = {h}')
startx = xmin - (1 / 2 * h)

print(f'Начальное X: {startx}')

current = startx
interval = []
table = {
    0: {},
    1: {},
    2: {}
}
# Первая строка таблицы
while current < xmax:
    interval.append({'start': current, 'end': current + h})
    current += h

table[0] = interval

# Вторая строка таблицы
string2 = []
for i in range(len(table[0])):
    count = 0
    for num in a:
        if i != len(table[0]) - 1:
            if (num >= table[0][i]['start']) and (num < table[0][i]['end']):
                count += 1
        else:
            if (num >= table[0][i]['start']) and (num <= table[0][i]['end']):
                # Если последний столбик, то последнее число тоже включаем [;]
                count += 1
    string2.append(count)

table[1] = string2

# Третья строка таблицы
sigma = sum(table[1])
print(f'Сумма {sigma}')
string3 = []
for i in range(len(table[1])):
    string3.append(f'{table[1][i]}/{sigma}')
table[2] = string3

print('#' * 16 + ' Интервальный статистический ряд ' + '#' * 16)

string1 = []
for i in range(len(table[0])):
    string1.append('[' + str(table[0][i]['start']) + ';' + str(table[0][i]['end']) + ')')

print(*string1)
print(*string2)
print(*string3)

table2 = {
    0: {},
    1: {},
    2: {}
}

t2string1 = []
for i in range(len(table[0])):
    t2string1.append(int(((table[0][i]['start'] + table[0][i]['end']) / 2)))

table2[0] = t2string1
print('#' * 16 + ' Интервальный статистический ряд 2 ' + '#' * 16)
print(*t2string1)
table2[1] = table[2]
print(*table2[1])
table2[2] = table[1]
print(*table2[2])


def polygon_particulars(xi, ni):
    plt.plot(xi, ni)
    plt.xlabel('Xi')
    plt.ylabel('ni')
    plt.title('Полигон частоты')
    plt.show()


def histogram_particulars(xi, pi):
    plt.bar(xi, pi)
    plt.xlabel('Xi')
    plt.ylabel('Pi')
    plt.plot(xi, pi, color='red')
    plt.title('Гистограмма частностей')
    plt.show()


def func_empirical(xn, fx):
    plt.step(xn, fx)
    plt.xlabel('X')
    plt.ylabel('F*(x)')
    plt.title('Эмпирическая функция')
    plt.show()


allxi = []
allxi2 = []
allni = table2[2]
allpi = [i / sigma for i in allni]
for i in range(len(table[0])):
    # allxi.append(table[0][i]['start'])
    # allxi2.append(str(table[0][i]['start']) + '-' + str(table[0][i]['end']))
    allxi.append(str(table[0][i]['start']))

polygon_particulars(table2[0], allni)
histogram_particulars(allxi, allpi)
print('#' * 16 + 'Эмпирическая функция' + '#' * 16)
empirical = {}
for i in range(len(table2[0]) + 1):
    if i == 0:
        f = round(i / sigma, 2)
        print(f'{f} при x <= {table2[0][i]}')
        empirical[table2[0][i]] = f
    elif i == len(table2[0]):
        f = round(sum(table2[2][:i]) / sigma, 2)
        print(f'{f} при x > {table2[0][i-1]}')
        empirical[table2[0][i-1]] = f
    else:
        f = round(sum(table2[2][:i]) / sigma, 2)
        print(f'{f} при {table2[0][i-1]} < x <= {table2[0][i]}')
        empirical[table2[0][i]] = f

func_empirical(empirical.keys(), empirical.values())
print()
# Среднее выборочное
avgx = 0
for i in range(len(table2[0])):
    avgx += table2[0][i] * allni[i]

avgx /= sigma
# avgx = round(avgx,1)
print(f'Среднее выборочное: {avgx}')

# Выборочная дисперсия
avgd = 0
for i in range(len(table2[0])):
    avgd += (table2[0][i] ** 2) * table2[2][i]
avgd /= n
avgd -= avgx**2
avgd = round(avgd, 2)
print(f'Выборочная дисперсия: {avgd}')

# Среднее квадротическое отклонение
avgdev = round(sqrt(avgd), 2)
print(f'Среднее квадротическое отклонение: {avgdev}')

# Исправленная выборочная дисперсия
fixavgd = round((n / (n - 1)) * avgd, 2)
print(f'Исправленная выборочная дисперсия: {fixavgd}')

# Исправленное среднее квадротическое отклонение
fixavgdev = round(sqrt(fixavgd), 2)
print(f'Исправленное среднее квадротическое отклонение: {fixavgdev}')

# Размах выборки
samplesize = xmax - xmin
print(f'Размах выборки: {samplesize}')


# Медиана

def median(sample):
    size = len(sample)
    index = size // 2

    if size % 2:
        return sample[index]
    else:
        return sum(sorted(sample[index - 1:index + 1])) / 2


median = median(a)
print(f'Медиана: {median}')

# Мода
modaindex = table2[2].index(max(table2[2]))
# moda = '[' + str(table[0][modaindex]['start']) + ';' + str(table[0][modaindex]['end']) + ')'
moda = table2[0][modaindex]

print(f'Мода: {moda}')

# Объем
samplevolume = n
print(f'Объем: {samplevolume}')
