import urllib.request
import json
import re
from datetime import datetime

GROUPS = ["152","153","154","155","252","253","254","255","343","344",
          "352","353","354","355","454","455","512","513","514","515",
          "552","553","554","555","652","653","655","754","755","812",
          "813","814","815","852","853","854","855","952","953","954","955"]

# Соответствие групп и страниц
PAGES = {
    "455": "16", "152": "1", "153": "2", "154": "3", "155": "4",
    "252": "5", "253": "6", "254": "7", "255": "8", "343": "9",
    "344": "10", "352": "11", "353": "12", "354": "13", "355": "14",
    "454": "15", "512": "17", "513": "18", "514": "19", "515": "20",
    "552": "21", "553": "22", "554": "23", "555": "24", "652": "25",
    "653": "26", "655": "27", "754": "28", "755": "29", "812": "30",
    "813": "31", "814": "32", "815": "33", "852": "34", "853": "35",
    "854": "36", "855": "37", "952": "38", "953": "39", "954": "40", "955": "41",
}

def parse_schedule(group, page):
    url = f"https://ytk-edu.ru/newrasp/cg{page}.htm"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            html = response.read().decode('utf-8')
    except:
        return None
    
    days = []
    rows = re.findall(r'<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', html, re.DOTALL)
    
    current_day = None
    for first, second in rows:
        first = re.sub('<[^<]+?>', '', first).strip()
        second = re.sub('<[^<]+?>', '', second).strip()
        
        if re.search(r'\d{2}\.\d{2}\.\d{4}', first):
            if current_day:
                days.append(current_day)
            current_day = {'date': first, 'pairs': []}
            if second and 'Пара' not in second and len(second) > 2:
                current_day['pairs'].append({'num': '1', 'subject': second})
        elif current_day and re.match(r'^\d+$', first) and second:
            current_day['pairs'].append({'num': first, 'subject': second})
    
    if current_day:
        days.append(current_day)
    
    return days

def main():
    all_data = {}
    for group in GROUPS:
        page = PAGES.get(group)
        if page:
            schedule = parse_schedule(group, page)
            if schedule:
                all_data[group] = schedule
                print(f"✓ {group}")
            else:
                print(f"✗ {group}")
    
    with open('data/schedule.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"Сохранено {len(all_data)} групп")

if __name__ == '__main__':
    main()
