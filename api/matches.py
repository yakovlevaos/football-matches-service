from flask import Blueprint, jsonify, request
from data import (
    get_all_matches, 
    get_match_by_id, 
    add_match, 
    update_match, 
    delete_match, 
    get_statistics,
    partial_update_match
)

# Создаем Blueprint для матчей
matches_bp = Blueprint('matches', __name__, url_prefix='/api')


@matches_bp.route('/matches', methods=['GET'])
def get_matches():
    """
    Получить список всех футбольных матчей
    ---
    parameters:
      - name: sort
        in: query
        type: string
        enum: ['id', 'home_team', 'away_team', 'home_score', 'away_score', 'date', 'spectators', 'stadium', 'tournament']
        required: false
        description: Поле для сортировки
    responses:
      200:
        description: Список матчей
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              home_team:
                type: string
                example: "Спартак"
              away_team:
                type: string
                example: "Зенит"
              home_score:
                type: integer
                example: 2
              away_score:
                type: integer
                example: 1
              date:
                type: string
                example: "2024-05-15"
              spectators:
                type: integer
                example: 45000
              stadium:
                type: string
                example: "Открытие Арена"
              tournament:
                type: string
                example: "Премьер-Лига"
    """
    sort_field = request.args.get('sort')
    matches = get_all_matches(sort_field)
    return jsonify(matches)


@matches_bp.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """
    Получить матч по ID
    ---
    parameters:
      - name: match_id
        in: path
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Данные матча
        schema:
          type: object
          properties:
            id:
              type: integer
            home_team:
              type: string
            away_team:
              type: string
            home_score:
              type: integer
            away_score:
              type: integer
            date:
              type: string
            spectators:
              type: integer
            stadium:
              type: string
            tournament:
              type: string
      404:
        description: Матч не найден
    """
    match = get_match_by_id(match_id)
    if match:
        return jsonify(match)
    return jsonify({"error": "Матч не найден"}), 404


@matches_bp.route('/matches', methods=['POST'])
def create_match():
    """
    Добавить новый матч
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - home_team
            - away_team
            - home_score
            - away_score
            - date
            - spectators
            - stadium
            - tournament
          properties:
            home_team:
              type: string
              example: "Динамо"
            away_team:
              type: string
              example: "Рубин"
            home_score:
              type: integer
              example: 1
            away_score:
              type: integer
              example: 1
            date:
              type: string
              example: "2024-05-16"
            spectators:
              type: integer
              example: 15000
            stadium:
              type: string
              example: "ВТБ Арена"
            tournament:
              type: string
              example: "Премьер-Лига"
    responses:
      201:
        description: Матч успешно создан
      400:
        description: Неверные данные
    """
    data = request.get_json()
    
    required_fields = ['home_team', 'away_team', 'home_score', 'away_score', 
                      'date', 'spectators', 'stadium', 'tournament']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400
    
    new_match = add_match(data)
    return jsonify(new_match), 201


@matches_bp.route('/matches/<int:match_id>', methods=['PUT'])
def modify_match(match_id):
    """
    Обновить данные матча
    ---
    parameters:
      - name: match_id
        in: path
        type: integer
        required: true
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            home_team:
              type: string
            away_team:
              type: string
            home_score:
              type: integer
            away_score:
              type: integer
            date:
              type: string
            spectators:
              type: integer
            stadium:
              type: string
            tournament:
              type: string
    responses:
      200:
        description: Матч обновлен
      404:
        description: Матч не найден
    """
    data = request.get_json()
    updated_match = update_match(match_id, data)
    
    if updated_match:
        return jsonify(updated_match)
    return jsonify({"error": "Матч не найден"}), 404



@matches_bp.route('/matches/<int:match_id>', methods=['PATCH'])
def patch_match(match_id):
    """
    Частичное обновление матча
    ---
    parameters:
      - name: match_id
        in: path
        type: integer
        required: true
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          example: {
            "home_score": 3,
            "away_score": 2,
            "spectators": 50000
          }
          properties:
            home_team:
              type: string
            away_team:
              type: string
            home_score:
              type: integer
            away_score:
              type: integer
            date:
              type: string
            spectators:
              type: integer
            stadium:
              type: string
            tournament:
              type: string
    responses:
      200:
        description: Матч обновлен
        schema:
          type: object
          properties:
            id:
              type: integer
            home_team:
              type: string
            away_team:
              type: string
            home_score:
              type: integer
            away_score:
              type: integer
            date:
              type: string
            spectators:
              type: integer
            stadium:
              type: string
            tournament:
              type: string
      400:
        description: Неверные данные
      404:
        description: Матч не найден
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Нет данных для обновления"}), 400
    
    existing_match = get_match_by_id(match_id)
    if not existing_match:
        return jsonify({"error": "Матч не найден"}), 404
    
    valid_fields = ['home_team', 'away_team', 'home_score', 'away_score', 
                   'date', 'spectators', 'stadium', 'tournament']
    
    update_data = {}
    for key, value in data.items():
        if key in valid_fields:
            update_data[key] = value
    
    if not update_data:
        return jsonify({"error": "Нет валидных полей для обновления"}), 400
    
    updated_match = partial_update_match(match_id, update_data)
    
    if updated_match:
        return jsonify(updated_match)
    return jsonify({"error": "Ошибка при обновлении матча"}), 500
  
@matches_bp.route('/matches/<int:match_id>', methods=['DELETE'])
def remove_match(match_id):
    """
    Удалить матч
    ---
    parameters:
      - name: match_id
        in: path
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Матч удален
      404:
        description: Матч не найден
    """
    match = get_match_by_id(match_id)
    if match:
        delete_match(match_id)
        return jsonify({"message": "Матч удален"})
    return jsonify({"error": "Матч не найден"}), 404


@matches_bp.route('/matches/stats', methods=['GET'])
def get_matches_stats():
    """
    Получить статистику по матчам
    ---
    responses:
      200:
        description: Статистика по числовым полям
        schema:
          type: object
          properties:
            home_score:
              type: object
              properties:
                min:
                  type: integer
                max:
                  type: integer
                average:
                  type: number
                sum:
                  type: integer
            away_score:
              type: object
              properties:
                min:
                  type: integer
                max:
                  type: integer
                average:
                  type: number
                sum:
                  type: integer
            spectators:
              type: object
              properties:
                min:
                  type: integer
                max:
                  type: integer
                average:
                  type: number
                sum:
                  type: integer
    """
    stats = get_statistics()
    return jsonify(stats)
