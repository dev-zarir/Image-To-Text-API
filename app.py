from flask import Flask, request, jsonify
from urllib.parse import unquote_plus
import requests

def img_to_text(base64:str):
    attemp=0
    while attemp<100:
        resp = requests.post(
            url="https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAUbA4T8UWO-pw750uQqz0X2deq9lHLuLk",
            headers={
                "x-android-package": "image.to.text.ocr",
                "x-android-cert": "ad32d34755bb3b369a2ea8dfe9e0c385d73f80f0",
                "Content-Type": "application/json",
            },
            data='{"requests": [{"features": [{"maxResults": 10,"type": "DOCUMENT_TEXT_DETECTION"}],"image": {"content": "' + base64 + '"}}]}',
        )
        try:
            return resp.json()["responses"][0]["fullTextAnnotation"]["text"]
        except:
            if 'Resource' in resp.text:
                attemp+=1
                continue
            elif 'Quota exceeded' in resp.text:
                attemp+=1
                continue
            else:
                raise Exception(f'Something went wrong! {resp.text}')

app=Flask(__name__)
app.config['SECRET_KEY']='thisismysecretkey'

@app.route('/', methods=['POST'])
def home():
	base64=request.form.get('data')
	try:
		text=img_to_text(base64)
		return jsonify({'success':True, 'text':text})
	except Exception as e:
		return jsonify({'success':False, 'message':str(e)})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)