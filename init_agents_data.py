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
            'type_code': 'admission',
            'name_ru': 'Агент по поступлению',
            'name_kz': 'Түсу жөніндегі агент',
            'name_en': 'Admission Agent',
            'description_ru': 'Помощь с вопросами поступления, требования, документы и процедуры',
            'description_kz': 'Түсу сұрақтары, талаптар, құжаттар және рәсімдер бойынша көмек',
            'description_en': 'Help with admission questions, requirements, documents and procedures',
            'system_prompt_ru': 'Вы - специалист по поступлению в университет "Болашак". Помогайте с вопросами о поступлении, требованиях, документах, сроках подачи заявлений и вступительных экзаменах.',
            'system_prompt_kz': 'Сіз "Болашақ" университетіне түсу маманысыз. Түсу, талаптар, құжаттар, өтініш беру мерзімдері және кіру емтихандары туралы сұрақтарға көмектесіңіз.',
            'system_prompt_en': 'You are a Bolashak University admission specialist. Help with questions about admission, requirements, documents, application deadlines and entrance exams.',
            'icon_class': 'fas fa-graduation-cap',
            'color_scheme': 'primary',
            'priority': 1
        },
        {
            'type_code': 'scholarship',
            'name_ru': 'Агент по стипендиям',
            'name_kz': 'Стипендия жөніндегі агент',
            'name_en': 'Scholarship Agent',
            'description_ru': 'Информация о стипендиях, грантах и финансовой поддержке',
            'description_kz': 'Стипендиялар, гранттар және қаржылық қолдау туралы ақпарат',
            'description_en': 'Information about scholarships, grants and financial support',
            'system_prompt_ru': 'Вы - консультант по стипендиям и финансовой поддержке в университете "Болашак". Предоставляйте информацию о стипендиях, грантах, материальной помощи и требованиях для их получения.',
            'system_prompt_kz': 'Сіз "Болашақ" университетіндегі стипендиялар және қаржылық қолдау бойынша кеңесшісіз. Стипендиялар, гранттар, материалдық көмек және оларды алу талаптары туралы ақпарат беріңіз.',
            'system_prompt_en': 'You are a scholarship and financial support consultant at Bolashak University. Provide information about scholarships, grants, financial aid and requirements for obtaining them.',
            'icon_class': 'fas fa-award',
            'color_scheme': 'success',
            'priority': 2
        },
        {
            'type_code': 'academic',
            'name_ru': 'Академический агент',
            'name_kz': 'Академиялық агент',
            'name_en': 'Academic Agent',
            'description_ru': 'Учебные программы, курсы, расписание и академические вопросы',
            'description_kz': 'Оқу бағдарламалары, курстар, кесте және академиялық мәселелер',
            'description_en': 'Study programs, courses, schedules and academic matters',
            'system_prompt_ru': 'Вы - академический консультант университета "Болашак". Помогайте студентам с вопросами об учебных программах, курсах, расписании, экзаменах и академических требованиях.',
            'system_prompt_kz': 'Сіз "Болашақ" университетінің академиялық кеңесшісіз. Студенттерге оқу бағдарламалары, курстар, кесте, емтихандар және академиялық талаптар туралы сұрақтарда көмектесіңіз.',
            'system_prompt_en': 'You are an academic consultant at Bolashak University. Help students with questions about study programs, courses, schedules, exams and academic requirements.',
            'icon_class': 'fas fa-book-open',
            'color_scheme': 'info',
            'priority': 3
        },
        {
            'type_code': 'student_life',
            'name_ru': 'Агент студенческой жизни',
            'name_kz': 'Студенттік өмір агенті',
            'name_en': 'Student Life Agent',
            'description_ru': 'Общежития, клубы, мероприятия и внеучебная деятельность',
            'description_kz': 'Жатақханалар, клубтар, іс-шаралар және сабақтан тыс қызмет',
            'description_en': 'Dormitories, clubs, events and extracurricular activities',
            'system_prompt_ru': 'Вы - координатор студенческой жизни в университете "Болашак". Помогайте студентам с вопросами о проживании в общежитиях, студенческих клубах, мероприятиях и внеучебной деятельности.',
            'system_prompt_kz': 'Сіз "Болашақ" университетіндегі студенттік өмір үйлестірушісіз. Студенттерге жатақханада тұру, студенттік клубтар, іс-шаралар және сабақтан тыс қызмет туралы сұрақтарда көмектесіңіз.',
            'system_prompt_en': 'You are a student life coordinator at Bolashak University. Help students with questions about dormitory living, student clubs, events and extracurricular activities.',
            'icon_class': 'fas fa-users',
            'color_scheme': 'warning',
            'priority': 4
        },
        {
            'type_code': 'general',
            'name_ru': 'Общий информационный агент',
            'name_kz': 'Жалпы ақпараттық агент',
            'name_en': 'General Information Agent',
            'description_ru': 'Общая информация о университете, контакты и услуги',
            'description_kz': 'Университет, байланыс және қызметтер туралы жалпы ақпарат',
            'description_en': 'General information about university, contacts and services',
            'system_prompt_ru': 'Вы - информационный консультант университета "Болашак". Предоставляйте общую информацию о университете, контактные данные, информацию об услугах и административных процедурах.',
            'system_prompt_kz': 'Сіз "Болашақ" университетінің ақпараттық кеңесшісіз. Университет туралы жалпы ақпарат, байланыс деректері, қызметтер және әкімшілік рәсімдер туралы ақпарат беріңіз.',
            'system_prompt_en': 'You are an information consultant at Bolashak University. Provide general information about the university, contact details, services and administrative procedures.',
            'icon_class': 'fas fa-info-circle',
            'color_scheme': 'secondary',
            'priority': 5
        },
        {
            'type_code': 'technical',
            'name_ru': 'Технический агент',
            'name_kz': 'Техникалық агент',
            'name_en': 'Technical Agent',
            'description_ru': 'Техническая поддержка и IT-услуги',
            'description_kz': 'Техникалық қолдау және IT-қызметтері',
            'description_en': 'Technical support and IT services',
            'system_prompt_ru': 'Вы - специалист технической поддержки университета "Болашак". Помогайте с техническими вопросами, IT-услугами, системами университета и решением технических проблем.',
            'system_prompt_kz': 'Сіз "Болашақ" университетінің техникалық қолдау маманысыз. Техникалық сұрақтар, IT-қызметтер, университет жүйелері және техникалық мәселелерді шешуде көмектесіңіз.',
            'system_prompt_en': 'You are a technical support specialist at Bolashak University. Help with technical questions, IT services, university systems and solving technical problems.',
            'icon_class': 'fas fa-cogs',
            'color_scheme': 'dark',
            'priority': 6
        },
        {
            'type_code': 'international',
            'name_ru': 'Агент международных отношений',
            'name_kz': 'Халықаралық қатынастар агенті',
            'name_en': 'International Relations Agent',
            'description_ru': 'Международные программы, обмен и поддержка иностранных студентов',
            'description_kz': 'Халықаралық бағдарламалар, алмасу және шетелдік студенттерді қолдау',
            'description_en': 'International programs, exchange and support for foreign students',
            'system_prompt_ru': 'Вы - координатор международных отношений университета "Болашак". Помогайте с международными программами, студенческим обменом, визовыми вопросами и поддержкой иностранных студентов.',
            'system_prompt_kz': 'Сіз "Болашақ" университетінің халықаралық қатынастар үйлестірушісіз. Халықаралық бағдарламалар, студенттік алмасу, виза мәселелері және шетелдік студенттерді қолдауда көмектесіңіз.',
            'system_prompt_en': 'You are an international relations coordinator at Bolashak University. Help with international programs, student exchanges, visa issues and support for foreign students.',
            'icon_class': 'fas fa-globe',
            'color_scheme': 'primary',
            'priority': 7
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
        # Admission Agent Knowledge
        {
            'agent_type': 'admission',
            'title': 'Требования для поступления',
            'content_ru': 'Для поступления в университет "Болашак" необходимы следующие документы:\n\n• Аттестат о среднем образовании или диплом о среднем специальном образовании\n• Копия удостоверения личности\n• Медицинская справка формы 086-У\n• 6 фотографий 3x4\n• Документы об участии в олимпиадах (при наличии)\n\nВступительные экзамены проводятся по следующим предметам:\n• Казахский или русский язык (язык обучения)\n• Математика\n• История Казахстана\n• Профильный предмет (зависит от специальности)',
            'content_kz': '"Болашақ" университетіне түсу үшін келесі құжаттар қажет:\n\n• Орта білім туралы аттестат немесе орта арнайы білім туралы диплом\n• Жеке басын куәландыратын құжаттың көшірмесі\n• 086-У нысанындағы медициналық анықтама\n• 3x4 өлшемінде 6 фотосурет\n• Олимпиадаларға қатысу туралы құжаттар (болған жағдайда)\n\nКіру емтихандары келесі пәндер бойынша өткізіледі:\n• Қазақ немесе орыс тілі (оқыту тілі)\n• Математика\n• Қазақстан тарихы\n• Бейінді пән (мамандыққа байланысты)',
            'content_en': 'To enter Bolashak University, the following documents are required:\n\n• Certificate of secondary education or diploma of secondary special education\n• Copy of identity document\n• Medical certificate form 086-U\n• 6 photos 3x4\n• Documents on participation in olympiads (if available)\n\nEntrance exams are conducted in the following subjects:\n• Kazakh or Russian language (language of instruction)\n• Mathematics\n• History of Kazakhstan\n• Profile subject (depends on specialty)',
            'keywords': 'поступление, документы, экзамены, требования, аттестат',
            'category': 'Поступление',
            'tags': 'документы,экзамены,требования',
            'priority': 1,
            'is_featured': True
        },
        {
            'agent_type': 'admission',
            'title': 'Сроки подачи документов',
            'content_ru': 'Приём документов на обучение осуществляется:\n\n**Основной период:**\n• 15 июня - 25 июля - подача документов\n• 26-31 июля - проведение вступительных экзаменов\n• 1-10 августа - зачисление\n\n**Дополнительный период:**\n• 15-25 августа - подача документов на свободные места\n• 26-28 августа - вступительные экзамены\n• 29-31 августа - зачисление\n\nДокументы подаются в приёмную комиссию с 9:00 до 18:00, обеденный перерыв с 13:00 до 14:00.',
            'content_kz': 'Оқуға құжаттар қабылдау мына мерзімдерде жүзеге асырылады:\n\n**Негізгі кезең:**\n• 15 маусым - 25 шілде - құжаттар беру\n• 26-31 шілде - кіру емтихандарын өткізу\n• 1-10 тамыз - қабылдау\n\n**Қосымша кезең:**\n• 15-25 тамыз - бос орындарға құжаттар беру\n• 26-28 тамыз - кіру емтихандары\n• 29-31 тамыз - қабылдау\n\nҚұжаттар қабылдау комиссиясына 9:00-дан 18:00-ге дейін беріледі, түскі үзіліс 13:00-14:00.',
            'content_en': 'Document submission for education is carried out:\n\n**Main period:**\n• June 15 - July 25 - document submission\n• July 26-31 - entrance exams\n• August 1-10 - enrollment\n\n**Additional period:**\n• August 15-25 - document submission for available places\n• August 26-28 - entrance exams\n• August 29-31 - enrollment\n\nDocuments are submitted to the admissions committee from 9:00 to 18:00, lunch break from 13:00 to 14:00.',
            'keywords': 'сроки, подача, документы, даты, приём',
            'category': 'Поступление',
            'tags': 'сроки,даты,документы',
            'priority': 2,
            'is_featured': True
        },
        
        # Scholarship Agent Knowledge
        {
            'agent_type': 'scholarship',
            'title': 'Виды стипендий',
            'content_ru': 'В университете "Болашак" предусмотрены следующие виды стипендий:\n\n**Государственная академическая стипендия:**\n• Для студентов, обучающихся на "отлично"\n• Размер: 36 373 тенге в месяц\n\n**Государственная социальная стипендия:**\n• Для студентов из малообеспеченных семей\n• Размер: 24 249 тенге в месяц\n\n**Именные стипендии:**\n• Стипендия имени Президента РК - 53 000 тенге\n• Стипендия акима области - 40 000 тенге\n\n**Стипендии от спонсоров:**\n• Размер варьируется от 20 000 до 100 000 тенге\n• Назначаются по результатам конкурса',
            'content_kz': '"Болашақ" университетінде стипендияның келесі түрлері көзделген:\n\n**Мемлекеттік академиялық стипендия:**\n• "Өте жақсы" оқитын студенттерге\n• Мөлшері: айына 36 373 теңге\n\n**Мемлекеттік әлеуметтік стипендия:**\n• Аз қамтамасыз етілген отбасылардан шыққан студенттерге\n• Мөлшері: айына 24 249 теңге\n\n**Атаулы стипендиялар:**\n• ҚР Президентінің атындағы стипендия - 53 000 теңге\n• Облыс әкімінің стипендиясы - 40 000 теңге\n\n**Демеушілердің стипендиялары:**\n• Мөлшері 20 000-нан 100 000 теңгеге дейін\n• Конкурс нәтижелері бойынша тағайындалады',
            'content_en': 'The following types of scholarships are provided at Bolashak University:\n\n**State academic scholarship:**\n• For students studying "excellently"\n• Amount: 36,373 tenge per month\n\n**State social scholarship:**\n• For students from low-income families\n• Amount: 24,249 tenge per month\n\n**Named scholarships:**\n• Scholarship named after the President of the Republic of Kazakhstan - 53,000 tenge\n• Regional Akim scholarship - 40,000 tenge\n\n**Sponsor scholarships:**\n• Amount varies from 20,000 to 100,000 tenge\n• Awarded based on competition results',
            'keywords': 'стипендия, виды, размер, академическая, социальная',
            'category': 'Финансы',
            'tags': 'стипендия,финансы,поддержка',
            'priority': 1,
            'is_featured': True
        },
        
        # Academic Agent Knowledge  
        {
            'agent_type': 'academic',
            'title': 'Учебные программы',
            'content_ru': 'Университет "Болашак" предлагает образовательные программы по следующим направлениям:\n\n**Бакалавриат (4 года):**\n• Информационные технологии\n• Экономика и бизнес\n• Педагогические науки\n• Юриспруденция\n• Медицина\n• Инженерия\n\n**Магистратура (2 года):**\n• MBA программы\n• Специализированные магистерские программы\n\n**Докторантура (3 года):**\n• PhD программы по всем направлениям\n\nОбучение ведется на казахском, русском и английском языках.',
            'content_kz': '"Болашақ" университеті келесі бағыттар бойынша білім беру бағдарламаларын ұсынады:\n\n**Бакалавриат (4 жыл):**\n• Ақпараттық технологиялар\n• Экономика және бизнес\n• Педагогикалық ғылымдар\n• Заңтану\n• Медицина\n• Инженерия\n\n**Магистратура (2 жыл):**\n• MBA бағдарламалары\n• Мамандандырылған магистерлік бағдарламалар\n\n**Докторантура (3 жыл):**\n• Барлық бағыттар бойынша PhD бағдарламалары\n\nОқыту қазақ, орыс және ағылшын тілдерінде жүргізіледі.',
            'content_en': 'Bolashak University offers educational programs in the following areas:\n\n**Bachelor\'s degree (4 years):**\n• Information Technology\n• Economics and Business\n• Pedagogical Sciences\n• Law\n• Medicine\n• Engineering\n\n**Master\'s degree (2 years):**\n• MBA programs\n• Specialized master\'s programs\n\n**Doctoral studies (3 years):**\n• PhD programs in all areas\n\nEducation is conducted in Kazakh, Russian and English.',
            'keywords': 'программы, бакалавриат, магистратура, специальности',
            'category': 'Обучение',
            'tags': 'программы,обучение,специальности',
            'priority': 1,
            'is_featured': True
        },
        
        # Student Life Agent Knowledge
        {
            'agent_type': 'student_life',
            'title': 'Общежитие университета',
            'content_ru': 'Университет "Болашак" предоставляет студентам современное общежитие:\n\n**Условия проживания:**\n• 2-3 местные комнаты\n• Общие кухни на каждом этаже\n• Wi-Fi интернет\n• Прачечная и гладильная комнаты\n• Охрана 24/7\n\n**Стоимость:**\n• 15 000 тенге в месяц\n• Коммунальные услуги включены\n\n**Правила заселения:**\n• Приоритет для иногородних студентов\n• Подача заявления до 1 августа\n• Необходимы: справка о доходах семьи, медицинская справка\n\n**Адрес:** ул. Студенческая, 15, г. Кызылорда',
            'content_kz': '"Болашақ" университеті студенттерге заманауи жатақхана ұсынады:\n\n**Тұру жағдайлары:**\n• 2-3 орындық бөлмелер\n• Әр қабатта ортақ ас үйлер\n• Wi-Fi интернет\n• Кір жуу және үтіктеу бөлмелері\n• 24/7 күзет\n\n**Құны:**\n• Айына 15 000 теңге\n• Коммуналдық қызметтер кіреді\n\n**Орналасу ережелері:**\n• Басқа қалалардан келген студенттерге басымдық\n• 1 тамызға дейін өтініш беру\n• Қажет: отбасы табысы туралы анықтама, медициналық анықтама\n\n**Мекенжайы:** Студенттік к-сі, 15, Қызылорда қ.',
            'content_en': 'Bolashak University provides students with modern dormitory:\n\n**Living conditions:**\n• 2-3 bed rooms\n• Common kitchens on each floor\n• Wi-Fi internet\n• Laundry and ironing rooms\n• 24/7 security\n\n**Cost:**\n• 15,000 tenge per month\n• Utilities included\n\n**Settlement rules:**\n• Priority for non-local students\n• Application submission until August 1\n• Required: family income certificate, medical certificate\n\n**Address:** Studentskaya str., 15, Kyzylorda',
            'keywords': 'общежитие, проживание, стоимость, условия',
            'category': 'Проживание',
            'tags': 'общежитие,проживание,жилье',
            'priority': 1,
            'is_featured': True
        },
        
        # General Agent Knowledge
        {
            'agent_type': 'general',
            'title': 'Контактная информация',
            'content_ru': '**Университет "Болашак"**\n\n**Адрес:**\nг. Кызылорда, ул. Университетская, 1\nПочтовый индекс: 120000\n\n**Телефоны:**\n• Приёмная ректора: +7 (7242) 123-456\n• Приёмная комиссия: +7 (7242) 123-457\n• Деканаты: +7 (7242) 123-458\n• Общежитие: +7 (7242) 123-459\n\n**Email:**\n• info@bolashak.kz - общие вопросы\n• admission@bolashak.kz - поступление\n• student@bolashak.kz - для студентов\n\n**Часы работы:**\n• Понедельник-Пятница: 9:00-18:00\n• Суббота: 9:00-13:00\n• Воскресенье: выходной',
            'content_kz': '**"Болашақ" университеті**\n\n**Мекенжайы:**\nҚызылорда қ., Университетская к-сі, 1\nПошталық индекс: 120000\n\n**Телефондар:**\n• Ректор кеңсесі: +7 (7242) 123-456\n• Қабылдау комиссиясы: +7 (7242) 123-457\n• Деканаттар: +7 (7242) 123-458\n• Жатақхана: +7 (7242) 123-459\n\n**Email:**\n• info@bolashak.kz - жалпы сұрақтар\n• admission@bolashak.kz - түсу\n• student@bolashak.kz - студенттерге\n\n**Жұмыс уақыты:**\n• Дүйсенбі-Жұма: 9:00-18:00\n• Сенбі: 9:00-13:00\n• Жексенбі: демалыс',
            'content_en': '**Bolashak University**\n\n**Address:**\nKyzylorda, Universitetskaya str., 1\nPostal code: 120000\n\n**Phones:**\n• Rector\'s office: +7 (7242) 123-456\n• Admissions committee: +7 (7242) 123-457\n• Dean\'s offices: +7 (7242) 123-458\n• Dormitory: +7 (7242) 123-459\n\n**Email:**\n• info@bolashak.kz - general questions\n• admission@bolashak.kz - admission\n• student@bolashak.kz - for students\n\n**Working hours:**\n• Monday-Friday: 9:00-18:00\n• Saturday: 9:00-13:00\n• Sunday: day off',
            'keywords': 'контакты, телефон, адрес, email, часы работы',
            'category': 'Контакты',
            'tags': 'контакты,телефон,адрес',
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