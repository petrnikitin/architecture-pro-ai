"""
Модуль для логирования запросов к RAG боту
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class QueryLogger:
    """Логирование запросов в JSONL формат"""

    def __init__(self, log_file: str = "logs/query_logs.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log_query(
        self,
        query: str,
        chunks_found: bool,
        num_chunks: int,
        answer: str,
        sources: List[str],
        confidence: float,
        duration_sec: float
    ):
        """Логировать один запрос"""

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "chunks_found": chunks_found,
            "num_chunks": num_chunks,
            "answer_length": len(answer),
            "answer": answer[:200],  # Первые 200 символов
            "success": chunks_found and len(answer) > 20,
            "sources": sources,
            "confidence": confidence,
            "duration_sec": round(duration_sec, 2)
        }

        # Append в JSONL
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

        return log_entry
