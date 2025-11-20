from flask import Blueprint, jsonify, request
from data import (
    get_all_matches, 
    get_match_by_id, 
    add_match, 
    update_match, 
    delete_match, 
    get_statistics,
    patch_match
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
    """
    sort_field = request.args.get('sort')
    matches = get_all_matches(sort_field)
    return jsonify(matches)


@matches_bp.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """
    Получить матч по ID
    ---
    responses:
      200:
        description: Данные матча
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
    responses:
      201:
        description: Матч создан
      400:
        description: Ошибка данных
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
    Полностью обновить данные матча
    ---
    responses:
      200: Матч обновлен
      404: Матч не найден
    """
    data = request.get_json()
    updated_match = update_match(match_id, data)
    
    if updated_match:
        return jsonify(updated_match)
    return jsonify({"error": "Матч не найден"}), 404


@matches_bp.route('/matches/<int:match_id>', methods=['PATCH'])
def partially_modify_match(match_id):
    """
    Частичное обновление данных матча (PATCH)
    ---
    description: Обновляет только указанные поля.
    parameters:
      - in: path
        name: match_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          description: Поля для обновления
          example:
            spectators: 50000
            stadium: "Газпром Арена"
    responses:
      200:
        description: Частичное обновление успешно
      404:
        description: Матч не найден
    """
    fields = request.get_json()
    updated_match = patch_match(match_id, fields)

    if updated_match:
        return jsonify(updated_match)
    return jsonify({"error": "Матч не найден"}), 404


@matches_bp.route('/matches/<int:match_id>', methods=['DELETE'])
def remove_match(match_id):
    """
    Удалить матч
    ---
    responses:
      200: Матч удален
      404: Матч не найден
    """
    match = get_match_by_id(match_id)
    if match:
        delete_match(match_id)
        return jsonify({"message": "Матч удален"})
    return jsonify({"error": "Матч не найден"}), 404


@matches_bp.route('/matches/stats', methods=['GET'])
def get_matches_stats():
    """
    Получить статистику по числовым полям
    ---
    responses:
      200: Статистика
    """
    stats = get_statistics()
    return jsonify(stats)
