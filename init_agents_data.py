#!/usr/bin/env python3
"""
Скрипт для инициализации базовых данных агентов и их баз знаний
"""

import logging
from app import create_app, db
from models import AgentType, AgentKnowledgeBase, AdminUser

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_agent_types():
    """Инициализация типов агентов"""
    
    agent_types_data = [
        {
            'type_code': 'database_expert',
            'name_ru': 'Database Expert',
            'name_kz': 'Database Expert',
            'name_en': 'Database Expert',
            'description_ru': 'Эксперт по базам данных и SQL-разработке. Помощь в проектировании баз данных, оптимизации запросов, настройке индексов.',
            'description_kz': 'Деректер базасы және SQL дамыту жөніндегі сарапшы. Деректер базасын жобалау, сұрауларды оңтайландыру, индекстерді орнату.',
            'description_en': 'Database and SQL development expert. Help with database design, query optimization, index configuration.',
            'system_prompt_ru': 'Вы - эксперт по базам данных и SQL-разработке. Помогайте с проектированием баз данных, оптимизацией SQL-запросов, решением вопросов безопасности, объяснением ORM и моделей, рекомендациями по правильному индексированию.',
            'system_prompt_kz': 'Сіз деректер базасы және SQL дамыту жөніндегі сарапшысыз. Деректер базасын жобалауда, SQL сұрауларын оңтайландыруда, қауіпсіздік мәселелерін шешуде, ORM мен модельдерді түсіндіруде көмектесіңіз.',
            'system_prompt_en': 'You are a database and SQL development expert. Help with database design, SQL query optimization, security issues, explaining ORM and models, recommendations for proper indexing.',
            'icon_class': 'fas fa-database',
            'color_scheme': 'primary',
            'priority': 1
        },
        {
            'type_code': 'api_developer',
            'name_ru': 'API Developer',
            'name_kz': 'API Developer',
            'name_en': 'API Developer',
            'description_ru': 'Разработчик REST API и веб-сервисов. Проектирование API, настройка аутентификации, создание документации.',
            'description_kz': 'REST API және веб-қызметтер дамытушысы. API жобалау, аутентификация орнату, құжаттама құру.',
            'description_en': 'REST API and web services developer. API design, authentication setup, documentation creation.',
            'system_prompt_ru': 'Вы - разработчик REST API и веб-сервисов. Помогайте с проектированием API дизайна и архитектуры, объяснением RESTful принципов, настройкой аутентификации и авторизации, созданием документации API.',
            'system_prompt_kz': 'Сіз REST API және веб-қызметтер дамытушысыз. API дизайны мен архитектурасын жобалауда, RESTful принциптерін түсіндіруде, аутентификация мен авторизацияны орнатуда көмектесіңіз.',
            'system_prompt_en': 'You are a REST API and web services developer. Help with API design and architecture, explaining RESTful principles, setting up authentication and authorization, creating API documentation.',
            'icon_class': 'fas fa-code',
            'color_scheme': 'info',
            'priority': 2
        },
        {
            'type_code': 'devops_specialist',
            'name_ru': 'DevOps Specialist',
            'name_kz': 'DevOps Specialist',
            'name_en': 'DevOps Specialist',
            'description_ru': 'Специалист по DevOps, CI/CD и инфраструктуре. Автоматизация развертывания, контейнеризация, мониторинг.',
            'description_kz': 'DevOps, CI/CD және инфрақұрылым маманы. Орналастыруды автоматтандыру, контейнерлеу, мониторинг.',
            'description_en': 'DevOps, CI/CD and infrastructure specialist. Deployment automation, containerization, monitoring.',
            'system_prompt_ru': 'Вы - специалист по DevOps, CI/CD и инфраструктуре. Помогайте с настройкой процессов автоматизации, объяснением контейнеризации и оркестрации, конфигурированием мониторинга и логирования.',
            'system_prompt_kz': 'Сіз DevOps, CI/CD және инфрақұрылым мамандарысыз. Автоматтандыру процестерін орнатуда, контейнерлеу мен оркестрацияны түсіндіруде, мониторинг пен логтауды конфигурациялауда көмектесіңіз.',
            'system_prompt_en': 'You are a DevOps, CI/CD and infrastructure specialist. Help with setting up automation processes, explaining containerization and orchestration, configuring monitoring and logging.',
            'icon_class': 'fas fa-cogs',
            'color_scheme': 'success',
            'priority': 3
        },
        {
            'type_code': 'security_expert',
            'name_ru': 'Security Expert',
            'name_kz': 'Security Expert',
            'name_en': 'Security Expert',
            'description_ru': 'Эксперт по информационной безопасности и защите данных. Оценка рисков, настройка аутентификации, защита от уязвимостей.',
            'description_kz': 'Ақпараттық қауіпсіздік және деректерді қорғау сарапшысы. Тәуекелдерді бағалау, аутентификация орнату, осалдықтардан қорғау.',
            'description_en': 'Information security and data protection expert. Risk assessment, authentication setup, vulnerability protection.',
            'system_prompt_ru': 'Вы - эксперт по информационной безопасности и защите данных. Помогайте с оценкой рисков безопасности, настройкой систем аутентификации, объяснением шифрования данных, выявлением уязвимостей.',
            'system_prompt_kz': 'Сіз ақпараттық қауіпсіздік және деректерді қорғау сарапшысыз. Қауіпсіздік тәуекелдерін бағалауда, аутентификация жүйелерін орнатуда, деректерді шифрлауды түсіндіруде көмектесіңіз.',
            'system_prompt_en': 'You are an information security and data protection expert. Help with security risk assessment, authentication system setup, data encryption explanation, vulnerability identification.',
            'icon_class': 'fas fa-shield-alt',
            'color_scheme': 'warning',
            'priority': 4
        },
        {
            'type_code': 'backend_architect',
            'name_ru': 'Backend Architect',
            'name_kz': 'Backend Architect',
            'name_en': 'Backend Architect',
            'description_ru': 'Архитектор backend-систем и проектирования. Проектирование архитектуры, микросервисы, оптимизация производительности.',
            'description_kz': 'Backend-жүйелер мен жобалаудың сәулетшісі. Архитектураны жобалау, микроқызметтер, өнімділікті оңтайландыру.',
            'description_en': 'Backend systems and design architect. Architecture design, microservices, performance optimization.',
            'system_prompt_ru': 'Вы - архитектор backend-систем и проектирования. Помогайте с проектированием системной архитектуры, объяснением микросервисов, оптимизацией производительности, рекомендациями по масштабированию.',
            'system_prompt_kz': 'Сіз backend-жүйелер мен жобалаудың сәулетшісіз. Жүйе архитектурасын жобалауда, микроқызметтерді түсіндіруде, өнімділікті оңтайландыруда көмектесіңіз.',
            'system_prompt_en': 'You are a backend systems and design architect. Help with system architecture design, microservices explanation, performance optimization, scaling recommendations.',
            'icon_class': 'fas fa-sitemap',
            'color_scheme': 'secondary',
            'priority': 5
        }
    ]
    
    for agent_data in agent_types_data:
        existing_agent = AgentType.query.filter_by(type_code=agent_data['type_code']).first()
        if not existing_agent:
            agent_type = AgentType(**agent_data)
            db.session.add(agent_type)
            logger.info(f"Создан тип агента: {agent_data['type_code']}")
        else:
            logger.info(f"Тип агента уже существует: {agent_data['type_code']}")
    
    db.session.commit()
    logger.info("Инициализация типов агентов завершена")

def init_knowledge_base():
    """Инициализация базы знаний агентов"""
    
    # Получаем или создаем админа для связи
    admin_user = AdminUser.query.first()
    if not admin_user:
        admin_user = AdminUser(
            username='system',
            email='system@bolashak.kz',
            password_hash='system',
            full_name='System Administrator'
        )
        db.session.add(admin_user)
        db.session.commit()
    
    knowledge_data = [
        # Database Expert Agent Knowledge
        {
            'agent_type': 'database_expert',
            'title': 'Проектирование базы данных',
            'content_ru': 'Основные принципы проектирования баз данных:\n\n**Нормализация:**\n• 1NF: Атомарность значений\n• 2NF: Устранение частичных зависимостей\n• 3NF: Устранение транзитивных зависимостей\n\n**Типы связей:**\n• One-to-One (1:1)\n• One-to-Many (1:N)\n• Many-to-Many (M:N)\n\n**Индексы:**\n• Primary Index (первичный ключ)\n• Secondary Index (вторичные индексы)\n• Composite Index (составные индексы)\n• Unique Index (уникальные индексы)\n\n**Оптимизация запросов:**\n• Использование EXPLAIN для анализа\n• Избегание SELECT *\n• Правильное использование JOIN\n• Кэширование результатов',
            'content_kz': 'Деректер базасын жобалаудың негізгі принциптері:\n\n**Нормализация:**\n• 1NF: Мәндердің атомарлығы\n• 2NF: Ішінара тәуелділіктерді жою\n• 3NF: Транзитивті тәуелділіктерді жою\n\n**Байланыс түлері:**\n• Бірден-бірге (1:1)\n• Бірден-көпке (1:N)\n• Көптен-көпке (M:N)\n\n**Индекстер:**\n• Primary Index (негізгі кілт)\n• Secondary Index (қайталама индекстер)\n• Composite Index (құрама индекстер)\n• Unique Index (бірегей индекстер)\n\n**Сұрауларды оңтайландыру:**\n• Талдау үшін EXPLAIN қолдану\n• SELECT * -тан аулақ болу\n• JOIN-ды дұрыс қолдану\n• Нәтижелерді кэштеу',
            'content_en': 'Basic principles of database design:\n\n**Normalization:**\n• 1NF: Atomicity of values\n• 2NF: Elimination of partial dependencies\n• 3NF: Elimination of transitive dependencies\n\n**Relationship types:**\n• One-to-One (1:1)\n• One-to-Many (1:N)\n• Many-to-Many (M:N)\n\n**Indexes:**\n• Primary Index (primary key)\n• Secondary Index (secondary indexes)\n• Composite Index (composite indexes)\n• Unique Index (unique indexes)\n\n**Query optimization:**\n• Using EXPLAIN for analysis\n• Avoiding SELECT *\n• Proper use of JOIN\n• Result caching',
            'keywords': 'база данных, проектирование, нормализация, индексы, sql',
            'category': 'База данных',
            'tags': 'database,design,normalization',
            'priority': 1,
            'is_featured': True
        },
        {
            'agent_type': 'database_expert',
            'title': 'SQL оптимизация',
            'content_ru': 'Методы оптимизации SQL-запросов:\n\n**EXPLAIN планы:**\n• Анализ выполнения запросов\n• Выявление медленных операций\n• Оценка стоимости операций\n\n**Индексирование:**\n• Создание индексов для часто используемых колонок\n• B-tree индексы для поиска по диапазону\n• Hash индексы для точного поиска\n• Составные индексы для сложных запросов\n\n**Оптимизация JOIN:**\n• INNER JOIN vs LEFT JOIN\n• Порядок таблиц в JOIN\n• Использование подзапросов vs JOIN\n\n**Кэширование:**\n• Query cache\n• Result set cache\n• Connection pooling',
            'content_kz': 'SQL-сұрауларды оңтайландыру әдістері:\n\n**EXPLAIN жоспарлары:**\n• Сұрауларды орындауды талдау\n• Баяу операцияларды анықтау\n• Операциялардың құнын бағалау\n\n**Индекстеу:**\n• Жиі қолданылатын бағандарға индекс құру\n• Диапазон бойынша іздеуге арналған B-tree индекстері\n• Нақты іздеуге арналған Hash индекстері\n• Күрделі сұрауларға арналған құрама индекстер\n\n**JOIN оңтайландыру:**\n• INNER JOIN vs LEFT JOIN\n• JOIN-дағы кестелердің реті\n• Ішкі сұраулар vs JOIN қолдану\n\n**Кэштеу:**\n• Query cache\n• Result set cache\n• Connection pooling',
            'content_en': 'SQL query optimization methods:\n\n**EXPLAIN plans:**\n• Query execution analysis\n• Identifying slow operations\n• Cost estimation of operations\n\n**Indexing:**\n• Creating indexes for frequently used columns\n• B-tree indexes for range searches\n• Hash indexes for exact searches\n• Composite indexes for complex queries\n\n**JOIN optimization:**\n• INNER JOIN vs LEFT JOIN\n• Table order in JOIN\n• Using subqueries vs JOIN\n\n**Caching:**\n• Query cache\n• Result set cache\n• Connection pooling',
            'keywords': 'sql, оптимизация, индексы, производительность',
            'category': 'База данных',
            'tags': 'sql,optimization,performance',
            'priority': 2,
            'is_featured': True
        },
        
        # API Developer Agent Knowledge
        {
            'agent_type': 'api_developer',
            'title': 'REST API дизайн',
            'content_ru': 'Принципы проектирования REST API:\n\n**HTTP методы:**\n• GET - получение данных\n• POST - создание ресурса\n• PUT - полное обновление\n• PATCH - частичное обновление\n• DELETE - удаление ресурса\n\n**Коды ответов:**\n• 200 OK - успешный запрос\n• 201 Created - ресурс создан\n• 400 Bad Request - неверный запрос\n• 401 Unauthorized - не авторизован\n• 404 Not Found - ресурс не найден\n• 500 Internal Server Error - ошибка сервера\n\n**Структура URL:**\n• /api/v1/users - коллекция пользователей\n• /api/v1/users/123 - конкретный пользователь\n• /api/v1/users/123/orders - заказы пользователя\n\n**Лучшие практики:**\n• Использование JSON для обмена данными\n• Версионирование API\n• Пагинация для больших списков\n• Валидация входных данных',
            'content_kz': 'REST API жобалау принциптері:\n\n**HTTP әдістері:**\n• GET - деректерді алу\n• POST - ресурс құру\n• PUT - толық жаңарту\n• PATCH - ішінара жаңарту\n• DELETE - ресурсты жою\n\n**Жауап кодтары:**\n• 200 OK - сәтті сұрау\n• 201 Created - ресурс құрылды\n• 400 Bad Request - қате сұрау\n• 401 Unauthorized - авторизация жоқ\n• 404 Not Found - ресурс табылмады\n• 500 Internal Server Error - сервер қатесі\n\n**URL құрылымы:**\n• /api/v1/users - пайдаланушылар жинағы\n• /api/v1/users/123 - нақты пайдаланушы\n• /api/v1/users/123/orders - пайдаланушының тапсырыстары\n\n**Ең жақсы тәжірибелер:**\n• Деректер алмасуға JSON қолдану\n• API нұсқалау\n• Үлкен тізімдерге пагинация\n• Кіріс деректерін растау',
            'content_en': 'REST API design principles:\n\n**HTTP methods:**\n• GET - retrieve data\n• POST - create resource\n• PUT - full update\n• PATCH - partial update\n• DELETE - delete resource\n\n**Response codes:**\n• 200 OK - successful request\n• 201 Created - resource created\n• 400 Bad Request - invalid request\n• 401 Unauthorized - not authorized\n• 404 Not Found - resource not found\n• 500 Internal Server Error - server error\n\n**URL structure:**\n• /api/v1/users - user collection\n• /api/v1/users/123 - specific user\n• /api/v1/users/123/orders - user orders\n\n**Best practices:**\n• Using JSON for data exchange\n• API versioning\n• Pagination for large lists\n• Input data validation',
            'keywords': 'api, rest, http, json, endpoint',
            'category': 'API разработка',
            'tags': 'api,rest,http',
            'priority': 1,
            'is_featured': True
        },
        
        # DevOps Specialist Agent Knowledge  
        {
            'agent_type': 'devops_specialist',
            'title': 'Docker контейнеризация',
            'content_ru': 'Основы работы с Docker:\n\n**Dockerfile:**\n```dockerfile\nFROM python:3.9-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD ["python", "app.py"]\n```\n\n**Docker команды:**\n• `docker build -t myapp .` - сборка образа\n• `docker run -p 8000:8000 myapp` - запуск контейнера\n• `docker ps` - список запущенных контейнеров\n• `docker logs <container_id>` - просмотр логов\n• `docker exec -it <container_id> bash` - подключение к контейнеру\n\n**Docker Compose:**\n```yaml\nversion: "3.8"\nservices:\n  app:\n    build: .\n    ports:\n      - "8000:8000"\n  db:\n    image: postgres:13\n    environment:\n      POSTGRES_DB: mydb\n```\n\n**Лучшие практики:**\n• Использование multi-stage builds\n• Минимальные базовые образы\n• .dockerignore для исключения файлов\n• Не запускать контейнеры от root',
            'content_kz': 'Docker жұмысының негіздері:\n\n**Dockerfile:**\n```dockerfile\nFROM python:3.9-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD ["python", "app.py"]\n```\n\n**Docker командалары:**\n• `docker build -t myapp .` - образды құрастыру\n• `docker run -p 8000:8000 myapp` - контейнерді іске қосу\n• `docker ps` - іске қосылған контейнерлер тізімі\n• `docker logs <container_id>` - логтарды қарау\n• `docker exec -it <container_id> bash` - контейнерге қосылу\n\n**Docker Compose:**\n```yaml\nversion: "3.8"\nservices:\n  app:\n    build: .\n    ports:\n      - "8000:8000"\n  db:\n    image: postgres:13\n    environment:\n      POSTGRES_DB: mydb\n```\n\n**Ең жақсы тәжірибелер:**\n• Multi-stage builds қолдану\n• Минималды базалық образдар\n• Файлдарды алып тастауға арналған .dockerignore\n• Контейнерлерді root-тан іске қоспау',
            'content_en': 'Docker basics:\n\n**Dockerfile:**\n```dockerfile\nFROM python:3.9-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD ["python", "app.py"]\n```\n\n**Docker commands:**\n• `docker build -t myapp .` - build image\n• `docker run -p 8000:8000 myapp` - run container\n• `docker ps` - list running containers\n• `docker logs <container_id>` - view logs\n• `docker exec -it <container_id> bash` - connect to container\n\n**Docker Compose:**\n```yaml\nversion: "3.8"\nservices:\n  app:\n    build: .\n    ports:\n      - "8000:8000"\n  db:\n    image: postgres:13\n    environment:\n      POSTGRES_DB: mydb\n```\n\n**Best practices:**\n• Using multi-stage builds\n• Minimal base images\n• .dockerignore for excluding files\n• Don\'t run containers as root',
            'keywords': 'docker, контейнер, dockerfile, compose',
            'category': 'DevOps',
            'tags': 'docker,container,devops',
            'priority': 1,
            'is_featured': True
        },
        
        # Security Expert Agent Knowledge
        {
            'agent_type': 'security_expert',
            'title': 'Аутентификация и авторизация',
            'content_ru': 'Системы аутентификации и авторизации:\n\n**JWT (JSON Web Token):**\n• Статeless токены\n• Структура: Header.Payload.Signature\n• Содержит claims (утверждения)\n• Проверка подписи для валидации\n\n**OAuth 2.0:**\n• Authorization Code Flow\n• Client Credentials Flow\n• Resource Owner Password Flow\n• Implicit Flow (deprecated)\n\n**Безопасное хранение паролей:**\n• Хэширование с солью (bcrypt, Argon2)\n• Никогда не храните пароли в открытом виде\n• Минимальные требования к сложности\n• Двухфакторная аутентификация (2FA)\n\n**Защита API:**\n• Rate limiting\n• API ключи\n• CORS настройки\n• Input validation\n• SQL injection protection',
            'content_kz': 'Аутентификация және авторизация жүйелері:\n\n**JWT (JSON Web Token):**\n• Stateless токендер\n• Құрылымы: Header.Payload.Signature\n• Claims (мәлімдемелер) қамтиды\n• Растау үшін қолтаңбаны тексеру\n\n**OAuth 2.0:**\n• Authorization Code Flow\n• Client Credentials Flow\n• Resource Owner Password Flow\n• Implicit Flow (ескірген)\n\n**Құпия сөздерді қауіпсіз сақтау:**\n• Тұзбен хэштеу (bcrypt, Argon2)\n• Құпия сөздерді ашық түрде ешқашан сақтамаңыз\n• Күрделілікке минималды талаптар\n• Екі факторлы аутентификация (2FA)\n\n**API қорғау:**\n• Rate limiting\n• API кілттері\n• CORS баптаулары\n• Input validation\n• SQL injection қорғанысы',
            'content_en': 'Authentication and authorization systems:\n\n**JWT (JSON Web Token):**\n• Stateless tokens\n• Structure: Header.Payload.Signature\n• Contains claims\n• Signature verification for validation\n\n**OAuth 2.0:**\n• Authorization Code Flow\n• Client Credentials Flow\n• Resource Owner Password Flow\n• Implicit Flow (deprecated)\n\n**Secure password storage:**\n• Hashing with salt (bcrypt, Argon2)\n• Never store passwords in plain text\n• Minimum complexity requirements\n• Two-factor authentication (2FA)\n\n**API protection:**\n• Rate limiting\n• API keys\n• CORS settings\n• Input validation\n• SQL injection protection',
            'keywords': 'безопасность, аутентификация, jwt, oauth, пароли',
            'category': 'Безопасность',
            'tags': 'security,authentication,jwt',
            'priority': 1,
            'is_featured': True
        },
        
        # Backend Architect Agent Knowledge
        {
            'agent_type': 'backend_architect',
            'title': 'Микросервисная архитектура',
            'content_ru': 'Принципы микросервисной архитектуры:\n\n**Характеристики микросервисов:**\n• Декомпозиция по бизнес-возможностям\n• Децентрализованное управление\n• Отказоустойчивость\n• Независимое развертывание\n\n**Паттерны коммуникации:**\n• Синхронные: REST API, GraphQL\n• Асинхронные: Message Queues (RabbitMQ, Kafka)\n• Event-driven архитектура\n• Service mesh (Istio, Linkerd)\n\n**Управление данными:**\n• Database per service\n• Saga pattern для транзакций\n• CQRS (Command Query Responsibility Segregation)\n• Event sourcing\n\n**Мониторинг и логирование:**\n• Distributed tracing (Jaeger, Zipkin)\n• Centralized logging (ELK stack)\n• Service discovery (Consul, Eureka)\n• Health checks',
            'content_kz': 'Микроқызметтер архитектурасының принциптері:\n\n**Микроқызметтердің сипаттамалары:**\n• Бизнес мүмкіндіктері бойынша декомпозиция\n• Орталықсыздандырылған басқару\n• Қателерге төзімділік\n• Тәуелсіз орналастыру\n\n**Коммуникация паттерндері:**\n• Синхронды: REST API, GraphQL\n• Асинхронды: Message Queues (RabbitMQ, Kafka)\n• Event-driven архитектурасы\n• Service mesh (Istio, Linkerd)\n\n**Деректерді басқару:**\n• Қызметке арналған дерекқор\n• Транзакциялар үшін Saga паттерні\n• CQRS (Command Query Responsibility Segregation)\n• Event sourcing\n\n**Мониторинг және логтау:**\n• Distributed tracing (Jaeger, Zipkin)\n• Орталықтандырылған логтау (ELK stack)\n• Service discovery (Consul, Eureka)\n• Health checks',
            'content_en': 'Microservices architecture principles:\n\n**Microservices characteristics:**\n• Decomposition by business capabilities\n• Decentralized governance\n• Fault tolerance\n• Independent deployment\n\n**Communication patterns:**\n• Synchronous: REST API, GraphQL\n• Asynchronous: Message Queues (RabbitMQ, Kafka)\n• Event-driven architecture\n• Service mesh (Istio, Linkerd)\n\n**Data management:**\n• Database per service\n• Saga pattern for transactions\n• CQRS (Command Query Responsibility Segregation)\n• Event sourcing\n\n**Monitoring and logging:**\n• Distributed tracing (Jaeger, Zipkin)\n• Centralized logging (ELK stack)\n• Service discovery (Consul, Eureka)\n• Health checks',
            'keywords': 'микросервисы, архитектура, масштабирование, паттерны',
            'category': 'Архитектура',
            'tags': 'microservices,architecture,patterns',
            'priority': 1,
            'is_featured': True
        }
    ]
    
    for knowledge in knowledge_data:
        existing_knowledge = AgentKnowledgeBase.query.filter_by(
            agent_type=knowledge['agent_type'], 
            title=knowledge['title']
        ).first()
        
        if not existing_knowledge:
            kb_entry = AgentKnowledgeBase(
                created_by=admin_user.id,
                **knowledge
            )
            db.session.add(kb_entry)
            logger.info(f"Создана запись базы знаний: {knowledge['title']} для {knowledge['agent_type']}")
        else:
            logger.info(f"Запись базы знаний уже существует: {knowledge['title']}")
    
    db.session.commit()
    logger.info("Инициализация базы знаний завершена")

def main():
    """Главная функция инициализации"""
    with create_app().app_context():
        logger.info("Начинаем инициализацию данных агентов...")
        
        try:
            init_agent_types()
            init_knowledge_base()
            
            logger.info("Инициализация данных агентов завершена успешно!")
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации данных: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    main()