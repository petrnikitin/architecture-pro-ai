"""
Тестирование поиска по векторному индексу
"""

import sys
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# Конфигурация
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
INDEX_DIR = Path("data/vector_db")
TOP_K = 3  # Количество результатов


def load_index():
    """Загружает FAISS индекс и метаданные"""
    # Загружаем индекс
    index_path = INDEX_DIR / "faiss.index"
    index = faiss.read_index(str(index_path))

    # Загружаем метаданные чанков
    metadata_path = INDEX_DIR / "chunks_metadata.pkl"
    with open(metadata_path, 'rb') as f:
        chunks_metadata = pickle.load(f)

    return index, chunks_metadata


def search(query: str, index: faiss.Index, chunks_metadata: list, model: SentenceTransformer, top_k: int = TOP_K):
    """Выполняет поиск по запросу"""
    # Генерируем эмбеддинг для запроса
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Ищем в FAISS
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        chunk = chunks_metadata[idx]
        results.append({
            'rank': i + 1,
            'distance': float(dist),
            'similarity': 1 / (1 + dist),  # Приблизительная похожесть
            'text': chunk['text'],
            'source': chunk['source'],
            'category': chunk['category'],
            'filename': chunk['filename'],
            'chunk_id': chunk['chunk_id']
        })

    return results


def main():
    """Основная функция"""
    print("🔍 Тестирование поиска по векторному индексу\n")

    # Загружаем индекс и модель
    print("📥 Загружаю индекс и модель...")
    index, chunks_metadata = load_index()
    model = SentenceTransformer(EMBEDDING_MODEL)
    print(f"✅ Загружено. Индекс содержит {index.ntotal} векторов\n")

    # Тестовые запросы
    test_queries = [
        "Who is Xarn Velgor?",
        "What is the Synth Flux?",
        "Tell me about the Void Core"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"{'='*80}")
        print(f"Запрос {i}: {query}")
        print(f"{'='*80}\n")

        results = search(query, index, chunks_metadata, model)

        for result in results:
            print(f"📄 Результат #{result['rank']} (similarity: {result['similarity']:.4f})")
            print(f"   Источник: {result['source']}")
            print(f"   Текст: {result['text'][:200]}...")
            print()

    print("\n✅ Тестирование завершено!")


if __name__ == "__main__":
    main()
