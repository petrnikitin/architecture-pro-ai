"""
Тестирование RAG-бота с примерами диалогов
"""
import sys
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_bot import RAGBot


def test_rag_bot():
    """Тестирование RAG-бота"""
    print("=" * 80)
    print("ТЕСТИРОВАНИЕ RAG-БОТА")
    print("=" * 80)

    bot = RAGBot()

    # Тестовые запросы
    test_queries = [
        # Успешные запросы (должны найти ответы)
        "Who is Xarn Velgor?",
        "What is the Synth Flux?",
        "Tell me about the Shadow Order",
        "What technology does Cypher-9 have?",
        "Describe planet Tal'vora",

        # Запросы вне базы знаний (должны ответить "не знаю")
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
