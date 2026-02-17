# Векторный индекс Cyber Nexus

## Описание

Векторный индекс для базы знаний Cyber Nexus, созданный с использованием FAISS и sentence-transformers.

## Файлы

- `faiss.index` - FAISS индекс с векторами (65 чанков)
- `chunks_metadata.pkl` - Метаданные чанков (source, category, text)
- `index_info.json` - Информация об индексе

## Характеристики

**Embedding модель:** sentence-transformers/paraphrase-multilingual-mpnet-base-v2
- Размерность: 768
- Поддержка языков: Мультиязычная (50+ языков)
- Репозиторий: https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2

**База знаний:**
- Документов: 33
- Чанков: 65
- Chunk size: 1000 символов
- Chunk overlap: 200 символов

**Векторная БД:** FAISS
- Тип индекса: IndexFlatL2 (точный поиск по L2 distance)
- Векторов в индексе: 65
- Размер на диске: ~200KB

**Время генерации:** 146.65 сек (~2.5 минуты)

## Использование

### Загрузка индекса

```python
import faiss
import pickle

# Загрузить FAISS индекс
index = faiss.read_index("data/vector_db/faiss.index")

# Загрузить метаданные
with open("data/vector_db/chunks_metadata.pkl", "rb") as f:
    chunks_metadata = pickle.load(f)
```

### Поиск

```python
from sentence_transformers import SentenceTransformer

# Загрузить модель
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# Сгенерировать эмбеддинг для запроса
query = "Who is Xarn Velgor?"
query_embedding = model.encode([query])

# Поиск в FAISS
distances, indices = index.search(query_embedding, k=3)

# Получить результаты
for idx in indices[0]:
    chunk = chunks_metadata[idx]
    print(chunk['text'])
```

### Тестирование

```bash
python scripts/test_search.py
```

## Примеры запросов

**Запрос 1:** "Who is Xarn Velgor?"
- ✅ Найден документ: `characters/Xarn_Velgor.md`
- Similarity: 0.2198

**Запрос 2:** "What is the Synth Flux?"
- ✅ Найден документ: `technology/Synth_Flux.md`
- Similarity: 0.2396

**Запрос 3:** "Tell me about the Void Core"
- ✅ Найден документ: `technology/Void_Core.md`
- Similarity: 0.2203

## Структура метаданных чанка

```json
{
  "chunk_id": 0,
  "text": "...",
  "source": "characters/Xarn_Velgor.md",
  "category": "characters",
  "filename": "Xarn_Velgor",
  "chunk_index": 0,
  "total_chunks": 2
}
```

## Пересоздание индекса

```bash
python scripts/build_index.py
```

Время выполнения: ~2-3 минуты на CPU
