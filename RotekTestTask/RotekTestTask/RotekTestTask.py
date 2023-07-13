# Чтение данных из файла /proc/meminfo
with open('/proc/meminfo', 'r') as file:
    data = file.readlines()

# Запись оригинального файла в meminfo.txt для проверки результата
with open('meminfo.txt', 'w') as file:
    file.writelines(data)

# Замена нулевых значений на "-"
cleaned_data = []
for line in data:
    parts = line.split()    # Замена отдельно стоящих "0"
    if len(parts) > 1 and parts[1] == '0':
        line = f'{parts[0]} -'

    line = line.strip()     # Замена "0 kB"
    if 'kB' in line:
        key, value = line.split(':')
        value = value.strip()
        value = '-' if value == '0 kB' or value == '0' else value
        line = f'{key}: {value}'

    cleaned_data.append(line)

# Функция для получения значения памяти
def get_memory_value(line):
    try:
        value = line.split(':')[1].strip()
        if value.endswith('kB'):
            value = value[:-2].strip()
        return int(value)
    except (ValueError, IndexError):
        return 0

# Сортировка строк по объему памяти
sorted_data = sorted(cleaned_data, key=get_memory_value)

# Удаление всех символов ":" из строк
sorted_data = [line.replace(':', '') for line in sorted_data]

# Запись результатов в новый файл
with open('sorted_meminfo.txt', 'w') as file:
    file.write('\n'.join(sorted_data))
