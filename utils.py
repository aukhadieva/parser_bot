import os


# Путь к директории, в которой находится текущий скрипт
script_directory = os.path.dirname(os.path.abspath(__file__))

# Полный путь к файлу базы данных 'zyzybliki.db'
db_path = os.path.join(script_directory, 'zyzybliki.db')

# Полный путь к файлу Exel
xlsx_path = os.path.join(script_directory, 'data.xlsx')
