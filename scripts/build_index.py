"""
Создание векторного индекса для базы знаний Cyber Nexus
Использует: sentence-transformers + FAISS
"""

import sys
import json
import pickle
from pathlib import Path
from datetime import datetime
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# Конфигурация
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
CHUNK_SIZE = 1000  # символов
CHUNK_OVERLAP = 200  # символов
KNOWLEDGE_BASE_DIR = Path("knowledge_base/processed")
OUTPUT_DIR = Path("data/vector_db")


def load_documents() -> List[Dict]:
    """Загружает все markdown документы из базы знаний"""
    documents = []

    for md_file in KNOWLEDGE_BASE_DIR.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Извлекаем категорию и имя файла
        category = md_file.parent.name
        filename = md_file.stem

        documents.append({
            'content': content,
            'source': str(md_file.relative_to(KNOWLEDGE_BASE_DIR)),
            'category': category,
            'filename': filename,
            'full_path': str(md_file)
        })

    return documents


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    """Разбивает документы на чанки"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []
    chunk_id = 0

    for doc in documents:
        text_chunks = text_splitter.split_text(doc['content'])

        for i, chunk_text in enumerate(text_chunks):
            chunks.append({
                'chunk_id': chunk_id,
                'text': chunk_text,
                'source': doc['source'],
                'category': doc['category'],
                'filename': doc['filename'],
                'chunk_index': i,
                'total_chunks': len(text_chunks)
            })
            chunk_id += 1

    return chunks


def generate_embeddings(chunks: List[Dict], model_name: str) -> np.ndarray:
    """Генерирует эмбеддинги для всех чанков"""
    print(f"📥 Загружаю модель {model_name}...")
    model = SentenceTransformer(model_name)

    texts = [chunk['text'] for chunk in chunks]

    print(f"🔄 Генерирую эмбеддинги для {len(texts)} чанков...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings


def create_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """Создаёт FAISS индекс"""
    dimension = embeddings.shape[1]

    # Используем IndexFlatL2 (простой, точный поиск по L2 distance)
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index


def save_index(index: faiss.Index, chunks: List[Dict], metadata: Dict):
    """Сохраняет индекс и метаданные"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Сохраняем FAISS индекс
    faiss_path = OUTPUT_DIR / "faiss.index"
    faiss.write_index(index, str(faiss_path))
    print(f"✅ FAISS индекс сохранён: {faiss_path}")

    # Сохраняем метаданные чанков
    chunks_path = OUTPUT_DIR / "chunks_metadata.pkl"
    with open(chunks_path, 'wb') as f:
        pickle.dump(chunks, f)
    print(f"✅ Метаданные чанков сохранены: {chunks_path}")

    # Сохраняем общую информацию
    info_path = OUTPUT_DIR / "index_info.json"
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"✅ Информация об индексе сохранена: {info_path}")


def main():
    """Основная функция"""
    start_time = datetime.now()

    print("🚀 Начинаю создание векторного индекса...\n")

    # 1. Загрузка документов
    print("📚 Загружаю документы...")
    documents = load_documents()
    print(f"✅ Загружено {len(documents)} документов\n")

    # 2. Chunking
    print("✂️  Разбиваю на чанки...")
    chunks = chunk_documents(documents)
    print(f"✅ Создано {len(chunks)} чанков\n")

    # 3. Генерация эмбеддингов
    embeddings = generate_embeddings(chunks, EMBEDDING_MODEL)
    print(f"✅ Эмбеддинги сгенерированы: {embeddings.shape}\n")

    # 4. Создание FAISS индекса
    print("🔨 Создаю FAISS индекс...")
    index = create_faiss_index(embeddings)
    print(f"✅ FAISS индекс создан: {index.ntotal} векторов\n")

    # 5. Сохранение
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    metadata = {
        'model': EMBEDDING_MODEL,
        'embedding_dimension': int(embeddings.shape[1]),
        'total_documents': len(documents),
        'total_chunks': len(chunks),
        'chunk_size': CHUNK_SIZE,
        'chunk_overlap': CHUNK_OVERLAP,
        'created_at': start_time.isoformat(),
        'duration_seconds': duration,
        'index_type': 'IndexFlatL2'
    }

    print("💾 Сохраняю индекс...")
    save_index(index, chunks, metadata)

    print(f"\n✅ Готово! Время: {duration:.2f} сек")
    print(f"\n📊 Статистика:")
    print(f"   Документов: {len(documents)}")
    print(f"   Чанков: {len(chunks)}")
    print(f"   Размерность эмбеддингов: {embeddings.shape[1]}")
    print(f"   Размер индекса: {index.ntotal} векторов")


if __name__ == "__main__":
    main()
