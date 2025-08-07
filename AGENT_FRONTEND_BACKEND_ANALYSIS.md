# Анализ связи фронтенд-агентов с бэкендом | Frontend-Backend Agent Connection Analysis

## Краткое резюме | Executive Summary

**Да, бэкенд-агенты тесно связаны с фронтендом** через сложную систему маршрутизации и API-интерфейсы. Система представляет собой полноценную многоагентную архитектуру с интеллектуальным распределением запросов.

**Yes, backend agents are tightly connected with the frontend** through a sophisticated routing system and API interfaces. The system implements a complete multi-agent architecture with intelligent request distribution.

---

## Архитектура системы | System Architecture

```
Frontend (UI) → API Gateway (/api/chat) → AgentRouter → Specialized Agents → AI Processing
     ↓                    ↓                     ↓              ↓              ↓
User Interface    Request Handling    Message Routing    Domain Logic    External AI
```

---

## 🤖 Бэкенд-агенты | Backend Agents

Система включает **5 специализированных AI-агентов**:

### 1. **AI-Abitur** (`ai_abitur`)
- **Назначение**: Помощь абитуриентам при поступлении
- **Ключевые слова**: поступление, абитуриент, документы, экзамен, приём
- **Файл**: `agents.py:104-138`

### 2. **KadrAI** (`kadrai`) 
- **Назначение**: Поддержка сотрудников в кадровых вопросах
- **Ключевые слова**: кадры, отпуск, перевод, приказ, сотрудник
- **Файл**: `agents.py:139-171`

### 3. **UniNav** (`uninav`)
- **Назначение**: Сопровождение студентов по учебным процессам
- **Ключевые слова**: расписание, учёба, занятие, заявление, деканат
- **Файл**: `agents.py:172-204`

### 4. **CareerNavigator** (`career_navigator`)
- **Назначение**: Помощь в трудоустройстве студентов и выпускников
- **Ключевые слова**: работа, трудоустройство, вакансии, резюме, карьера
- **Файл**: `agents.py:205-237`

### 5. **UniRoom** (`uniroom`)
- **Назначение**: Поддержка студентов в общежитии
- **Ключевые слова**: общежитие, заселение, переселение, бытовые вопросы
- **Файл**: `agents.py:238-270`

---

## 🌐 Фронтенд-интеграция | Frontend Integration

### 1. **Главная страница** (`/templates/index_new.html`)

Содержит карточки агентов с JavaScript-функциями:

```html
<div class="col-lg-4 col-md-6">
    <div class="agent-card" onclick="startChatWithAgent('admission')">
        <div class="agent-icon">
            <i class="fas fa-graduation-cap"></i>
        </div>
        <h5 class="agent-title">{{ _('agent.admission') }}</h5>
        <p class="agent-description">Поможет с вопросами поступления...</p>
    </div>
</div>
```

**JavaScript функция**:
```javascript
function startChatWithAgent(agentType) {
    localStorage.setItem('selectedAgent', agentType);
    window.location.href = '{{ url_for("views.chat_new") }}';
}
```

### 2. **Чат-интерфейс** (`/templates/chat_new.html`)

Содержит селектор агентов:

```html
<div class="agent-badge active" data-agent="auto">
    <div class="agent-icon"><i class="fas fa-magic"></i></div>
    <span>Авто</span>
</div>
<div class="agent-badge" data-agent="admission">
    <div class="agent-icon"><i class="fas fa-graduation-cap"></i></div>
    <span>{{ _('agent.admission') }}</span>
</div>
```

### 3. **JavaScript-обработка** (`/static/js/main.js`)

Управление выбором агентов:

```javascript
const payload = {
    message,
    agent_type: currentModel,  // Тип выбранного агента
    language: currentLang,
};

const resp = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
});
```

---

## 🔄 API-интеграция | API Integration

### Основной эндпоинт: `/api/chat` (`views.py:65-152`)

**Входные параметры**:
```json
{
    "message": "Как поступить в университет?",
    "language": "ru",
    "agent": "ai_abitur"  // Опционально
}
```

**Логика маршрутизации**:
```python
if agent_type and agent_type != 'auto':
    # Принудительный выбор агента
    for agent in router.agents:
        if agent.agent_type == agent_type:
            result = agent.process_message(user_message, language)
            break
else:
    # Автоматический выбор агента
    result = router.route_message(user_message, language)
```

**Ответ**:
```json
{
    "success": true,
    "response": "Для поступления в университет...",
    "agent_name": "AI-Abitur",
    "agent_type": "ai_abitur",
    "confidence": 0.85,
    "query_id": 123
}
```

---

## 🧠 Интеллектуальная маршрутизация | Intelligent Routing

### Система оценки уверенности (`agents.py:271-292`)

```python
def route_message(self, message: str, language: str = "ru") -> Dict[str, Any]:
    best_conf = 0
    best_agent = None
    for agent in self.agents:
        conf = agent.can_handle(message, language)  # Оценка 0.0-1.0
        if conf > best_conf:
            best_conf = conf
            best_agent = agent
    return best_agent.process_message(message, language)
```

### Пример оценки уверенности:

**AI-Abitur агент**:
```python
def can_handle(self, message: str, language: str = "ru") -> float:
    keywords = ["поступление", "абитуриент", "документы", "экзамен"]
    return 1.0 if any(k in message.lower() for k in keywords) else 0.3
```

---

## 💾 Отслеживание и аналитика | Tracking & Analytics

### Модель данных (`models.py`)

```python
class UserQuery(db.Model):
    # ... базовые поля
    agent_type = db.Column(db.String(50))        # Тип агента
    agent_name = db.Column(db.String(100))       # Имя агента  
    agent_confidence = db.Column(db.Float)       # Уверенность (0.0-1.0)
    context_used = db.Column(db.Boolean)         # Использован ли контекст
```

### Аналитические эндпоинты

1. **`/api/agents`** - Информация о доступных агентах
2. **`/admin/api/analytics/agents`** - Статистика по агентам
3. **`/admin/api/analytics/summary`** - Сводная аналитика

---

## 🎯 Ключевые точки интеграции | Key Integration Points

### 1. **Выбор агента в UI**
- Фронтенд: карточки агентов → JavaScript → localStorage
- Бэкенд: получение `agent_type` → маршрутизация к нужному агенту

### 2. **Автоматическая маршрутизация**
- Фронтенд: отправка сообщения без указания агента
- Бэкенд: анализ ключевых слов → выбор лучшего агента

### 3. **Обратная связь**
- Бэкенд: возврат информации об агенте (имя, тип, уверенность)
- Фронтенд: отображение информации об обработавшем агенте

### 4. **Аналитика**
- Бэкенд: сохранение всех взаимодействий с агентами
- Фронтенд: админ-панель с графиками использования агентов

---

## 📊 Пример полного цикла | Complete Workflow Example

### Сценарий: Пользователь спрашивает о поступлении

1. **Фронтенд**: Пользователь выбирает "Поступление" или пишет "Как поступить?"
2. **API**: Запрос отправляется на `/api/chat` с параметрами
3. **Маршрутизация**: `AgentRouter` анализирует сообщение
4. **Обработка**: `AI-Abitur` агент обрабатывает запрос (confidence: 1.0)
5. **AI**: Агент использует специализированный промпт для Mistral AI
6. **Ответ**: Возврат ответа с метаданными агента
7. **UI**: Отображение ответа с указанием агента "AI-Abitur"
8. **Аналитика**: Сохранение в БД для последующего анализа

---

## 🔧 Техническая реализация | Technical Implementation

### Базовый класс агента (`agents.py:16-103`)

```python
class BaseAgent(ABC):
    def __init__(self, agent_type: str, name: str, description: str):
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.mistral = MistralClient()  # Собственный клиент AI

    @abstractmethod
    def can_handle(self, message: str, language: str = "ru") -> float:
        pass  # Оценка способности обработать сообщение

    @abstractmethod  
    def get_system_prompt(self, language: str = "ru") -> str:
        pass  # Специализированный промпт для агента

    def process_message(self, message: str, language: str = "ru") -> Dict[str, Any]:
        # Единая логика обработки с использованием специализированного промпта
```

### Инициализация роутера (`views.py:21-27`)

```python
def initialize_agent_router():
    global agent_router
    if agent_router is None:
        from agents import AgentRouter
        agent_router = AgentRouter()  # Создает все 5 агентов
    return agent_router
```

---

## 📈 Аналитика использования | Usage Analytics

### Дашборд агентов (`/admin/dashboard`)

- **Круговая диаграмма**: распределение запросов по агентам
- **Столбчатая диаграмма**: время ответа по агентам
- **Линейный график**: активность по дням
- **Метрики успешности**: процент высокоуверенных ответов

### Отслеживание эффективности

```python
# Сохранение метрик в БД
user_query = UserQuery(
    user_message=message,
    bot_response=result['response'],
    agent_type=result.get('agent_type'),
    agent_name=result.get('agent_name'),
    agent_confidence=result.get('confidence', 0.0),
    context_used=result.get('context_used', False)
)
```

---

## 🚀 Готовность к производству | Production Readiness

### Текущее состояние:
- ✅ **Полная интеграция фронтенд-бэкенд**
- ✅ **5 специализированных агентов**
- ✅ **Интеллектуальная маршрутизация**
- ✅ **Система аналитики**
- ✅ **API документация**
- ✅ **Многоязычная поддержка (RU/KZ)**

### Требования для деплоя:
- Настройка переменных окружения (`MISTRAL_API_KEY`, `DATABASE_URL`)
- PostgreSQL для продакшена
- Настройка CORS для домена университета

---

## 📝 Заключение | Conclusion

**Система демонстрирует продвинутую интеграцию фронтенда и бэкенда** с использованием многоагентной архитектуры. Каждый агент имеет специализацию, систему оценки уверенности и интегрированную аналитику. Фронтенд предоставляет интуитивный интерфейс для выбора агентов и отображения результатов их работы.

**The system demonstrates advanced frontend-backend integration** using a multi-agent architecture. Each agent has specialization, confidence scoring, and integrated analytics. The frontend provides an intuitive interface for agent selection and displaying their work results.

Это **готовая к производству система** для университета "Болашак" с полной функциональностью чат-бота и административной панелью.

This is a **production-ready system** for Bolashak University with complete chatbot functionality and administrative dashboard.