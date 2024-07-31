import csv
import json
from datetime import datetime

def parse_csv_data(csv_file_path):
    results = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        current_data = {}

        for row in reader:
            if row and row[0] != '':
                if 'Сред.значение:' in row[0]:
                    date_str = current_data.get('data')
                    if date_str:
                        date_str = datetime.strptime(date_str, "%d.%m.%Y")
                        date_str = date_str.strftime("%d.%m.%Y")
                        current_data['data'] = date_str
                    for i, name in enumerate(current_data['names']):
                        current_data[name].append(float(row[i+1].replace(',', '.')))
                    results.append(current_data)
                    current_data = {}
                elif current_data.get('data') is None:
                    current_data['data'] = row[0]
                    current_data['names'] = row[1:]
                    for name in current_data['names']:
                        current_data[name] = []
                else:
                    continue
    return results

# def save_to_json(data, output_file_path):
#     with open(output_file_path, 'w', encoding='utf-8') as json_file:
#         json.dump(data, json_file, ensure_ascii=False, indent=4)

# Пример использования:
# csv_file_path = 'MyGroups/NewSystem.csv'
# # json_file_path = 'MyGroups/NewSystem.json'
#
# parsed_data = parse_csv_data(csv_file_path)
# print(type(parsed_data))
# save_to_json(parsed_data, json_file_path)

# print(f'Data has been successfully saved to {json_file_path}')
