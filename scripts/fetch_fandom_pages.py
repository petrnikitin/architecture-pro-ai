"""
Скрипт для скачивания страниц из Star Wars Fandom
и извлечения чистого текста.
"""

import requests
from bs4 import BeautifulSoup
import time
import os
from pathlib import Path


# Список страниц для скачивания (30+ сущностей)
PAGES = {
    # Главные персонажи
    "characters": [
        "Darth_Vader",
        "Luke_Skywalker",
        "Leia_Organa",
        "Han_Solo",
        "Obi-Wan_Kenobi",
        "Yoda",
        "Emperor_Palpatine",
        "Anakin_Skywalker",
        "Padmé_Amidala",
        "Rey",
        "Kylo_Ren",
        "Chewbacca",
        "R2-D2",
        "C-3PO",
    ],
    # Организации
    "organizations": [
        "Jedi_Order",
        "Sith",
        "Galactic_Empire",
        "Rebel_Alliance",
        "First_Order",
        "Resistance",
    ],
    # Планеты и локации
    "planets": [
        "Tatooine",
        "Coruscant",
        "Hoth",
        "Endor",
        "Naboo",
        "Alderaan",
    ],
    # Технологии и объекты
    "technology": [
        "Death_Star",
        "Lightsaber",
        "Millennium_Falcon",
        "TIE_fighter",
        "X-wing",
        "Star_Destroyer",
    ],
    # Концепции
    "concepts": [
        "The_Force",
        "Hyperspace",
        "Clone_Wars",
    ],
}


def fetch_page(page_name: str, category: str) -> str:
    """
    Скачивает страницу с Wookieepedia (Star Wars Wiki)
    и извлекает текст из основного контента.
    """
    url = f"https://starwars.fandom.com/wiki/{page_name}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Извлекаем основной контент
        content_div = soup.find('div', {'id': 'mw-content-text'})

        if not content_div:
            print(f"⚠️  Не найден контент для {page_name}")
            return ""

        # Удаляем ненужные элементы
        for tag in content_div.find_all(['script', 'style', 'table', 'nav', 'aside']):
            tag.decompose()

        # Извлекаем текст
        paragraphs = content_div.find_all('p')
        text = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

        return text

    except Exception as e:
        print(f"❌ Ошибка при скачивании {page_name}: {e}")
        return ""


def save_raw_pages():
    """
    Скачивает все страницы и сохраняет в knowledge_base/raw/
    """
    base_dir = Path("knowledge_base/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    total = sum(len(pages) for pages in PAGES.values())
    current = 0

    for category, pages in PAGES.items():
        category_dir = base_dir / category
        category_dir.mkdir(exist_ok=True)

        for page_name in pages:
            current += 1
            print(f"[{current}/{total}] Скачиваю {page_name}...")

            text = fetch_page(page_name, category)

            if text:
                file_path = category_dir / f"{page_name}.txt"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {page_name.replace('_', ' ')}\n\n")
                    f.write(text)

                print(f"✅ Сохранено: {file_path}")
            else:
                print(f"⚠️  Пропущено: {page_name}")

            # Задержка, чтобы не перегружать сервер
            time.sleep(1)

    print(f"\n✅ Скачано {current} страниц")


if __name__ == "__main__":
    print("🚀 Начинаю скачивание страниц из Star Wars Fandom...\n")
    save_raw_pages()
    print("\n✅ Готово! Проверьте папку knowledge_base/raw/")
