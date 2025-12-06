from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess
from datetime import datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Папка для хранения файлов

# Создаём папку для загрузок, если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # convert()
    if request.method == 'POST':
        # Получаем файл из формы
        file = request.files['file']
        if file:
            # Сохраняем файл в папку
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'in1.mp3'))
            convert()
            return redirect(url_for('download_file'))
    return render_template('upload.html')


@app.route('/download')
def download_file():
    file=''

    # Получаем список файлов в папке
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if 'out.opus' in files:
        file = 'out.opus'
    print(files)
    return render_template('download.html', file=file)


@app.route('/download/<filename>')
def download(filename):
    # Отдаём файл для скачивания
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


def convert():
    #ffmpeg -i in.mp3 -c:a libopus -b:a 128k -vbr on -compression_level 10 out.opus
    # command = [
    #     "ffmpeg",
    #     "-i", input_file,
    #     "-c:a", "libopus",
    #     "-b:a", bitrate,
    #     "-vbr", "on",
    #     "-compression_level", "10",
    #     output_file
    # ]
    current_time = datetime.now().time()
    new_name = str(current_time)+".opus"

    # Получаем список процессов, отсортированных по CPU и памяти
    cmd = "cd uploads && ffmpeg -i in.mp3 -c:a libopus -b:a 128k -vbr on -compression_level 10 "+new_name
    #result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='latin-1'  # или 'utf-8' с errors='ignore'
        )
        print(f"Успешно сконвертировано в {result}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    app.run(debug=True)
