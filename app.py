from flask import Flask, request, send_file
from gtts import gTTS
from pdfminer.high_level import extract_text
from googletrans import Translator
import os

app = Flask(__name__)
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pdf_file = request.files.get('file')
        language = request.form.get('language')

        if pdf_file and pdf_file.filename.endswith('.pdf'):
            # Save file to disk
            filename = pdf_file.filename
            pdf_file.save(filename)

            # Convert PDF to text
            text = extract_text(filename)

            # Remove the pdf file
            os.remove(filename)

            # Translate text
            translated = translator.translate(text, dest=language)
            
            # Convert text to speech
            tts = gTTS(text=translated.text, lang=language)
            speech_filename = 'speech.mp3'
            tts.save(speech_filename)

            return send_file(speech_filename, as_attachment=True)

    return '''
        <html>
            <head>
                <title>PDF to Speech</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #f8f9fa;
                    }
                    .container {
                        width: 500px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="text-center">Audiobook Reader</h1>
                    <form method="POST" enctype="multipart/form-data">
                        <div class="form-group">
                            <label for="file">Upload a Book</label>
                            <input type="file" class="form-control-file" name="file">
                        </div>
                        <div class="form-group">
                            <label for="language">Select language</label>
                            <select class="form-control" name="language">
                                <option value="en">English</option>
                                <option value="es">Spanish</option>
                                <option value="te">Telugu</option>

                                <!-- Add as many languages as you want here -->
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Convert</button>
                    </form>
                </div>
            </body>
        </html>
    '''

if __name__ == "__main__":
    app.run(port=5000, debug=True)
