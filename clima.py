import flet as ft
import requests
from flet import IconButton, Page, Row, TextField, Column, ElevatedButton, Container

# Chave da API do OpenWeatherMap
API_KEY = 'a5676ce9dbe81f9ddad2125c4dedb9b6'  # Coloque sua chave da API do OpenWeatherMap aqui

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança exceção se houver erro na requisição
        data = response.json()
        
        # Extrair informações relevantes
        weather_description = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        country = data['sys']['country']

        # Construir a string com as informações do clima
        weather_info = f'{weather_description}\n' \
                       f'Temperatura: {temp}°C\n' \
                       f'Umidade: {humidity}%\n' \
                       f'Velocidade do vento: {wind_speed} m/s\n' \
                       f'País: {country}'
        
        return weather_info
    except requests.exceptions.HTTPError as http_err:
        return f"Erro na requisição HTTP: {http_err}"
    except Exception as err:
        return f"Erro: {err}"

def main(page: ft.Page):
    page.title = "Clima App do Dundun"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
  

    txt_city = TextField(label="Cidade", hint_text="Digite sua cidade aqui", width=400, text_align="left")
    txt_weather = TextField(value="Informações do Clima irão aparecer aqui !\n\n\n\n", text_align="left", multiline=True, width=400, read_only=True)

    def update_weather(e):
        city = txt_city.value.strip()
        if city:
            weather = get_weather(city)
            txt_weather.value = weather
        else:
            txt_weather.value = "Digite o nome de uma cidade"
        page.update()

    def clear_weather(e):
        txt_city.value = ""
        txt_weather.value = "\n\n\n\n"
        page.update()

    def handle_enter(e):
        if e.key == "Enter":
            update_weather(None)

    page.add(
        Container(
            image_src='https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
            image_fit=ft.ImageFit.COVER,
            expand=True,
        ),
        Column(
            [
                txt_city,
                ElevatedButton(text="Buscar Clima", on_click=update_weather, width=400),
                txt_weather,
                ElevatedButton(text="Limpar", on_click=clear_weather, width=400)],
            horizontal_alignment="center",  # Centralizar os elementos horizontalmente

        )
    )

ft.app(target=main)
