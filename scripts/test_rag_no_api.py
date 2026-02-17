"""
Тестирование RAG-бота без API (только векторный поиск)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_bot import RAGBot
import os

# Временно отключаем инициализацию OpenAI
class MockRAGBot(RAGBot):
    def __init__(self, index_dir: str = "data/vector_db"):
        """Инициализация без OpenAI"""
        from pathlib import Path
        import faiss
        import pickle
        from sentence_transformers import SentenceTransformer

        self.index_dir = Path(index_dir)

        print("📥 Загрузка векторного индекса...")
        self.index = faiss.read_index(str(self.index_dir / "faiss.index"))

        with open(self.index_dir / "chunks_metadata.pkl", "rb") as f:
            self.chunks = pickle.load(f)

        print("🔧 Загрузка модели эмбеддингов...")
        self.embedder = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )

        print("✅ RAG-бот готов (без OpenAI API)!\n")

    def generate_answer(self, query: str, top_k: int = 3) -> dict:
        """Только поиск, без генерации"""
        contexts = self.search(query, top_k)

        # Mock ответ
        if contexts:
            answer = f"[MOCK] Найдено {len(contexts)} релевантных документов.\n"
            answer += f"Лучший результат: {contexts[0]['source']}\n"
            answer += f"Similarity: {contexts[0]['similarity']:.3f}"
        else:
            answer = "[MOCK] I don't know - no relevant documents found."

        return {
            "query": query,
            "answer": answer,
            "contexts": contexts,
            "sources": [ctx['source'] for ctx in contexts]
        }


def test_rag_bot():
    """Тестирование RAG-бота"""
    print("=" * 80)
    print("ТЕСТИРОВАНИЕ RAG-БОТА (БЕЗ OPENAI API)")
    print("=" * 80)

    bot = MockRAGBot()

    test_queries = [
        # Успешные запросы
        "Who is Xarn Velgor?",
        "What is the Synth Flux?",
        "Tell me about the Shadow Order",
        "What technology does Cypher-9 have?",
        "Describe planet Tal'vora",

        # Запросы вне базы
        "What is the capital of France?",
        "Who is Harry Potter?",
    ]

    results = []

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 80}")
        print(f"ТЕСТ {i}/{len(test_queries)}")
        print(f"{'=' * 80}")
        print(f"❓ Вопрос: {query}\n")

        result = bot.generate_answer(query, top_k=3)

        print(f"📄 Источники: {', '.join(result['sources']) if result['sources'] else 'Нет'}")
        print(f"\n{result['answer']}\n")

        results.append({
            "query": query,
            "has_sources": len(result['sources']) > 0,
            "answer_length": len(result['answer'])
        })

    # Статистика
    print("\n" + "=" * 80)
    print("СТАТИСТИКА")
    print("=" * 80)

    successful = sum(1 for r in results if r['has_sources'])
    no_info = len(results) - successful

    print(f"\n✅ Успешных ответов (с источниками): {successful}")
    print(f"❌ Ответов 'не знаю' (без источников): {no_info}")
    print(f"\n📊 Всего запросов: {len(results)}")


if __name__ == "__main__":
    test_rag_bot()
