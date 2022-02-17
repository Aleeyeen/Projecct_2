import pyrebase 
from flask import render_template, request, redirect, session, Flask, Response
import cv2

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyAlzRUjngRbT3Jj2PyRnZduK0zBSZE2MIM",
    "authDomain": "flask-web-bcbb7.firebaseapp.com",
    "databaseURL": "https://flask-web-bcbb7-default-rtdb.firebaseio.com/",
    "projectId": "flask-web-bcbb7",
    "storageBucket": "flask-web-bcbb7.appspot.com",
    "messagingSenderId": "1046582323129",
    "appId": "1:1046582323129:web:f969226549695b8bcf7868",
    "measurementId": "G-J3GEEV7C29"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                return render_template('home.html')
            except:
                unsuccessful = 'Please check your e-mail or password'
                return render_template('index.html', umessage=unsuccessful)
    return render_template('index.html')

@app.route('/home' , methods=['GET', 'POST'])
def home():
    return render_template('home.html')

def generate():   
    # """Video streaming generator function."""
    cap = cv2.VideoCapture(0)

    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else: 
            break

@app.route('/video')
def video():
    return Response(generate(),  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fall_log', methods=['GET', 'POST'])
def fall_log():
    return render_template('fall_log.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.create_user_with_email_and_password(email, password)
                return render_template('index.html')
            except:
                unsuccessful = 'Please check your e-mail or field  '
                return render_template('create_account.html', umessage=unsuccessful)
    return render_template('create_account.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            try:
                auth.send_password_reset_email(email)
                return render_template('index.html')
            except:
                unsuccessful = 'Please check your field'
                return render_template('forgot_password.html', umessage=unsuccessful)
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)
