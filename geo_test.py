from geopy.geocoders import Yandex

def get_coordinates_by_address(address):
    """
    Получает географические координаты по адресу на русском языке с помощью Яндекс.Геокодера.
    
    :param address: Адрес на русском языке
    :return: Тупл (широта, долгота)
    """
    geolocator = Yandex(api_key='4156b60a-97bc-4285-84a3-9be6b876ce1b')  # Замените на свой ключ API Яндекс.Геокодера
    location = geolocator.geocode(address)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        print("Адрес не найден.")
        return None

if __name__ == "__main__":
    address = input("Введите адрес на русском языке: ")
    coordinates = get_coordinates_by_address(address)
    
    if coordinates:
        print(coordinates)