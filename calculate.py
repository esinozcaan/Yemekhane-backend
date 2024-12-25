import json
from model import Menu, Items

menu_list = {
    "fix_menü": {
        "description": "1 Ana Yemek, 3 Yan Yemek",
        "items": {
            "ana_yemek": 1,
            "yardimci_yemek": 3,
            "etli_yemek": 0,
            "etsiz_yemek": 0,
        },
        "price": 132,
    },
    "menü_1": {
        "description": "1 Etli Yemek, 1 Yan Yemek",
        "items": {
            "etli_yemek": 1,
            "etsiz_yemek": 0,
            "yardimci_yemek": 1,
            "ana_yemek": 0,
        },
        "price": 106,
    },
    "menü_2": {
        "description": "1 Etsiz Yemek, 1 Yan Yemek",
        "items": {
            "etsiz_yemek": 1,
            "yardimci_yemek": 1,
            "etli_yemek": 0,
            "ana_yemek": 0,
        },
        "price": 73,
    },
    "menü_3": {
        "description": "1 Etsiz Yemek",
        "items": {
            "etsiz_yemek": 1,
            "yardimci_yemek": 0,
            "etli_yemek": 0,
            "ana_yemek": 0,
        },
        "price": 53,
    },
}


def calculate_result(
    result_dict: dict, food_items: list
) -> tuple[Items, Menu | None, int, float]:
    total_calories, total_price, result_expanded = summary(result_dict, food_items)

    detected_menu = detect_menu(result_expanded, menu_list)
    savings = 0
    savings_percent = 0
    if detected_menu:
        savings = total_price - detected_menu.price
        savings_percent = (savings / total_price) * 100

    detected_items = Items(
        total_calories=total_calories, 
        total_price=total_price, 
        result=result_expanded
    )
    return (
        detected_items,
        detected_menu,
        savings,
        savings_percent,
    )


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


def detect_menu(result_expanded, menu) -> Menu | None:
    ana_yemek_count = 0
    yardimci_yemek_count = 0
    etli_yemek_count = 0
    etsiz_yemek_count = 0

    for item in result_expanded:
        if item["category"] == "ana_yemek":
            ana_yemek_count += item["count"]
        elif item["category"] == "yardimci_yemek":
            yardimci_yemek_count += item["count"]
        elif item["type"] == "etli_yemek":
            etli_yemek_count += item["count"]
        elif item["type"] == "etsiz_yemek":
            etsiz_yemek_count += item["count"]

    for menu_name in menu:
        if (
            ana_yemek_count == menu[menu_name]["items"]["ana_yemek"]
            and yardimci_yemek_count == menu[menu_name]["items"]["yardimci_yemek"]
            and etli_yemek_count == menu[menu_name]["items"]["etli_yemek"]
            and etsiz_yemek_count == menu[menu_name]["items"]["etsiz_yemek"]
        ):
            return Menu(
                name=menu_name,
                description=menu[menu_name]["description"],
                price=menu[menu_name]["price"],
            )

    return None
