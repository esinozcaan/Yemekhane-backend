import json


def calculate_result(result_dict: dict, food_items: list, menu: dict) -> dict:
    calories, price, result_expanded = summary(result_dict, food_items)


def summary(result, index) -> int:
    total_calories = 0
    total_price = 0
    result_expanded = []
    for i in result:
        for j in index:
            if i == j["name"]:
                total_calories += j["calories"]
                total_price += j["price"]
                current_result = {
                    "name": j["name"],
                    "calories": j["calories"],
                    "price": j["price"],
                    "count": result[i],
                    "category": j["category"],
                    "type": j["type"],
                }
                result_expanded.append(current_result)
                
    return (total_calories, total_price, result_expanded)


def detect_menu(result_expanded, menu):
    pass