import os
import sys

# Укажите полный путь к папке проекта
PROJECT_PATH = 'C:/Users/User/PycharmProjects/drf_project'  # для Windows
# PROJECT_PATH = '/home/user/PycharmProjects/drf_project'  # для Linux/macOS


if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()