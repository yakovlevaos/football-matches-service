from flask import Flask, jsonify
from flasgger import Swagger
from api.matches import matches_bp

# Инициализация Flask приложения
app = Flask(__name__)

# Упрощенная конфигурация Swagger
app.config['SWAGGER'] = {
    'title': 'Football Matches API',
    'uiversion': 3,
    'specs_route': '/apidocs/',
    'specs': [
        {
            'endpoint': 'apispec',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }
    ]
}

# Регистрируем Blueprint ДО инициализации Swagger
app.register_blueprint(matches_bp)

# Инициализация Swagger после регистрации всех Blueprint
swagger = Swagger(app)

@app.route('/')
def index():
    """
    Главная страница API
    ---
    responses:
      200:
        description: Информация о сервисе
        schema:
          type: object
          properties:
            service:
              type: string
            version:
              type: string
            description:
              type: string
        examples:
          application/json:
            service: "Football Matches API"
            version: "2.0"
            description: "Веб-сервис для управления футбольными матчами"
    """
    return jsonify({
        "service": "Football Matches API",
        "version": "2.0",
        "description": "Веб-сервис для управления футбольными матчами",
        "endpoints": {
            "matches": "/api/matches",
            "statistics": "/api/matches/stats",
            "documentation": "/apidocs"
        }
    })

@app.route('/info/<about>/')
def info(about):
    """
    Информация о сервисе
    ---
    parameters:
      - name: about
        in: path
        type: string
        enum: ['all', 'version', 'author', 'year']
        required: true
        default: all
    responses:
      200:
        description: Информация о сервисе
        schema:
          type: object
        examples:
          application/json:
            version: "2.0"
    """
    all_info = {
        'all': {
            'author': 'Студент',
            'version': '2.0', 
            'year': '2024',
            'description': 'Веб-сервис для футбольных матчей'
        },
        'version': '2.0',
        'author': 'Студент',
        'year': '2024'
    }
    
    if about in all_info:
        result = {about: all_info[about]}
    else:
        result = {'error': 'Информация не найдена'}
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)