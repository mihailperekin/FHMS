import folium
import json

# Функция для загрузки меток из файла
def load_markers():
    try:
        with open('markers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Функция для сохранения меток в файл
def save_markers(markers):
    with open('markers.json', 'w') as f:
        json.dump(markers, f, indent=4)

# Создаем пустую карту
map = folium.Map(location=[51.505, -0.09], zoom_start=13)

# Загружаем метки из файла и добавляем их на карту
markers = load_markers()
for marker in markers:
    folium.Marker([marker['latitude'], marker['longitude']], popup=marker['title']).add_to(map)

# Функция для добавления метки
def add_marker():
    latitude = float(input("Введите широту: "))
    longitude = float(input("Введите долготу: "))
    title = input("Введите заголовок метки: ")
    
    # Добавляем новую метку в список
    markers.append({'latitude': latitude, 'longitude': longitude, 'title': title})
    
    # Создаем метку и добавляем ее на карту
    folium.Marker([latitude, longitude], popup=title).add_to(map)
    
    save_markers(markers)  # Сохраняем изменения в файл
    print(f"Метка '{title}' добавлена на координатах ({latitude}, {longitude})")

# Добавляем несколько меток
add_marker()

# Сохраняем карту в HTML файл
map.save('map.html')