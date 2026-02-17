"""
Просмотр содержимого векторного индекса
"""

import sys
import pickle
import json
from pathlib import Path

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def view_chunks_metadata():
    """Показывает метаданные чанков"""
    print("=" * 80)
    print("CHUNKS METADATA (chunks_metadata.pkl)")
    print("=" * 80)

    # Загружаем pickle файл
    with open('data/vector_db/chunks_metadata.pkl', 'rb') as f:
        chunks = pickle.load(f)

    print(f"\nВсего чанков: {len(chunks)}")
    print(f"Тип данных: {type(chunks)}")
    print(f"\nПример первого чанка:")
    print("-" * 80)

    first_chunk = chunks[0]
    print(f"Chunk ID: {first_chunk['chunk_id']}")
    print(f"Source: {first_chunk['source']}")
    print(f"Category: {first_chunk['category']}")
    print(f"Filename: {first_chunk['filename']}")
    print(f"Chunk Index: {first_chunk['chunk_index']} / {first_chunk['total_chunks']}")
    print(f"\nТекст (первые 200 символов):")
    print(first_chunk['text'][:200] + "...")

    print("\n" + "-" * 80)
    print("Статистика по категориям:")

    categories = {}
    for chunk in chunks:
        cat = chunk['category']
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} чанков")


def view_index_info():
    """Показывает информацию об индексе"""
    print("\n" + "=" * 80)
    print("INDEX INFO (index_info.json)")
    print("=" * 80)

    with open('data/vector_db/index_info.json', 'r', encoding='utf-8') as f:
        info = json.load(f)

    print(f"\nМодель эмбеддингов: {info['model']}")
    print(f"Размерность векторов: {info['embedding_dimension']}")
    print(f"Всего документов: {info['total_documents']}")
    print(f"Всего чанков: {info['total_chunks']}")
    print(f"Chunk size: {info['chunk_size']} символов")
    print(f"Chunk overlap: {info['chunk_overlap']} символов")
    print(f"Тип индекса: {info['index_type']}")
    print(f"Создан: {info['created_at']}")
    print(f"Время генерации: {info['duration_seconds']:.2f} секунд")


def view_faiss_index():
    """Показывает информацию о FAISS индексе"""
    import faiss
    import numpy as np

    print("\n" + "=" * 80)
    print("FAISS INDEX (faiss.index)")
    print("=" * 80)

    # Загружаем FAISS индекс
    index = faiss.read_index('data/vector_db/faiss.index')

    print(f"\nТип индекса: {type(index).__name__}")
    print(f"Количество векторов: {index.ntotal}")
    print(f"Размерность векторов: {index.d}")
    print(f"Обучен: {index.is_trained}")

    # Показываем первый вектор (частично)
    print(f"\nПример вектора #0 (первые 10 значений):")
    # Реконструируем вектор из индекса
    vector = faiss.rev_swig_ptr(index.get_xb(), index.ntotal * index.d)
    vector = np.copy(vector).reshape(index.ntotal, index.d)

    print(vector[0][:10])
    print(f"Диапазон значений: [{vector[0].min():.4f}, {vector[0].max():.4f}]")
    print(f"Средне значение: {vector[0].mean():.4f}")


def main():
    """Главная функция"""
    print("\n🔍 ПРОСМОТР ВЕКТОРНОГО ИНДЕКСА\n")

    # 1. Метаданные чанков
    view_chunks_metadata()

    # 2. Общая информация
    view_index_info()

    # 3. FAISS индекс
    view_faiss_index()

    print("\n" + "=" * 80)
    print("✅ Готово!")
    print("=" * 80)


if __name__ == "__main__":
    main()
