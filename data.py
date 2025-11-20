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

def get_all_matches(sort_field=None):
    if sort_field:
        return sorted(matches, key=lambda x: x.get(sort_field))
    return matches

def get_match_by_id(match_id):
    return next((m for m in matches if m['id'] == match_id), None)

def add_match(data):
    new_id = max(m['id'] for m in matches) + 1 if matches else 1
    data['id'] = new_id
    matches.append(data)
    return data

def update_match(match_id, data):
    match = get_match_by_id(match_id)
    if match:
        index = matches.index(match)
        matches[index] = data
        return matches[index]
    return None

def partial_update_match(match_id, fields):
    match = get_match_by_id(match_id)
    if not match:
        return None
    for key, value in fields.items():
        if key in match:
            match[key] = value
    return update_match(match_id, match)

def delete_match(match_id):
    match = get_match_by_id(match_id)
    if match:
        matches.remove(match)
        return True
    return False

def get_statistics():
    if not matches:
        return {}
    stats = {}
    num_fields = ['home_score', 'away_score', 'spectators']
    for field in num_fields:
        values = [m[field] for m in matches if field in m]
        stats[field] = {
            'min': min(values),
            'max': max(values),
            'average': sum(values) / len(values),
            'sum': sum(values)
        }
    return stats