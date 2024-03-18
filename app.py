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
        photo = request.files['photo']
        name = request.form['name']
        slogan = request.form['slogan']
        afis_type = request.form['type']
        belediye = request.form['belediye']
        
        # Afiş tipine göre görseli seç
        if afis_type == 'akp':
            afis_image = 'afis_akp.jpeg'
            name_color = 'white'
            slogan_color = 'black'
            belediye_color = 'black'
            name_fontSize = 86
            slogan_fontSize = 26
            belediye_fontSize = 56
            name_position = (390, 250)
            slogan_position = (390, 380)
            belediye_position = (390, 450)
        elif afis_type == 'chp':
            afis_image = 'afis_chp.jpeg'
            name_color = 'red'
            slogan_color = 'black'
            belediye_color = 'white'
            name_fontSize = 86
            slogan_fontSize = 26
            belediye_fontSize = 56
            name_position = (390, 250)
            slogan_position = (390, 380)
            belediye_position = (390, 450)
        elif afis_type == 'mhp':
            afis_image = 'afis_mhp.jpeg'
            name_color = 'red'
            slogan_color = 'black'
            belediye_color = 'black'
            name_fontSize = 86
            slogan_fontSize = 26
            belediye_fontSize = 56
            name_position = (390, 250)
            slogan_position = (390, 380)
            belediye_position = (390, 450)
        elif afis_type == 'diger' or afis_type == 'muhtar':
            afis_image = 'afis_diger.jpeg' if afis_type == 'diger' else 'afis_muhtar.jpeg'
            name_color = 'red'
            slogan_color = 'black'
            belediye_color = 'white'
            name_fontSize = 76
            slogan_fontSize = 26
            belediye_fontSize = 56
            name_position = (390, 250)
            slogan_position = (390, 380)
            belediye_position = (380, 48)

        # Afiş oluştur
        img = Image.open(os.path.join('static', afis_image))
        draw = ImageDraw.Draw(img)
        fontName = ImageFont.truetype('static/ARLRDBD.ttf', name_fontSize)
        fontSlogan = ImageFont.truetype('static/ARLRDBD.ttf', slogan_fontSize)
        fontBelediye = ImageFont.truetype('static/ARLRDBD.ttf', belediye_fontSize)

        # Fotoğrafı afişe ekle
        user_photo = Image.open(photo)
        user_photo = user_photo.resize((327, 455))
        img.paste(user_photo, (20, 16))

        # İsim, slogan ve belediye/mahalle ismi yaz
        draw.text(name_position, f'{name}', fill=name_color, font=fontName)
        draw.text(slogan_position, f'{slogan}', fill=slogan_color, font=fontSlogan)
        draw.text(belediye_position, f'{belediye}', fill=belediye_color, font=fontBelediye)

        # Oluşan afişi base64 formatında döndürme
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode()

        return jsonify({"data": img_base64})

if __name__ == '__main__':
    app.run(debug=True)
