"""
Скрипт для замены всех терминов Star Wars на Cyber Nexus
в скачанных документах.
"""

import json
import re
from pathlib import Path
from typing import Dict


def load_terms_map() -> Dict[str, str]:
    """Загружает словарь замен из terms_map.json"""
    with open('knowledge_base/terms_map.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Объединяем все категории в один плоский словарь
    terms = {}
    for category in data.values():
        if isinstance(category, dict) and not category.get('_comment'):
            terms.update(category)

    # Сортируем по длине (сначала длинные фразы, чтобы не было partial matches)
    terms = dict(sorted(terms.items(), key=lambda x: len(x[0]), reverse=True))

    return terms


def replace_terms_in_text(text: str, terms_map: Dict[str, str]) -> str:
    """
    Заменяет все термины в тексте.
    Использует word boundaries для точного совпадения.
    """
    for original, replacement in terms_map.items():
        # Создаём паттерн с границами слов
        # \b не работает с дефисами, поэтому используем (?<!\w) и (?!\w)
        pattern = r'(?<!\w)' + re.escape(original) + r'(?!\w)'

        # Заменяем, сохраняя регистр первой буквы
        def replace_match(match):
            matched_text = match.group(0)
            if matched_text[0].isupper():
                return replacement
            else:
                return replacement.lower()

        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


def process_all_documents():
    """
    Обрабатывает все документы из raw/ и сохраняет в processed/
    """
    raw_dir = Path('knowledge_base/raw')
    processed_dir = Path('knowledge_base/processed')
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Загружаем словарь замен
    print("📖 Загружаю словарь замен...")
    terms_map = load_terms_map()
    print(f"✅ Загружено {len(terms_map)} терминов для замены\n")

    # Получаем все txt файлы
    txt_files = list(raw_dir.rglob('*.txt'))

    if not txt_files:
        print("⚠️  Не найдено файлов в knowledge_base/raw/")
        print("   Сначала запустите: python scripts/fetch_fandom_pages.py")
        return

    total = len(txt_files)
    print(f"🔄 Обрабатываю {total} документов...\n")

    for i, file_path in enumerate(txt_files, 1):
        # Читаем исходный файл
        with open(file_path, 'r', encoding='utf-8') as f:
            original_text = f.read()

        # Заменяем термины
        processed_text = replace_terms_in_text(original_text, terms_map)

        # Сохраняем в processed/ с той же структурой
        relative_path = file_path.relative_to(raw_dir)
        output_path = processed_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_text)

        print(f"[{i}/{total}] ✅ {relative_path}")

    print(f"\n✅ Обработано {total} документов!")
    print(f"📁 Результаты сохранены в: knowledge_base/processed/")


def verify_replacement():
    """Проверяет, что замены произошли корректно"""
    print("\n🔍 Проверка результатов...")

    processed_dir = Path('knowledge_base/processed')
    terms_map = load_terms_map()

    # Проверяем несколько ключевых терминов
    key_terms = ["Darth Vader", "Luke Skywalker", "Jedi", "Force", "Death Star"]

    found_originals = []

    for file_path in processed_dir.rglob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        for term in key_terms:
            if term in text:
                found_originals.append((file_path.name, term))

    if found_originals:
        print("\n⚠️  ВНИМАНИЕ: Найдены оригинальные термины:")
        for filename, term in found_originals:
            print(f"   - {filename}: '{term}'")
    else:
        print("✅ Все ключевые термины успешно заменены!")


if __name__ == "__main__":
    print("🚀 Начинаю замену терминов Star Wars → Cyber Nexus...\n")
    process_all_documents()
    verify_replacement()
    print("\n✅ Готово! База знаний Cyber Nexus создана.")
