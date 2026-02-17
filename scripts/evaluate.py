"""
Автоматическое тестирование RAG бота на золотом наборе вопросов
"""
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from src.rag_bot_local import RAGBot
from src.query_logger import QueryLogger


def evaluate_rag_bot():
    """Запуск оценки"""

    print("=" * 80)
    print("🧪 ТЕСТИРОВАНИЕ RAG БОТА")
    print("=" * 80)
    print()

    # Загрузка вопросов
    golden_file = Path("tests/golden_questions.json")
    with open(golden_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    print(f"📋 Загружено вопросов: {len(questions)}")
    print()

    # Инициализация бота
    print("🤖 Загрузка RAG бота...")
    bot = RAGBot(use_simple_mode=False)
    logger = QueryLogger(log_file="logs/evaluation_logs.jsonl")

    # Результаты
    results = []
    correct = 0
    total = 0

    # Тестирование
    for q in questions:
        print(f"\n{'='*80}")
        print(f"❓ Вопрос #{q['id']}: {q['question']}")
        print(f"📚 Категория: {q['category']}")
        print(f"✅ Должен ответить: {'ДА' if q['should_answer'] else 'НЕТ'}")
        print()

        start = datetime.now()
        result = bot.generate_answer(q['question'], top_k=3)
        duration = (datetime.now() - start).total_seconds()

        answer = result['answer']
        sources = result['sources']
        chunks_found = len(sources) > 0

        print(f"💬 Ответ: {answer[:150]}...")
        print(f"📊 Длина ответа: {len(answer)} символов")
        print(f"📄 Источники: {len(sources)}")
        print(f"⏱️  Время: {duration:.2f}s")

        # Оценка корректности
        is_dont_know = answer.strip().lower() in ["я не знаю.", "i don't know.", "я не знаю"]
        is_correct = (q['should_answer'] and not is_dont_know) or (not q['should_answer'] and is_dont_know)

        if is_correct:
            correct += 1
            print("✅ КОРРЕКТНО")
        else:
            print("❌ НЕКОРРЕКТНО")

        total += 1

        # Логирование
        logger.log_query(
            query=q['question'],
            chunks_found=chunks_found,
            num_chunks=len(sources),
            answer=answer,
            sources=sources,
            confidence=result.get('confidence', 0.0),
            duration_sec=duration
        )

        # Сохранение результата
        results.append({
            "question_id": q['id'],
            "question": q['question'],
            "expected_answer": q['expected_answer'],
            "should_answer": q['should_answer'],
            "actual_answer": answer,
            "chunks_found": chunks_found,
            "sources": sources,
            "is_correct": is_correct,
            "duration_sec": duration
        })

    # Финальная статистика
    print()
    print("=" * 80)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print("=" * 80)
    print(f"Всего вопросов: {total}")
    print(f"Корректных ответов: {correct}")
    print(f"Точность: {100 * correct / total:.1f}%")
    print()

    # Анализ по категориям
    by_category = {}
    for r in results:
        cat = next(q['category'] for q in questions if q['id'] == r['question_id'])
        if cat not in by_category:
            by_category[cat] = {"total": 0, "correct": 0}
        by_category[cat]["total"] += 1
        if r["is_correct"]:
            by_category[cat]["correct"] += 1

    print("📈 Результаты по категориям:")
    for cat, stats in by_category.items():
        acc = 100 * stats["correct"] / stats["total"]
        print(f"  {cat}: {stats['correct']}/{stats['total']} ({acc:.0f}%)")

    print()

    # Сохранение результатов
    results_file = Path("logs/evaluation_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_questions": total,
            "correct_answers": correct,
            "accuracy": correct / total,
            "by_category": by_category,
            "results": results
        }, f, indent=2, ensure_ascii=False)

    print(f"💾 Результаты сохранены: {results_file}")
    print("=" * 80)


if __name__ == "__main__":
    evaluate_rag_bot()
