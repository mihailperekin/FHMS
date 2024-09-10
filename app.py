from flask import Flask,render_template,url_for,request,redirect,send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import pandas as pd
import sqlite3
import os
from io import BytesIO
from openpyxl import Workbook
import folium
from geopy.geocoders import Yandex
import json
import random


app = Flask(__name__,static_folder='templates\static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydrant.db'
app.config['TIME_ZONE'] = 'Europe/Moscow'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    vk = db.Column(db.Integer)
    pressure = db.Column(db.String)
    defects = db.Column(db.String)
    part = db.Column(db.String)
    responsible = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.now(pytz.timezone(app.config['TIME_ZONE'])))

    def __repr__(self):
        return '<Article %r>' % self.id 
    

map = folium.Map(location=[61.77816,34.36404],zoom_start=13)


def get_coordinates_by_address(address_for_coordinats):
    geolocator = Yandex(api_key='4156b60a-97bc-4285-84a3-9be6b876ce1b')
    location = geolocator.geocode(address_for_coordinats)
    if location:
        return (location.latitude, location.longitude)
    else:
        print("Адрес не найден.")
        return None


def load_markers():
    try:
        with open('instance/markers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
    
def save_markers(markers):
    with open('instance/markers.json', 'w') as f:
        json.dump(markers, f)


@app.route('/',methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        address = request.form['address']
        vk = request.form['vkNumber']
        pressure = request.form['pressure']
        defects = request.form['defects']
        part = request.form['part']
        responsible = request.form['responsible']
        article = Article(defects=defects,responsible=responsible,pressure=pressure,vk=vk,address=address,part=part)
        try:
            address_for_coordinats = address + ", Петрозаводск"
            if '-' in address_for_coordinats:
                address_for_coordinats = address_for_coordinats.replace('-',',')
            coordinates = get_coordinates_by_address(address_for_coordinats)
            latitude = coordinates[0]
            longitude = coordinates[1]
            

            markers = load_markers()
            for marker in markers:
                folium.Marker([marker['latitude'], marker['longitude']], popup=marker['title']).add_to(map)

            title = f"номер вк {vk}, давление: {pressure} деффекты: {defects}, ответственный: {responsible}"
            if defects!=' ':
                marker = folium.Marker([latitude, longitude], popup=title,collapsed = True)
            else:
                marker = folium.Marker([latitude, longitude], popup=title)
            marker.add_to(map)

            markers.append({'latitude': latitude, 'longitude': longitude, 'title': title})
            save_markers(markers)

            map.save('templates/map.html')


            db.session.add(article)
            db.session.commit()
            return redirect("/")
        except:
            return "Произощла ошибка,попробуйте еще раз"
    else:
        return render_template("index.html")


@app.route('/download_file')
def download_excel():
    conn = sqlite3.connect('instance\hydrant.db')
    df = pd.read_sql_query("SELECT * FROM article", conn)
    conn.close()
    workbook = Workbook()
    sheet = workbook.active
    for index, row in df.iterrows():
        row_list = [cell.tolist() if isinstance(cell, pd.Series) else cell for cell in row]
        sheet.append(row_list)
    excel_buffer = BytesIO()
    workbook.save(excel_buffer)
    excel_buffer.seek(0)
    temp_file_path = '/tmp/data.xlsx'
    if not os.path.exists('/tmp'):
        os.makedirs('/tmp')
    with open(temp_file_path, 'wb') as f:
        f.write(excel_buffer.getvalue())
    return send_from_directory('/tmp', 'data.xlsx', as_attachment=True)


@app.route('/map')
def maps():
    markers = load_markers()
    for marker in markers:
        folium.Marker([marker['latitude'], marker['longitude']], popup=marker['title']).add_to(map)
    map.save('templates/map.html')

    return render_template("map.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')