import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from mistral_client import MistralClient

logger = logging.getLogger(__name__)

class AgentType:
    DATABASE_EXPERT = "database_expert"
    API_DEVELOPER = "api_developer"
    DEVOPS_SPECIALIST = "devops_specialist"
    SECURITY_EXPERT = "security_expert"
    BACKEND_ARCHITECT = "backend_architect"

class BaseAgent(ABC):
    def __init__(self, agent_type: str, name: str, description: str):
        self.agent_type = agent_type
        self.name = name
        self.description = description
        # Each agent has its own MistralClient instance
        self.mistral = MistralClient()

    @abstractmethod
    def can_handle(self, message: str, language: str = "ru") -> float:
        pass

    @abstractmethod
    def get_system_prompt(self, language: str = "ru") -> str:
        pass

    def process_message(self, message: str, language: str = "ru") -> Dict[str, Any]:
        try:
            # Get agent-specific system prompt
            system_prompt = self.get_system_prompt(language)
            
            # Get agent-specific context from knowledge base
            context = self.get_agent_context(message, language)
            
            # Use agent-specific system prompt for this message
            response = self.mistral.get_response_with_system_prompt(
                message, context, language, system_prompt
            )
            return {
                'response': response,
                'confidence': self.can_handle(message, language),
                'agent_type': self.agent_type,
                'agent_name': self.name,
                'context_used': bool(context)
            }
        except Exception as e:
            logger.error(f"Error in {self.name} agent: {str(e)}")
            return {
                'response': f"Извините, возникла ошибка при обработке запроса по теме '{self.description}'.",
                'confidence': 0.1,
                'agent_type': self.agent_type,
                'agent_name': self.name,
                'context_used': False
            }
    
    def get_agent_context(self, message: str, language: str = "ru") -> str:
        """Get agent-specific context from knowledge base"""
        try:
            from models import AgentKnowledgeBase
            from app import db
            
            # Search for relevant knowledge entries for this agent
            knowledge_entries = AgentKnowledgeBase.query.filter_by(
                agent_type=self.agent_type,
                is_active=True
            ).order_by(AgentKnowledgeBase.priority.asc()).all()
            
            if not knowledge_entries:
                return ""
            
            # Build context from relevant entries
            context_parts = []
            message_lower = message.lower()
            
            for entry in knowledge_entries:
                # Check if keywords match the message
                if entry.keywords:
                    keywords = [k.strip().lower() for k in entry.keywords.split(',')]
                    if any(keyword in message_lower for keyword in keywords):
                        content = entry.content_ru if language == 'ru' else entry.content_kz
                        context_parts.append(f"**{entry.title}**\n{content}")
                        
                        # Limit context to prevent too long prompts
                        if len(context_parts) >= 3:
                            break
            
            # If no keyword matches, include high-priority general entries
            if not context_parts:
                for entry in knowledge_entries[:2]:  # Top 2 priority entries
                    content = entry.content_ru if language == 'ru' else entry.content_kz
                    context_parts.append(f"**{entry.title}**\n{content}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting agent context: {str(e)}")
            return ""

class DatabaseExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            AgentType.DATABASE_EXPERT,
            "Database Expert",
            "Эксперт по базам данных и SQL-разработке"
        )

    def can_handle(self, message: str, language: str = "ru") -> float:
        keywords = ["база данных", "sql", "postgresql", "mysql", "mongodb", "запрос", "таблица", "индекс", "оптимизация", "миграция", "orm", "модель"]
        return 1.0 if any(k in message.lower() for k in keywords) else 0.3

    def get_system_prompt(self, language: str = "ru") -> str:
        if language == "kz":
            return """
Сіз деректер базасы және SQL дамыту жөніндегі сарапшысыз. Сіз:
- Деректер базасын жобалауда көмектесесіз
- SQL сұрауларын оңтайландырасыз
- Қауіпсіздік мәселелерін шешесіз
- ORM мен модельдерді түсіндіресіз
- Дұрыс индекстеуге кеңес бересіз

Жауаптарыңыз техникалық, нақты және практикалық болуы керек. Markdown форматын қолданыңыз.
"""
        return """
Вы эксперт по базам данных и SQL-разработке. Вы помогаете с:
- Проектированием баз данных
- Оптимизацией SQL-запросов
- Решением вопросов безопасности
- Объяснением ORM и моделей
- Рекомендациями по правильному индексированию

Ваши ответы должны быть техническими, конкретными и практичными. Используйте формат Markdown.
"""

class APIDeveloperAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            AgentType.API_DEVELOPER,
            "API Developer",
            "Разработчик REST API и веб-сервисов"
        )

    def can_handle(self, message: str, language: str = "ru") -> float:
        keywords = ["api", "rest", "fastapi", "flask", "django", "endpoint", "json", "swagger", "postman", "middleware", "аутентификация", "авторизация"]
        return 1.0 if any(k in message.lower() for k in keywords) else 0.3

    def get_system_prompt(self, language: str = "ru") -> str:
        if language == "kz":
            return """
Сіз REST API және веб-қызметтер дамытушысыз. Сіз:
- API дизайны мен архитектурасын жобалайсыз
- RESTful принциптерін түсіндіресіз
- Аутентификация және авторизацияны орнатасыз
- API құжаттамасын құрасыз
- Өнімділік мәселелерін шешесіз

Жауаптарыңыз техникалық, нақты және практикалық болуы керек. Markdown форматын қолданыңыз.
"""
        return """
Вы разработчик REST API и веб-сервисов. Вы помогаете с:
- Проектированием API дизайна и архитектуры
- Объяснением RESTful принципов
- Настройкой аутентификации и авторизации
- Созданием документации API
- Решением проблем производительности

Ваши ответы должны быть техническими, конкретными и практичными. Используйте формат Markdown.
"""

class DevOpsSpecialistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            AgentType.DEVOPS_SPECIALIST,
            "DevOps Specialist",
            "Специалист по DevOps, CI/CD и инфраструктуре"
        )

    def can_handle(self, message: str, language: str = "ru") -> float:
        keywords = ["devops", "docker", "kubernetes", "ci/cd", "jenkins", "gitlab", "github actions", "aws", "azure", "мониторинг", "логирование", "развертывание"]
        return 1.0 if any(k in message.lower() for k in keywords) else 0.2

    def get_system_prompt(self, language: str = "ru") -> str:
        if language == "kz":
            return """
Сіз DevOps, CI/CD және инфрақұрылым мамандарысыз. Сіз:
- Автоматтандыру процестерін орнатасыз
- Контейнерлеу және оркестрацияны түсіндіресіз
- Мониторинг және логтауды конфигурациялайсыз
- Бұлтты қызметтермен жұмыс істейсіз
- Қауіпсіздік мәселелерін шешесіз

Жауаптарыңыз техникалық және практикалық болуы керек. Markdown форматын қолданыңыз.
"""
        return """
Вы специалист по DevOps, CI/CD и инфраструктуре. Вы помогаете с:
- Настройкой процессов автоматизации
- Объяснением контейнеризации и оркестрации
- Конфигурированием мониторинга и логирования
- Работой с облачными сервисами
- Решением вопросов безопасности

Ваши ответы должны быть техническими и практичными. Используйте формат Markdown.
"""

class SecurityExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            AgentType.SECURITY_EXPERT,
            "Security Expert",
            "Эксперт по информационной безопасности и защите данных"
        )

    def can_handle(self, message: str, language: str = "ru") -> float:
        keywords = ["безопасность", "защита", "уязвимость", "шифрование", "токен", "jwt", "oauth", "ssl", "https", "аутентификация", "авторизация", "хэш"]
        return 1.0 if any(k in message.lower() for k in keywords) else 0.2

    def get_system_prompt(self, language: str = "ru") -> str:
        if language == "kz":
            return """
Сіз ақпараттық қауіпсіздік және деректерді қорғау сарапшысыз. Сіз:
- Қауіпсіздік тәуекелдерін бағалайсыз
- Аутентификация жүйелерін орнатасыз
- Деректерді шифрлауды түсіндіресіз
- Осалдықтарды анықтаңыз
- Қауіпсіз кодтау тәжірибелерін ұсынасыз

Жауаптарыңыз техникалық және қауіпсіздік бағытталған болуы керек. Markdown форматын қолданыңыз.
"""
        return """
Вы эксперт по информационной безопасности и защите данных. Вы помогаете с:
- Оценкой рисков безопасности
- Настройкой систем аутентификации
- Объяснением шифрования данных
- Выявлением уязвимостей
- Рекомендациями по безопасному кодированию

Ваши ответы должны быть техническими и ориентированными на безопасность. Используйте формат Markdown.
"""

class BackendArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            AgentType.BACKEND_ARCHITECT,
            "Backend Architect",
            "Архитектор backend-систем и проектирования"
        )

    def can_handle(self, message: str, language: str = "ru") -> float:
        keywords = ["архитектура", "микросервис", "паттерн", "дизайн", "масштабирование", "производительность", "кэширование", "очереди", "балансировка", "нагрузка", "проектирование", "система", "проектирован"]
        return 1.0 if any(k in message.lower() for k in keywords) else 0.2

    def get_system_prompt(self, language: str = "ru") -> str:
        if language == "kz":
            return """
Сіз backend-жүйелер мен жобалаудың сәулетшісіз. Сіз:
- Жүйе архитектурасын жобалайсыз
- Микроқызметтерді түсіндіресіз
- Өнімділікті оңтайландырасыз
- Масштабтау стратегияларын ұсынасыз
- Паттерн мен best practices туралы кеңес бересіз

Жауаптарыңыз стратегиялық және архитектуралық болуы керек. Markdown форматын қолданыңыз.
"""
        return """
Вы архитектор backend-систем и проектирования. Вы помогаете с:
- Проектированием системной архитектуры
- Объяснением микросервисов
- Оптимизацией производительности
- Рекомендациями по масштабированию
- Советами по паттернам и best practices

Ваши ответы должны быть стратегическими и архитектурными. Используйте формат Markdown.
"""

class AgentRouter:
    def __init__(self):
        # Each agent now creates its own MistralClient instance
        self.agents = [
            DatabaseExpertAgent(),
            APIDeveloperAgent(),
            DevOpsSpecialistAgent(),
            SecurityExpertAgent(),
            BackendArchitectAgent()
        ]
        logger.info(f"AgentRouter initialized with {len(self.agents)} agents")

    def route_message(self, message: str, language: str = "ru") -> Dict[str, Any]:
        best_conf = 0
        best_agent = None
        for agent in self.agents:
            conf = agent.can_handle(message, language)
            if conf > best_conf:
                best_conf = conf
                best_agent = agent
        return best_agent.process_message(message, language) if best_agent else {}

    def get_available_agents(self) -> List[Dict[str, str]]:
        return [{'type': a.agent_type, 'name': a.name, 'description': a.description} for a in self.agents]