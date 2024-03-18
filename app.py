from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        font_amiko_bold = 'assets/fonts/Amiko-Bold.ttf'
        font_amiko_regular = 'assets/fonts/Amiko-Regular.ttf'
        font_amiko_semibold = 'assets/fonts/Amiko-SemiBold.ttf'

        photo = request.files['photo']
        name = request.form['name']
        slogan = request.form['slogan']
        placeType = request.form['placeType']
        placeName = request.form['placeName']

        if photo is None or name is None or slogan is None or placeType is None or placeName is None:
            return jsonify({'error': 'Required form fields are missing.'}), 400

        # Afiş tipine göre görseli seç
        if placeType == 'akp':
            placeImage = 'afis_akp.jpeg'
            name_color = 'white'
            slogan_color = 'black'
            placeName_color = 'black'
            user_photo_resize = (327, 455)
            name_fontSize = 56
            slogan_fontSize = 32
            placeName_fontSize = 44
            name_position = (10, 562)
            slogan_position = (10, 490)
            placeName_position = (155, 660)
            user_photo_position = (20, 16)
        elif placeType == 'chp':
            placeImage = 'afis_chp.jpeg'
            name_color = 'red'
            slogan_color = 'black'
            placeName_color = 'white'
            user_photo_resize = (327, 455)
            name_fontSize = 56
            slogan_fontSize = 32
            placeName_fontSize = 40
            name_position = (10, 490)
            slogan_position = (10, 580)
            placeName_position = (190, 660)
            user_photo_position = (20, 16)
        elif placeType == 'mhp':
            placeImage = 'afis_mhp.jpeg'
            name_color = 'red'
            slogan_color = 'black'
            placeName_color = 'black'
            user_photo_resize = (300, 430)
            name_fontSize = 52
            slogan_fontSize = 20
            placeName_fontSize = 32
            name_position = (20, 100)
            slogan_position = (250, 300)
            placeName_position = (8, 2)
            user_photo_position = (2, 160)
        elif placeType == 'diger' or placeType == 'muhtar':
            placeImage = 'afis_diger.jpeg' if placeType == 'diger' else 'afis_muhtar.jpeg'
            name_color = 'red'
            slogan_color = 'black'
            placeName_color = 'white'
            user_photo_resize = (327, 455)
            name_fontSize = 56
            slogan_fontSize = 36
            placeName_fontSize = 56
            name_position = (390, 250)
            slogan_position = (390, 380)
            placeName_position = (380, 48)
            user_photo_position = (20, 16)

        # Afiş oluştur
        img = Image.open(os.path.join('assets', 'posters', placeImage))
        draw = ImageDraw.Draw(img)
        fontName = ImageFont.truetype(font_amiko_bold, name_fontSize)
        fontSlogan = ImageFont.truetype(font_amiko_regular, slogan_fontSize)
        fontPlaceName = ImageFont.truetype(font_amiko_bold, placeName_fontSize)

        # Fotoğrafı afişe ekle
        user_photo = Image.open(photo)
        user_photo = user_photo.resize(user_photo_resize)
        img.paste(user_photo, user_photo_position)

        # Metinleri afişe ekle
        draw.text(name_position, f'{name}', fill=name_color, font=fontName)
        draw.text(slogan_position, f'{slogan}', fill=slogan_color, font=fontSlogan)
        draw.text(placeName_position, f'{placeName}', fill=placeName_color, font=fontPlaceName)
        
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode()

        return jsonify({"data": img_base64})

if __name__ == '__main__':
    app.run(debug=True)
