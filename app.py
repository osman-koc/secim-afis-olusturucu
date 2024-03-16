from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

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

        # Kullanıcının yüklediği fotoğrafı kaydet
        photo.save(os.path.join('static', photo.filename))

        # Afiş oluştur
        img = Image.open('static/afis.jpg')
        draw = ImageDraw.Draw(img)
        fontName = ImageFont.truetype('static/ARLRDBD.ttf', 86)
        fontSlogan = ImageFont.truetype('static/ARLRDBD.ttf', 26)

        # Fotoğrafı afişe ekle
        user_photo = Image.open(os.path.join('static', photo.filename))
        user_photo = user_photo.resize((327, 455))
        img.paste(user_photo, (20, 16))

        # İsim ve sloganı afişe yaz
        draw.text((390, 250), f'{name}', fill='black', font=fontName)
        draw.text((390, 380), f'{slogan}', fill='black', font=fontSlogan)

        # Oluşan afişi kaydet ve indirme linkini gönder
        img.save(os.path.join('static', 'generated_afis.png'))
        return send_file(os.path.join('static', 'generated_afis.png'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
