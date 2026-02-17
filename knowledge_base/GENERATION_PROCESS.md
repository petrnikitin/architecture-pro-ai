# Процесс создания базы знаний Cyber Nexus

## Обзор

База знаний **Cyber Nexus** была создана путём преобразования известной вселенной **Star Wars** с полной заменой всех ключевых терминов. Это гарантирует, что LLM не сможет ответить по памяти и будет вынуждена использовать RAG-механизм.

## Шаги создания

### 1. Выбор предметной области

**Выбрана:** Star Wars Universe (starwars.fandom.com)

**Причины выбора:**
- Богатая, хорошо документированная вселенная
- LLM хорошо знакома с оригинальными терминами
- Разнообразие категорий (персонажи, технологии, планеты, организации)
- Сложные взаимосвязи между сущностями

### 2. Сбор материала

Создано 33 документа в 4 категориях:

**Персонажи (12 документов):**
- Главные герои: Xarn Velgor, Kael Novarek, Lyra Zenith, Drake Vortex
- Наставники: Thal Kyros, Zeph Nexar
- Антагонисты: Lord Umbral, Kain Shadowstrike
- Второстепенные: Gorvan, Unit-7X, Cypher-9, Nova Starwind

**Организации (7 документов):**
- Synthari Order (Jedi Order)
- Voidborn (Sith)
- Nexus Dominion (Galactic Empire)
- Liberation Front (Rebel Alliance)
- Prime Covenant (First Order)
- Free Coalition (Resistance)
- Synthetic Legion (Clone Army)

**Планеты (8 документов):**
- Aridus Prime (Tatooine)
- Nexara Central (Coruscant)
- Frosthold (Hoth)
- Verdant Moon (Endor)
- Murkvale (Dagobah)
- Wasteland Sigma (Jakku)
- Seraphina (Naboo)
- Infernis (Mustafar)

**Технологии (6 документов):**
- Void Core (Death Star)
- Plasma Blade (Lightsaber)
- Quantum Drifter (Millennium Falcon)
- Synth Flux (The Force)
- Warp Core (Hyperdrive)
- Titan Walker (AT-AT)

### 3. Создание словаря замен

Файл: `terms_map.json`

**Статистика замен:**
- Всего категорий: 7
- Всего терминов: 100+
- Типы замен: персонажи, организации, планеты, технологии, концепции, расы

**Примеры ключевых замен:**

| Категория | Оригинал | Замена |
|-----------|----------|--------|
| Персонажи | Darth Vader | Xarn Velgor |
| | Luke Skywalker | Kael Novarek |
| | Yoda | Zeph Nexar |
| Организации | Jedi | Synthari |
| | Sith | Voidborn |
| | Empire | Nexus Dominion |
| Концепции | The Force | Synth Flux |
| | Dark Side | Void Resonance |
| | Light Side | Radiant Flow |
| Технологии | Lightsaber | Plasma Blade |
| | Death Star | Void Core |
| Планеты | Tatooine | Aridus Prime |
| | Coruscant | Nexara Central |

### 4. Генерация документов

**Скрипты:**
1. `scripts/generate_knowledge_base.py` - основной генератор (19 документов)
2. `scripts/generate_additional_docs.py` - дополнительные документы (14 документов)
3. `scripts/replace_terms.py` - скрипт замены терминов (если используются сырые тексты)

**Процесс:**
```bash
# Генерация основных документов
python scripts/generate_knowledge_base.py

# Добавление дополнительных документов
python scripts/generate_additional_docs.py
```

### 5. Проверка уникальности

**Тесты:**
1. ✅ Поиск оригинальных терминов в документах
2. ✅ Проверка логичности текстов
3. ✅ Валидация структуры markdown
4. ✅ Проверка связей между документами

**Результат:**
- Оригинальные термины полностью отсутствуют
- Тексты остались логичными и читаемыми
- Сохранены все сюжетные связи

## Технические детали

### Принципы замены терминов

1. **Полнота:** Заменены ВСЕ упоминания оригинальных терминов
2. **Консистентность:** Один оригинальный термин → одна замена во всех документах
3. **Порядок замены:** Сначала длинные фразы, потом короткие (избежание partial matches)
4. **Word boundaries:** Используются границы слов для точного совпадения

### Структура документов

Каждый документ содержит:
- **Заголовок (H1):** Название сущности
- **Overview:** Краткое описание
- **Разделы (H2):** Структурированная информация
  - Background/History
  - Key Events/Abilities
  - Legacy/Impact
- **Связи:** Упоминания других сущностей из базы знаний

### Формат файлов

- **Формат:** Markdown (.md)
- **Кодировка:** UTF-8
- **Размер:** 500-2000 слов на документ
- **Язык:** Английский (как в оригинальных материалах)

## Проверка работоспособности RAG

### Вопросы для LLM БЕЗ RAG (должна не знать ответа):

1. "Who is Xarn Velgor?"
2. "What is the Synth Flux?"
3. "Tell me about the Void Core"
4. "Where is Aridus Prime?"
5. "What are the Synthari?"

**Ожидаемый ответ:** "I don't have information about that."

### Вопросы для LLM С RAG (должна найти ответ):

1. "Who is Xarn Velgor and what is his connection to Kael Novarek?"
2. "Explain the difference between Radiant Flow and Void Resonance"
3. "How was the Void Core destroyed?"
4. "What happened on Aridus Prime?"
5. "Who founded the Synthari Order?"

**Ожидаемый ответ:** Точные ответы на основе документов.

## Статистика базы знаний

```
📊 Cyber Nexus Knowledge Base Statistics:

Total Documents:        33
Total Words:           ~25,000
Total Characters:      ~150,000
Average Doc Length:    ~750 words

Categories:
├── Characters:        12 documents
├── Organizations:     7 documents
├── Planets:           8 documents
└── Technology:        6 documents

Terms Replaced:        100+
Uniqueness:            100% (no original terms found)
```

## Результат

✅ **Создана уникальная база знаний из 33 документов**
✅ **Все термины Star Wars заменены на Cyber Nexus**
✅ **LLM не сможет ответить по памяти**
✅ **Идеально подходит для тестирования RAG-системы**

## Использование

Документы находятся в `knowledge_base/processed/` и готовы для:
1. Индексации в векторной базе данных (FAISS)
2. Генерации эмбеддингов
3. Тестирования RAG-пайплайна
4. Оценки качества ответов бота
