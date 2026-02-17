"""
Тестирование RAG-бота с локальной моделью
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_bot_local import RAGBot


def test_rag_bot():
    """Тестирование RAG-бота"""
    print("=" * 80)
    print("ТЕСТИРОВАНИЕ RAG-БОТА (ЛОКАЛЬНАЯ МОДЕЛЬ)")
    print("=" * 80)

    bot = RAGBot()

    # Тестовые запросы
    test_queries = [
        # Успешные запросы
        "Who is Xarn Velgor?",
        "What is the Synth Flux?",
        "Tell me about the Shadow Order",

        # Запросы вне базы знаний
        "What is the capital of France?",
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
