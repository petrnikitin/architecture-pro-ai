@echo off
REM Batch-файл для запуска обновления индекса через Windows Task Scheduler
REM Переходим в директорию проекта
cd /d H:\project\pycharm\architecture-pro-ai

REM Активируем виртуальное окружение
call .venv\Scripts\activate.bat

REM Запускаем скрипт обновления
python scripts\update_index.py

REM Деактивируем окружение
deactivate

REM Пауза для просмотра результатов (можно убрать для cron)
REM pause
