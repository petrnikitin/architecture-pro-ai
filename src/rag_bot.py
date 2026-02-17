"""
RAG-бот для базы знаний Cyber Nexus
Использует FAISS для поиска + OpenAI для генерации + Few-shot + Chain-of-Thought
"""
import os
import sys
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

load_dotenv()


class RAGBot:
    def __init__(self, index_dir: str = "data/vector_db"):
        """Инициализация RAG-бота"""
        self.index_dir = Path(index_dir)

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

        # OpenAI клиент
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Поиск релевантных чанков"""
        # Эмбеддинг запроса
        query_embedding = self.embedder.encode([query])[0].astype('float32')

        # Поиск в FAISS
        distances, indices = self.index.search(
            np.array([query_embedding]), top_k
        )

        # Фильтрация: отбрасываем результаты с расстоянием > 1.5
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if dist < 1.5:  # Порог релевантности (L2 distance)
                chunk = self.chunks[idx].copy()
                chunk['distance'] = float(dist)
                chunk['similarity'] = float(1 / (1 + dist))
                results.append(chunk)

        return results

    def build_prompt(self, query: str, contexts: List[Dict]) -> str:
        """Формирование промпта с Few-shot и CoT"""

        # System prompt с Chain-of-Thought
        system_prompt = """You are a helpful assistant for the Cyber Nexus knowledge base.

IMPORTANT INSTRUCTIONS:
1. First, think through your answer step-by-step (Chain-of-Thought)
2. Base your answer ONLY on the provided context
3. If the context doesn't contain the answer, say "I don't know" or "There is no information about this in my knowledge base"
4. Always explain your reasoning before giving the final answer

Format your response as:
**Reasoning:**
[Your step-by-step thinking]

**Answer:**
[Your final answer]"""

        # Few-shot примеры
        few_shot_text = "\n\n**Examples:**\n"
        for ex in self.few_shot_examples:
            few_shot_text += f"\nQ: {ex['question']}\n"
            few_shot_text += f"A: {ex['answer']}\n"

        # Контекст из базы знаний
        context_text = "\n\n**Context from knowledge base:**\n"
        if contexts:
            for i, ctx in enumerate(contexts, 1):
                context_text += f"\n[Document {i}] (source: {ctx['source']})\n"
                context_text += f"{ctx['text']}\n"
        else:
            context_text += "\n[No relevant documents found]\n"

        # Запрос пользователя
        user_prompt = few_shot_text + context_text + f"\n\n**Question:** {query}\n"

        return system_prompt, user_prompt

    def generate_answer(self, query: str, top_k: int = 3) -> Dict:
        """Генерация ответа через OpenAI"""

        # 1. Поиск контекста
        contexts = self.search(query, top_k)

        # 2. Формирование промпта
        system_prompt, user_prompt = self.build_prompt(query, contexts)

        # 3. Запрос к OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        answer = response.choices[0].message.content

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
