types_mapping = {
    "1": ("Нормальная ЭКГ"),
    "2": ("Вариант нормальной"),
    "3": ("Паталогическая"),
    "4": ("Неинтерпретируемая"),

    "11": ("Синусовая тахикардия"),
    "12": ("Синусовая брадикардия"),
    "13": ("Экстрасистолия"),
    "14": ("Синусовая аритмия"),
    "15": ("Трепетание предсердий"),
    "16": ("Фибрилляция предсердий"),
    "17": ("Трепетание и фибрилляция желудочков"),

    "21": ("Атриовентрикулярная блокада I"),
    "22": ("Атриовентрикулярная блокада II"),
    "23": ("Атриовентрикулярная блокада III"),
    "24": ("(БЛНПГ)Блокада левой ножки пучка Гиса"),
    "25": ("(НБЛНПГ)Неполная блокада левой ножки пучка Гиса"),
    "26": ("(ПБПНПГ)Полная блокада правой ножки пучка Гиса"),
    "27": ("(НБПНПГ)Неполная блокада правой ножки пучка Гиса"),

    "31": ("Гипертрофия левого желудочка"),
    "32": ("Гипертрофия правого желудочка"),
    "33": ("Гипертрофия левого предсердия"),
    "34": ("Гипертрофия правого предсердия"),
    "35": ("Ишемия миокарда"),
    "36": ("Инфаркт миокарда"),
    "37": ("Кардиостимулятор")
}

default_data = [
    {'group_label': "Общее",
     'group_data': [{"view": "checkbox", "label": "Нормальная ЭКГ", "value": 0, "name": "1"},
                    {"view": "checkbox", "label": "Вариант нормальной", "value": 0, "name": "2"},
                    {"view": "checkbox", "label": "Паталогическая", "value": 0, "name": "3"},
                    {"view": "checkbox", "label": "Неинтерпретируемая", "value": 0, "name": "4"},
                    ]},
    {'group_label': "Ритм",
     'group_data': [{"view": "checkbox", "label": "Синусовая тихикардия", "value": 0, "name": "11"},
                    {"view": "checkbox", "label": "Синусовая брадикардия", "value": 0, "name": "12"},
                    {"view": "checkbox", "label": "Экстрасистолия", "value": 0, "name": "13"},
                    {"view": "checkbox", "label": "Синусовая аритмия", "value": 0, "name": "14"},
                    {"view": "checkbox", "label": "Трепетание предсердий", "value": 0, "name": "15"},
                    {"view": "checkbox", "label": "Фибрилляция предсердий", "value": 0, "name": "16"},
                    {"view": "checkbox", "label": "Трепетание и фибрилляция желудочков", "value": 0, "name": "17"}

                    ]},
    {'group_label': "Нарушения функции проводимости",
     'group_data': [{"view": "checkbox", "label": "Атриовентрикулярная блокада I", "value": 0, "name": "21"},
                    {"view": "checkbox", "label": "Атриовентрикулярная блокада II", "value": 0, "name": "22"},
                    {"view": "checkbox", "label": "Атриовентрикулярная блокада III", "value": 0, "name": "23"},
                    {"view": "checkbox", "label": "(БЛНПГ)Блокада левой ножки пучка Гиса", "value": 0, "name": "24"},
                    {"view": "checkbox", "label": "(НБЛНПГ)Неполная блокада левой ножки пучка Гиса", "value": 0,
                     "name": "25"},
                    {"view": "checkbox", "label": "(ПБПНПГ)Полная блокада правой ножки пучка Гиса", "value": 0,
                     "name": "26"},
                    {"view": "checkbox", "label": "(НБПНПГ)Неполная блокада правой ножки пучка Гиса", "value": 0,
                     "name": "27"}
                    ]},
    {'group_label': "Другие Показатели",
     'group_data': [{"view": "checkbox", "label": "Гипертрофия левого желудочка", "value": 0, "name": "31"},
                    {"view": "checkbox", "label": "Гипертрофия правого желудочка", "value": 0, "name": "32"},
                    {"view": "checkbox", "label": "Гипертрофия левого предсердия", "value": 0, "name": "33"},
                    {"view": "checkbox", "label": "Гипертрофия правого предсердия", "value": 0, "name": "34"},
                    {"view": "checkbox", "label": "Ишемия миокарда", "value": 0, "name": "35"},
                    {"view": "checkbox", "label": "Инфаркт миокарда", "value": 0, "name": "36"},
                    {"view": "checkbox", "label": "Кардиостимулятор", "value": 0, "name": "37"},
                    ]}

]
