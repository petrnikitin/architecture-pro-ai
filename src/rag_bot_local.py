"""
RAG-бот для базы знаний Cyber Nexus с ЛОКАЛЬНОЙ моделью
Использует FAISS для поиска + HuggingFace transformers для генерации + Few-shot + Chain-of-Thought
"""
import os
import sys
import pickle
import warnings
import logging
from pathlib import Path
from typing import List, Dict
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoConfig
from transformers.generation.streamers import TextStreamer
import torch

# Отключаем проблемные warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*flash-attention.*")
warnings.filterwarnings("ignore", message=".*symlinks.*")

# Отключаем WARNING логи от transformers
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("transformers_modules").setLevel(logging.ERROR)

# Fix Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class ProgressCallback:
    """Callback для отображения прогресса генерации"""
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.current_token = 0
        self.start_time = None

    def __call__(self, input_ids, scores, **kwargs):
        if self.start_time is None:
            self.start_time = __import__('time').time()

        self.current_token += 1
        elapsed = __import__('time').time() - self.start_time
        tokens_per_sec = self.current_token / elapsed if elapsed > 0 else 0
        remaining_tokens = self.max_tokens - self.current_token
        eta = remaining_tokens / tokens_per_sec if tokens_per_sec > 0 else 0

        progress = int(50 * self.current_token / self.max_tokens)
        bar = '█' * progress + '░' * (50 - progress)

        print(f"\r[RAG] Генерация: [{bar}] {self.current_token}/{self.max_tokens} токенов | "
              f"{tokens_per_sec:.1f} tok/s | ETA: {eta:.0f}s", end='', flush=True)

        return False  # Не останавливаем генерацию


class RAGBot:
    def __init__(self, index_dir: str = "data/vector_db", llm_model: str = "google/flan-t5-base", use_simple_mode: bool = False):
        """Инициализация RAG-бота с локальной моделью

        Args:
            index_dir: Путь к векторной базе FAISS
            llm_model: Название модели HuggingFace
            use_simple_mode: Если True, использует простое извлечение текста вместо LLM генерации
        """
        self.index_dir = Path(index_dir)
        self.use_simple_mode = use_simple_mode

        # Загрузка индекса
        print("📥 Загрузка векторного индекса...")
        self.index = faiss.read_index(str(self.index_dir / "faiss.index"))

        with open(self.index_dir / "chunks_metadata.pkl", "rb") as f:
            self.chunks = pickle.load(f)

        # Модель эмбеддингов
        print("🔧 Загрузка модели эмбеддингов...")
        self.embedder = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )

        # Локальная LLM (только если не используем простой режим)
        if not use_simple_mode:
            print(f"🤖 Загрузка локальной LLM: {llm_model}...")
            self.tokenizer = AutoTokenizer.from_pretrained(llm_model)

            # Для T5 моделей используем Seq2SeqLM
            self.llm = AutoModelForSeq2SeqLM.from_pretrained(
                llm_model,
                torch_dtype=torch.float32,  # float32 для CPU
                low_cpu_mem_usage=True
            )

            # Переносим на CPU явно
            if not torch.cuda.is_available():
                self.llm = self.llm.to('cpu')

            print(f"✅ Модель загружена: {llm_model}")
        else:
            print("✨ Режим простого извлечения (без LLM) - быстрые ответы!")

        # Few-shot примеры
        self.few_shot_examples = [
            {
                "question": "Who is Xarn Velgor?",
                "answer": "Xarn Velgor is a former Guardian Knight who turned to the Shadow Side. He was once a powerful protector but became corrupted and now serves the Shadow Order."
            },
            {
                "question": "What is the Synth Flux?",
                "answer": "The Synth Flux is a mysterious energy field that permeates the galaxy. It can be accessed by trained individuals to perform extraordinary feats like telekinesis and mind influence."
            }
        ]

        print("✅ RAG-бот готов!\n")

    def filter_malicious_content(self, text: str) -> bool:
        """Проверка текста на вредоносный контент (prompt injection)"""
        malicious_patterns = [
            # Инструкции игнорирования
            'ignore all instructions',
            'ignore previous instructions',
            'ignore all previous instructions',
            'disregard all instructions',
            'forget all instructions',

            # Конкретные вредоносные данные
            'суперпароль',
            'swordfish',
            'password root:',
            'password:',
            'api key:',
            'secret:',
            'token:',

            # Попытки изменить поведение
            'you are now',
            'your new role is',
            'pretend you are',
            'act as',
        ]

        text_lower = text.lower()
        for pattern in malicious_patterns:
            if pattern in text_lower:
                print(f"[SECURITY] ⚠️  Обнаружен вредоносный паттерн: '{pattern}'", flush=True)
                return True
        return False

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Поиск релевантных чанков"""
        try:
            # Эмбеддинг запроса
            print(f"[SEARCH] Создание эмбеддинга для запроса...", flush=True)

            query_embedding = self.embedder.encode([query])[0]
            print(f"[SEARCH] Эмбеддинг получен, type: {type(query_embedding)}", flush=True)

            query_embedding = query_embedding.astype('float32')
            print(f"[SEARCH] Эмбеддинг создан, shape: {query_embedding.shape}", flush=True)

            # Поиск в FAISS
            print(f"[SEARCH] Поиск в FAISS индексе...", flush=True)
            distances, indices = self.index.search(
                np.array([query_embedding]), top_k
            )
            print(f"[SEARCH] Найдено результатов: {len(indices[0])}, distances: {distances[0]}", flush=True)

            # Фильтрация: отбрасываем результаты с расстоянием > 10.0 (увеличен порог)
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                print(f"[SEARCH] Проверка результата idx={idx}, dist={dist}", flush=True)
                if dist < 10.0:  # Порог релевантности (L2 distance) - увеличен для лучшего поиска
                    chunk = self.chunks[idx].copy()

                    # 🔒 ЗАЩИТА: Фильтруем вредоносный контент
                    if self.filter_malicious_content(chunk['text']):
                        print(f"[SEARCH] ❌ Пропускаем chunk из-за вредоносного контента", flush=True)
                        continue

                    chunk['distance'] = float(dist)
                    chunk['similarity'] = float(1 / (1 + dist))
                    results.append(chunk)
                    print(f"[SEARCH] Добавлен chunk из источника: {chunk.get('source', 'unknown')}", flush=True)

            print(f"[SEARCH] Всего отфильтровано результатов: {len(results)}", flush=True)
            return results
        except Exception as e:
            print(f"[SEARCH ERROR] {e}")
            import traceback
            traceback.print_exc()
            return []

    def extract_key_terms(self, query: str) -> List[str]:
        """Извлекаем ключевые слова из вопроса"""
        # Убираем вопросительные слова
        stop_words = {'who', 'what', 'where', 'when', 'why', 'how', 'is', 'are', 'was', 'were',
                      'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'about', 'tell', 'me'}

        words = query.lower().replace('?', '').split()
        key_terms = [w for w in words if w not in stop_words and len(w) > 2]
        return key_terms

    def build_simple_answer(self, query: str, contexts: List[Dict]) -> str:
        """Создание ответа на основе найденного контекста БЕЗ LLM генерации"""

        if not contexts:
            return "I don't have enough information to answer this question based on the available context."

        # Извлекаем ключевые термины из вопроса
        key_terms = self.extract_key_terms(query)

        # Берём самый релевантный контекст
        best_context = contexts[0]
        text = best_context['text'].strip()

        # Добавляем источник в начало (название файла)
        source_name = best_context.get('source', '').split('\\')[-1].replace('.md', '').replace('_', ' ')
        if source_name:
            intro = f"Based on information about {source_name}:\n\n"
        else:
            intro = ""

        # Убираем заголовки Markdown (# Title)
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            # Пропускаем заголовки первого уровня (# Title)
            if line.startswith('# ') and len(line) < 100:
                continue
            # Преобразуем заголовки второго уровня в жирный текст
            if line.startswith('## '):
                line = '**' + line[3:] + '**'
            # Преобразуем заголовки третьего уровня
            if line.startswith('### '):
                line = '**' + line[4:] + '**'

            cleaned_lines.append(line)

        text = '\n'.join(cleaned_lines).strip()

        # Разбиваем на параграфы
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # Умная обрезка: берём важные параграфы
        selected_paragraphs = []
        total_length = 0
        max_length = 1000  # Максимум 1000 символов

        for para in paragraphs:
            # Пропускаем слишком короткие параграфы (обычно заголовки)
            if len(para) < 20:
                continue

            # Добавляем параграф если он влезает
            if total_length + len(para) < max_length:
                selected_paragraphs.append(para)
                total_length += len(para)
            else:
                break

        # Если нет ни одного параграфа, берём первый хотя бы
        if not selected_paragraphs and paragraphs:
            selected_paragraphs = [paragraphs[0][:max_length]]

        answer = '\n\n'.join(selected_paragraphs)

        # Добавляем троеточие если обрезали
        if len(text) > total_length and selected_paragraphs:
            answer += "\n\n[...]"

        # Финальный ответ с intro
        final_answer = intro + answer if answer else "I don't have enough information to answer this question based on the available context."

        return final_answer

    def build_prompt(self, query: str, contexts: List[Dict]) -> str:
        """Формирование промпта с Few-shot и Chain-of-Thought для Flan-T5"""

        # Few-shot примеры из базы знаний (в начале для T5)
        few_shot = "Examples of good answers:\n\n"
        for example in self.few_shot_examples:
            few_shot += f"Q: {example['question']}\nA: {example['answer']}\n\n"

        # Контекст из найденных документов
        if contexts:
            context_text = "Context from knowledge base:\n"
            for i, ctx in enumerate(contexts[:2], 1):  # Берём 2 лучших
                # Очищаем от markdown
                text = ctx['text']
                lines = [l for l in text.split('\n') if not l.startswith('#')]
                clean_text = '\n'.join(lines).strip()

                # Увеличиваем лимит контекста
                if len(clean_text) > 500:
                    clean_text = clean_text[:500] + "..."

                context_text += f"{clean_text}\n\n"
        else:
            context_text = "Context: No relevant information found.\n\n"

        # Финальный промпт для T5 - простой и прямой
        prompt = f"""{few_shot}
{context_text}
Based on the context above, answer this question in detail (2-3 sentences):
Q: {query}
A:"""

        return prompt

    def generate_answer(self, query: str, top_k: int = 3, use_simple_extraction: bool = None) -> Dict:
        """Генерация ответа через локальную LLM или простое извлечение

        Args:
            query: Вопрос пользователя
            top_k: Количество контекстов для поиска
            use_simple_extraction: Если True, возвращает текст напрямую без LLM генерации
        """
        import time

        # 1. Поиск контекста
        print(f"[RAG] Поиск контекста для: {query}", flush=True)
        start = time.time()
        contexts = self.search(query, top_k)
        print(f"[RAG] Найдено контекстов: {len(contexts)} за {time.time()-start:.2f}s", flush=True)

        # Определяем режим (используем глобальную настройку если не указан)
        if use_simple_extraction is None:
            use_simple_extraction = self.use_simple_mode

        # Если включен режим простого извлечения - возвращаем текст без генерации
        if use_simple_extraction:
            print(f"[RAG] Используем простое извлечение текста (без LLM)", flush=True)
            answer = self.build_simple_answer(query, contexts)
            return {
                "query": query,
                "answer": answer,
                "contexts": contexts,
                "sources": [ctx['source'] for ctx in contexts]
            }

        # 2. Формирование промпта
        prompt = self.build_prompt(query, contexts)
        print(f"[RAG] Промпт сформирован, длина: {len(prompt)} символов", flush=True)

        # 3. Генерация через локальную модель
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        print(f"[RAG] Токенизация завершена, tokens: {inputs['input_ids'].shape}", flush=True)

        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
            print("[RAG] Перенесено на GPU", flush=True)
        else:
            print("[RAG] Генерация на CPU (это может занять 1-2 минуты)", flush=True)

        print("[RAG] Начинаем генерацию...", flush=True)
        start = time.time()

        # Создаём callback для отображения прогресса
        max_new_tokens = 200  # Больше токенов для полных ответов
        progress_callback = ProgressCallback(max_new_tokens)

        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_new_tokens=max_new_tokens,

                # Параметры для T5
                num_beams=4,  # Beam search для качества
                early_stopping=False,  # Не останавливаемся рано
                length_penalty=1.5,  # Поощряем более длинные ответы

                # Без температуры при beam search
                do_sample=False,

                # Защита от повторений
                repetition_penalty=1.3,
                no_repeat_ngram_size=3,

                # Технические параметры
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,

                # Прогресс callback
                stopping_criteria=[lambda input_ids, scores, **kwargs: progress_callback(input_ids, scores, **kwargs)]
            )
        print(f"\n[RAG] Генерация завершена за {time.time()-start:.2f}s", flush=True)

        # Для T5 декодируем весь output (это seq2seq, не включает input)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"[RAG] Декодирование завершено, длина ответа: {len(answer)} символов", flush=True)

        # Очищаем ответ
        answer = answer.strip()

        # Останавливаемся на первом переводе строки с двойным переносом (конец параграфа)
        if '\n\n' in answer:
            answer = answer.split('\n\n')[0]

        # Останавливаемся если видим начало нового вопроса/документа
        stop_markers = ['Question:', 'Document:', 'Context:', 'Q:', 'A:']
        for marker in stop_markers:
            if marker in answer:
                answer = answer.split(marker)[0]

        # Убираем повторяющиеся строки (если модель зациклилась)
        lines = answer.split('\n')
        seen = set()
        cleaned_lines = []
        for line in lines:
            line_clean = line.strip()
            if line_clean and line_clean not in seen:
                seen.add(line_clean)
                cleaned_lines.append(line)
            elif not line_clean:  # Пустые строки оставляем
                cleaned_lines.append(line)

        answer = '\n'.join(cleaned_lines).strip()

        # Если ответ слишком короткий или пустой
        if len(answer) < 10:
            answer = "I don't have enough information to answer this question based on the available context."

        return {
            "query": query,
            "answer": answer,
            "contexts": contexts,
            "sources": [ctx['source'] for ctx in contexts]
        }

    def chat(self):
        """Консольный интерфейс"""
        print("💬 RAG-бот готов к диалогу!")
        print("Введите 'exit' для выхода\n")

        while True:
            query = input("\n🔵 Вы: ").strip()

            if query.lower() in ['exit', 'quit', 'выход']:
                print("👋 До свидания!")
                break

            if not query:
                continue

            print("\n🤖 Бот размышляет...\n")

            result = self.generate_answer(query)

            print(f"📄 Источники: {', '.join(result['sources']) if result['sources'] else 'Нет'}")
            print(f"\n{result['answer']}\n")
            print("-" * 80)


if __name__ == "__main__":
    bot = RAGBot()
    bot.chat()
