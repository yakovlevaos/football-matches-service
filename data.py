"""
Модуль для работы с данными футбольных матчей
Содержит функции для CRUD операций и статистики
"""

# Начальные данные для демонстрации
matches = [
    {
        "id": 1,
        "home_team": "Спартак",
        "away_team": "Зенит", 
        "home_score": 2,
        "away_score": 1,
        "date": "2024-05-15",
        "spectators": 45000,
        "stadium": "Открытие Арена",
        "tournament": "Премьер-Лига"
    },
    {
        "id": 2,
        "home_team": "ЦСКА",
        "away_team": "Локомотив",
        "home_score": 0,
        "away_score": 0,
        "date": "2024-05-14",
        "spectators": 28000,
        "stadium": "ВЭБ Арена",
        "tournament": "Премьер-Лига"
    },
    {
        "id": 3,
        "home_team": "Краснодар",
        "away_team": "Ростов",
        "home_score": 3,
        "away_score": 2,
        "date": "2024-05-13",
        "spectators": 25000,
        "stadium": "Стадион Краснодар",
        "tournament": "Премьер-Лига"
    }
]

def get_all_matches(sort_by=None):
    """Получить все матчи с возможностью сортировки"""
    if sort_by and sort_by in matches[0].keys():
        return sorted(matches, key=lambda x: x[sort_by])
    return matches

def get_match_by_id(match_id):
    """Найти матч по ID"""
    for match in matches:
        if match["id"] == match_id:
            return match
    return None

def add_match(match_data):
    """Добавить новый матч"""
    new_id = max(match["id"] for match in matches) + 1
    match_data["id"] = new_id
    matches.append(match_data)
    return match_data

def update_match(match_id, match_data):
    """Обновить матч"""
    for i, match in enumerate(matches):
        if match["id"] == match_id:
            match_data["id"] = match_id
            matches[i] = match_data
            return match_data
    return None

def delete_match(match_id):
    """Удалить матч"""
    global matches
    matches = [match for match in matches if match["id"] != match_id]
    return True

def get_statistics():
    """Получить статистику по числовым полям"""
    numeric_fields = ["home_score", "away_score", "spectators"]
    stats = {}
    
    for field in numeric_fields:
        values = [match[field] for match in matches]
        stats[field] = {
            "min": min(values),
            "max": max(values),
            "average": round(sum(values) / len(values), 2),
            "sum": sum(values)
        }
    
    return stats