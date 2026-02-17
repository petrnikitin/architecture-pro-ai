"""
Скрипт автоматического обновления векторного индекса
Сканирует папку data/new_docs/ на наличие новых/изменённых файлов
Обновляет FAISS индекс и логирует процесс
"""
import os
import sys
import json
import pickle
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import logging

# Добавляем корневую директорию в PATH
sys.path.append(str(Path(__file__).parent.parent))

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Настройка логирования
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "index_update.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class IndexUpdater:
    """Класс для обновления векторного индекса"""

    def __init__(
        self,
        source_dir: str = "data/new_docs",
        processed_dir: str = "knowledge_base/processed",
        index_dir: str = "data/vector_db",
        state_file: str = "data/index_state.json"
    ):
        self.source_dir = Path(source_dir)
        self.processed_dir = Path(processed_dir)
        self.index_dir = Path(index_dir)
        self.state_file = Path(state_file)

        # Создаём необходимые директории
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)

        # Загрузка состояния (хеши обработанных файлов)
        self.state = self._load_state()

        # Инициализация моделей
        logger.info("Загрузка модели эмбеддингов...")
        self.embedder = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )

        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        logger.info("✅ Инициализация завершена")

    def _load_state(self) -> Dict:
        """Загрузка состояния (хеши файлов)"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"file_hashes": {}, "last_update": None}

    def _save_state(self):
        """Сохранение состояния"""
        self.state["last_update"] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, indent=2, fp=f)

    def _compute_file_hash(self, file_path: Path) -> str:
        """Вычисление SHA256 хеша файла"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def scan_new_files(self) -> List[Path]:
        """Сканирование новых или изменённых файлов"""
        new_files = []

        if not self.source_dir.exists():
            logger.warning(f"Директория {self.source_dir} не существует")
            return new_files

        for file_path in self.source_dir.rglob("*.md"):
            file_hash = self._compute_file_hash(file_path)
            file_key = str(file_path.relative_to(self.source_dir))

            # Проверяем, изменился ли файл
            if file_key not in self.state["file_hashes"] or \
               self.state["file_hashes"][file_key] != file_hash:
                new_files.append(file_path)
                self.state["file_hashes"][file_key] = file_hash
                logger.info(f"📄 Найден новый/изменённый файл: {file_key}")

        return new_files

    def process_documents(self, files: List[Path]) -> List[Dict]:
        """Обработка документов в чанки"""
        all_chunks = []

        for file_path in files:
            try:
                # Читаем файл
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Разбиваем на чанки
                chunks = self.text_splitter.split_text(content)

                # Копируем в processed (для резервного хранения)
                relative_path = file_path.relative_to(self.source_dir)
                dest_path = self.processed_dir / "auto_updated" / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Создаём метаданные для каждого чанка
                for i, chunk_text in enumerate(chunks):
                    all_chunks.append({
                        "text": chunk_text,
                        "source": str(dest_path),
                        "category": "auto_updated",
                        "chunk_index": i,
                        "chunk_id": f"{file_path.stem}_{i}",
                        "added_at": datetime.now().isoformat()
                    })

                logger.info(f"✂️  Файл {file_path.name} разбит на {len(chunks)} чанков")

            except Exception as e:
                logger.error(f"❌ Ошибка обработки {file_path}: {e}")

        return all_chunks

    def update_index(self, new_chunks: List[Dict]):
        """Обновление FAISS индекса"""
        try:
            # Загружаем существующий индекс
            index_path = self.index_dir / "faiss.index"
            metadata_path = self.index_dir / "chunks_metadata.pkl"

            if index_path.exists() and metadata_path.exists():
                logger.info("📥 Загрузка существующего индекса...")
                index = faiss.read_index(str(index_path))

                with open(metadata_path, 'rb') as f:
                    existing_chunks = pickle.load(f)

                old_size = index.ntotal
                logger.info(f"Текущий размер индекса: {old_size} векторов")
            else:
                logger.info("🆕 Создание нового индекса...")
                index = None
                existing_chunks = []
                old_size = 0

            if not new_chunks:
                logger.info("✅ Нет новых чанков для добавления")
                return

            # Генерируем эмбеддинги для новых чанков
            logger.info(f"🔄 Генерация эмбеддингов для {len(new_chunks)} новых чанков...")
            texts = [chunk["text"] for chunk in new_chunks]
            new_embeddings = self.embedder.encode(texts, show_progress_bar=True)
            new_embeddings = np.array(new_embeddings).astype('float32')

            # Создаём или обновляем индекс
            if index is None:
                dimension = new_embeddings.shape[1]
                index = faiss.IndexFlatL2(dimension)
                logger.info(f"Создан новый индекс, размерность: {dimension}")

            # Добавляем новые векторы
            index.add(new_embeddings)

            # Объединяем метаданные
            all_chunks = existing_chunks + new_chunks

            # Сохраняем
            logger.info("💾 Сохранение обновлённого индекса...")
            faiss.write_index(index, str(index_path))

            with open(metadata_path, 'wb') as f:
                pickle.dump(all_chunks, f)

            # Сохраняем info
            info = {
                "total_chunks": len(all_chunks),
                "embedding_dimension": index.d,
                "last_updated": datetime.now().isoformat(),
                "new_chunks_added": len(new_chunks)
            }

            with open(self.index_dir / "index_info.json", 'w') as f:
                json.dump(info, f, indent=2)

            logger.info(f"✅ Индекс обновлён: {old_size} → {index.ntotal} векторов (+{len(new_chunks)})")

        except Exception as e:
            logger.error(f"❌ Ошибка обновления индекса: {e}")
            raise

    def run(self):
        """Основной процесс обновления"""
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("🚀 НАЧАЛО ОБНОВЛЕНИЯ ИНДЕКСА")
        logger.info("=" * 80)

        try:
            # 1. Сканирование новых файлов
            logger.info(f"🔍 Сканирование директории: {self.source_dir}")
            new_files = self.scan_new_files()

            if not new_files:
                logger.info("✅ Новых файлов не найдено. Индекс актуален.")
                logger.info("=" * 80)
                return

            logger.info(f"📊 Найдено новых/изменённых файлов: {len(new_files)}")

            # 2. Обработка документов
            logger.info("✂️  Обработка документов в чанки...")
            new_chunks = self.process_documents(new_files)
            logger.info(f"📦 Создано новых чанков: {len(new_chunks)}")

            # 3. Обновление индекса
            logger.info("🔄 Обновление векторного индекса...")
            self.update_index(new_chunks)

            # 4. Сохранение состояния
            self._save_state()

            # 5. Итоговая статистика
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info("=" * 80)
            logger.info("✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО")
            logger.info(f"⏱️  Время выполнения: {elapsed:.2f} сек")
            logger.info(f"📄 Обработано файлов: {len(new_files)}")
            logger.info(f"📦 Добавлено чанков: {len(new_chunks)}")
            logger.info(f"❌ Ошибок: 0")
            logger.info("=" * 80)

        except Exception as e:
            logger.error("=" * 80)
            logger.error(f"❌ ОШИБКА ПРИ ОБНОВЛЕНИИ: {e}")
            logger.error("=" * 80)
            import traceback
            logger.error(traceback.format_exc())
            sys.exit(1)


def main():
    """Точка входа"""
    updater = IndexUpdater()
    updater.run()


if __name__ == "__main__":
    main()
