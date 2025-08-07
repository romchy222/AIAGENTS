# Импорт необходимых модулей
import time
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, Response
import requests
import base64
from sqlalchemy import func, desc
from datetime import datetime, timedelta


# Настройка логирования
logger = logging.getLogger(__name__)

# Создание Blueprint для основных маршрутов
main_bp = Blueprint('views', __name__)

# Инициализация роутера агентов (выполним позже, чтобы избежать circular import)
agent_router = None

def initialize_agent_router():
    """Initialize agent router after app context is available"""
    global agent_router
    if agent_router is None:
        from agents import AgentRouter
        agent_router = AgentRouter()
    return agent_router


@main_bp.route('/')
def index_new():
    """New main page with chat widget"""
    return render_template('index_new.html')

@main_bp.route('/index')
def index():
    """Old main page redirect"""
    return render_template('index_new.html')

@main_bp.route('/chat')
def chat_new():
    """New chat page"""
    return render_template('chat_new.html')

@main_bp.route('/chat-old')
def chat_page():
    """Old chat page"""
    return render_template('chat.html')

@main_bp.route('/set-language/<language>')
def set_language(language):
    """Set user language"""
    from flask import session, redirect, url_for, request
    if language in ['ru', 'kz', 'en']:
        session['language'] = language
    return redirect(request.referrer or url_for('views.index_new'))


@main_bp.route('/widget-demo')
def widget_demo():
    """Widget integration demo page"""
    return render_template('widget-demo.html')


@main_bp.route('/api/chat', methods=['POST'])
@main_bp.route('/chat', methods=['POST'])
def chat():
    try:
        from models import UserQuery
        from app import db
        from flask import current_app

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'success': False, 'error': 'Сообщение не найдено'}), 400

        user_message = data['message'].strip()
        language = data.get('language', 'ru')
        agent_type = data.get('agent')  # Updated parameter name

        if not user_message:
            return jsonify({'success': False, 'error': 'Пустое сообщение'}), 400

        start_time = time.time()

        # Initialize router within app context
        router = initialize_agent_router()

        if agent_type and agent_type != 'auto':
            # Find agent with required type
            for agent in router.agents:
                if getattr(agent, "agent_type", None) and (agent.agent_type == agent_type):
                    result = agent.process_message(user_message, language)
                    result['agent_type'] = agent.agent_type
                    result['agent_name'] = agent.name
                    result['confidence'] = 1.0
                    break
            else:
                # Если не найден — fallback на авто-выбор
                result = router.route_message(user_message, language)
        else:
            # Автоматический выбор агента
            result = router.route_message(user_message, language)

        response_time = time.time() - start_time

        # Create UserQuery within app context
        user_query = UserQuery(
            user_message=user_message,
            bot_response=result['response'],
            language=language,
            response_time=response_time,
            agent_type=result.get('agent_type'),
            agent_name=result.get('agent_name'),
            agent_confidence=result.get('confidence', 0.0),
            context_used=result.get('context_used', False),
            session_id=session.get('session_id', ''),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )

        try:
            db.session.add(user_query)
            db.session.commit()
        except Exception as db_error:
            logger.warning(f"Database error (continuing without saving): {str(db_error)}")
            # Continue without saving to database

        logger.info(
            f"Chat response generated in {response_time:.2f}s "
            f"by {result.get('agent_name', 'Unknown')} agent "
            f"(confidence: {result.get('confidence', 0):.2f}) "
            f"for language: {language}"
        )

        return jsonify({
            'success': True,
            'response': result['response'],
            'response_time': response_time,
            'agent_name': result.get('agent_name'),
            'agent_type': result.get('agent_type'),
            'confidence': result.get('confidence', 0.0),
            'query_id': getattr(user_query, 'id', None)  # Include query ID for rating functionality
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        # Use a default language if language is not defined
        lang = locals().get('language', 'ru')
        error_message = "Извините, произошла ошибка. Попробуйте еще раз." if lang == 'ru' else "Кешіріңіз, қате орын алды. Қайталап көріңіз."
        return jsonify({'success': False, 'error': error_message}), 500

@main_bp.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': time.time()})


@main_bp.route('/api/agents')
def get_agents():
    """Get information about available agents"""
    try:
        router = initialize_agent_router()
        agents_info = router.get_available_agents()
        return jsonify({
            'agents': agents_info,
            'total_agents': len(agents_info)
        })
    except Exception as e:
        logger.error(f"Error getting agents info: {str(e)}")
        return jsonify({'error': 'Failed to get agents information'}), 500


@main_bp.route('/api/rate/<int:query_id>', methods=['POST'])
def rate_response(query_id):
    """Rate a bot response with like/dislike"""
    try:
        from models import UserQuery
        from app import db

        data = request.get_json()
        if not data or 'rating' not in data:
            return jsonify({'error': 'Rating not provided'}), 400

        rating = data['rating']
        if rating not in ['like', 'dislike']:
            return jsonify({'error': 'Invalid rating. Must be "like" or "dislike"'}), 400

        # Find the query
        query = UserQuery.query.get(query_id)
        if not query:
            return jsonify({'error': 'Query not found'}), 404

        # Update rating
        query.user_rating = rating
        query.rating_timestamp = datetime.utcnow()

        try:
            db.session.commit()
            logger.info(f"Query {query_id} rated as {rating}")
            return jsonify({
                'success': True,
                'rating': rating,
                'query_id': query_id
            })
        except Exception as db_error:
            logger.error(f"Database error saving rating: {str(db_error)}")
            return jsonify({'error': 'Failed to save rating'}), 500

    except Exception as e:
        logger.error(f"Error rating response: {str(e)}")
        return jsonify({'error': 'Failed to rate response'}), 500


# Voice chat endpoints
@main_bp.route('/api/voice/start-session', methods=['POST'])
def start_voice_session():
    """Start a new voice chat session"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        language = data.get('language', 'ru')

        # Generate session ID
        import uuid
        session_id = str(uuid.uuid4())

        # Store session info (could be in database in production)
        session['voice_session_id'] = session_id
        session['voice_language'] = language
        session['voice_user_id'] = user_id

        logger.info(f"Started voice session {session_id} for user {user_id}")

        return jsonify({
            'session_id': session_id,
            'status': 'active',
            'language': language
        })

    except Exception as e:
        logger.error(f"Error starting voice session: {str(e)}")
        return jsonify({'error': 'Failed to start voice session'}), 500


@main_bp.route('/api/voice/process', methods=['POST'])
def process_voice_message():
    """Process voice message (placeholder for actual speech-to-text integration)"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        text_message = data.get('text')  # In real implementation, this would be audio data

        if not session_id or session_id != session.get('voice_session_id'):
            return jsonify({'error': 'Invalid session'}), 401

        if not text_message:
            return jsonify({'error': 'No message provided'}), 400

        # Use existing chat processing
        language = session.get('voice_language', 'ru')

        # Process through existing chat system
        router = initialize_agent_router()
        result = router.route_message(text_message, language)

        # Log the voice interaction
        from models import UserQuery
        from app import db

        user_query = UserQuery(
            user_message=text_message,
            bot_response=result['response'],
            language=language,
            agent_type=result.get('agent_type'),
            agent_name=result.get('agent_name'),
            agent_confidence=result.get('confidence', 0.0),
            session_id=session_id,
            ip_address=request.remote_addr,
            user_agent='Voice Chat API'
        )

        try:
            db.session.add(user_query)
            db.session.commit()
            query_id = user_query.id
        except Exception:
            query_id = None

        return jsonify({
            'response': result['response'],
            'agent_name': result.get('agent_name'),
            'query_id': query_id,
            'session_id': session_id
        })

    except Exception as e:
        logger.error(f"Error processing voice message: {str(e)}")
        return jsonify({'error': 'Failed to process voice message'}), 500


@main_bp.route('/api/tts', methods=['POST'])
def tts_proxy():
    """
    Free TTS endpoint using browser's native speech synthesis
    Returns instructions for client-side TTS instead of server-side processing
    """
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        speaker = data.get('speaker', 'default')
        lang = data.get('lang', 'ru')
        speed = data.get('speed', 1.0)
        emotion = data.get('emotion', 'neutral')

        # Instead of server-side TTS, return configuration for client-side Web Speech API
        tts_config = {
            'text': text,
            'lang': 'ru-RU' if lang == 'ru' else 'en-US',
            'rate': float(speed),
            'pitch': 1.0,
            'volume': 1.0,
            'voice_preference': speaker,
            'use_browser_tts': True
        }

        logger.info(f"TTS config generated for text: {text[:50]}... (lang: {lang}, speed: {speed})")

        return jsonify({
            'success': True,
            'config': tts_config,
            'message': 'Use browser TTS with provided config'
        })

    except Exception as e:
        logger.error(f"TTS config error: {str(e)}")
        return jsonify({'error': 'Failed to generate TTS config'}), 500


@main_bp.route('/api/deployment-readiness')
def deployment_readiness():
    """
    Comprehensive deployment readiness check
    Комплексная проверка готовности к деплою
    """
    try:
        from app import db
        from flask import current_app
        import os
        import sys

        # Инициализация результата проверки
        checks = {
            'database': {'status': 'unknown', 'message': ''},
            'agents': {'status': 'unknown', 'message': ''},
            'environment': {'status': 'unknown', 'message': ''},
            'dependencies': {'status': 'unknown', 'message': ''},
            'configuration': {'status': 'unknown', 'message': ''}
        }

        overall_status = 'healthy'

        # 1. Проверка базы данных
        try:
            # Проверяем соединение с базой данных
            from sqlalchemy import text
            # Простая проверка - создание таблиц
            db.create_all()
            checks['database']['status'] = 'healthy'
            checks['database']['message'] = 'База данных доступна и отвечает'
        except Exception as e:
            checks['database']['status'] = 'error'
            checks['database']['message'] = f'Ошибка подключения к БД: {str(e)}'
            overall_status = 'error'

        # 2. Проверка агентов
        try:
            router = initialize_agent_router()
            agents = router.get_available_agents()
            if len(agents) > 0:
                checks['agents']['status'] = 'healthy'
                checks['agents']['message'] = f'Доступно агентов: {len(agents)}'
            else:
                checks['agents']['status'] = 'warning'
                checks['agents']['message'] = 'Агенты не настроены'
                if overall_status != 'error':
                    overall_status = 'warning'
        except Exception as e:
            checks['agents']['status'] = 'error'
            checks['agents']['message'] = f'Ошибка инициализации агентов: {str(e)}'
            overall_status = 'error'

        # 3. Проверка переменных окружения
        required_env = ['DATABASE_URL', 'SESSION_SECRET']
        env_issues = []
        for env_var in required_env:
            if not os.environ.get(env_var):
                env_issues.append(env_var)

        if env_issues:
            checks['environment']['status'] = 'warning'
            checks['environment']['message'] = f'Отсутствуют переменные: {", ".join(env_issues)}'
            if overall_status == 'healthy':
                overall_status = 'warning'
        else:
            checks['environment']['status'] = 'healthy'
            checks['environment']['message'] = 'Все необходимые переменные окружения настроены'

        # 4. Проверка зависимостей
        try:
            import flask, sqlalchemy, gunicorn, requests
            checks['dependencies']['status'] = 'healthy'
            checks['dependencies']['message'] = f'Python {sys.version.split()[0]}, Flask {getattr(flask, "__version__", "unknown")}'
        except ImportError as e:
            checks['dependencies']['status'] = 'error'
            checks['dependencies']['message'] = f'Отсутствуют зависимости: {str(e)}'
            overall_status = 'error'

        # 5. Проверка конфигурации
        config_issues = []

        # Проверяем настройки безопасности для продакшена
        if current_app.debug and os.environ.get('FLASK_ENV') == 'production':
            config_issues.append('Debug режим включен в продакшене')

        # Проверяем секретный ключ
        if current_app.secret_key == 'dev-secret-key-change-in-production':
            config_issues.append('Используется тестовый секретный ключ')

        if config_issues:
            checks['configuration']['status'] = 'warning'
            checks['configuration']['message'] = '; '.join(config_issues)
            if overall_status == 'healthy':
                overall_status = 'warning'
        else:
            checks['configuration']['status'] = 'healthy'
            checks['configuration']['message'] = 'Конфигурация корректна'

        # Формирование итогового ответа
        result = {
            'overall_status': overall_status,
            'timestamp': time.time(),
            'checks': checks,
            'deployment_ready': overall_status != 'error',
            'recommendations': []
        }

        # Добавляем рекомендации
        if overall_status == 'error':
            result['recommendations'].append('Исправьте критические ошибки перед деплоем')
        elif overall_status == 'warning':
            result['recommendations'].append('Рекомендуется исправить предупреждения')
            result['recommendations'].append('Настройте переменные окружения для продакшена')
        else:
            result['recommendations'].append('Проект готов к деплою')
            result['recommendations'].append('Используйте Gunicorn для продакшена')
            result['recommendations'].append('Настройте PostgreSQL для продакшена')

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in deployment readiness check: {str(e)}")
        return jsonify({
            'overall_status': 'error',
            'error': f'Ошибка проверки готовности: {str(e)}',
            'deployment_ready': False
        }), 500