'''from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response
from functools import wraps
import pandas as pd
import os

app = Flask(__name__)
# This dictionary stores username-password pairs (you need to define this)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

def check_auth(username, password):
    user_hash = users.get(username)
    if user_hash:
        return user_hash == password
    return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            # Return 401 with WWW-Authenticate header to prompt for credentials
            response = make_response(jsonify({"message": "Authentication Required"}), 401)
            response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
            return response
        return f(*args, **kwargs)
    return decorated


users = {
    "admin": generate_password_hash("adminpas"),
    # Add more users as needed
}

def check_auth(username, password):
    user_hash = users.get(username)
    if user_hash:
        return check_password_hash(user_hash, password)
    return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            # Return 401 with WWW-Authenticate header to prompt for credentials
            response = make_response(jsonify({"message": "Authentication Required"}), 401)
            response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
            return response
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    return render_template('index.html')

@app.route('/division1A/table', methods=['GET', 'POST'])
@requires_auth
def data_table():
    #if request.method == 'POST':
        #file = request.form['upload-file']
        #print('Absolute path of file:     ', os.path.abspath(file))
        #print("Type : ",type(os.path.abspath(file)))
        data = pd.read_excel( "NationalCamogieLeague.xlsx",0)#os.path.abspath(file)
        return render_template('data.html', data=data.to_html())#to_dict())

@app.route('/division1A/data', methods=['GET', 'POST'])
@requires_auth
def data_json():
    #if request.method == 'POST':
        #file = request.form['upload-file']
        #print('Absolute path of file:     ', os.path.abspath(file))
        #print("Type : ",type(os.path.abspath(file)))
        data = pd.read_excel( "NationalCamogieLeague.xlsx",0)#os.path.abspath(file)
        return render_template('data.html', data=data.to_json())#to_dict())

@app.route('/division1B/table', methods=['GET', 'POST'])
@requires_auth
def data_table():
    #if request.method == 'POST':
        #file = request.form['upload-file']
        #print('Absolute path of file:     ', os.path.abspath(file))
        #print("Type : ",type(os.path.abspath(file)))
        data = pd.read_excel( "NationalCamogieLeague.xlsx",1)#os.path.abspath(file)
        return render_template('data.html', data=data.to_html())#to_dict())

@app.route('/division1B/data', methods=['GET', 'POST'])
@requires_auth
def data_json():
    #if request.method == 'POST':
        #file = request.form['upload-file']
        #print('Absolute path of file:     ', os.path.abspath(file))
        #print("Type : ",type(os.path.abspath(file)))
        data = pd.read_excel( "NationalCamogieLeague.xlsx",1)#os.path.abspath(file)
        return render_template('data.html', data=data.to_json())#to_dict())

if __name__ == '__main__':
    app.run(debug=True)'''

from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response
from functools import wraps
import pandas as pd
import os

app = Flask(__name__)
# This dictionary stores username-password pairs (you need to define this)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

def check_auth(username, password):
    user_hash = users.get(username)
    if user_hash:
        return user_hash == password
    return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            # Return 401 with WWW-Authenticate header to prompt for credentials
            response = make_response(jsonify({"message": "Authentication Required"}), 401)
            response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
            return response
        return f(*args, **kwargs)
    return decorated

def read_excel_data(sheet_number):
    data = pd.read_excel("NationalCamogieLeague.xlsx", sheet_number)
    return data

def render_data_template(sheet_number):
    data = read_excel_data(sheet_number)
    return render_template('data.html', data=data.to_html())

'''
@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    return render_template('index.html')

'''
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the home page
@app.route('/')
@requires_auth
def home():
    return render_template('index2.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
@requires_auth
def upload_file():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("Success")
        return redirect(url_for('data_table_1A'))


@app.route('/division1A/table', methods=['GET', 'POST'])
@requires_auth
def data_table_1A():
    return render_data_template(0)

@app.route('/division1A/data', methods=['GET', 'POST'])
@requires_auth
def data_json_1A():
    data = read_excel_data(0)
    return render_template('data.html', data=data.to_json())

@app.route('/division1B/table', methods=['GET', 'POST'])
@requires_auth
def data_table_1B():
    return render_data_template(1)

@app.route('/division1B/data', methods=['GET', 'POST'])
@requires_auth
def data_json_1B():
    data = read_excel_data(1)
    return render_template('data.html', data=data.to_json())

@app.route('/division2A/table', methods=['GET', 'POST'])
@requires_auth
def data_table_2A():
    return render_data_template(2)

@app.route('/division2A/data', methods=['GET', 'POST'])
@requires_auth
def data_json_2A():
    data = read_excel_data(2)
    return render_template('data.html', data=data.to_json())

@app.route('/division2B/table', methods=['GET', 'POST'])
@requires_auth
def data_table_2B():
    return render_data_template(3)

@app.route('/division2B/data', methods=['GET', 'POST'])
@requires_auth
def data_json_2B():
    data = read_excel_data(3)
    return render_template('data.html', data=data.to_json())

@app.route('/division3A/table', methods=['GET', 'POST'])
@requires_auth
def data_table_3A():
    return render_data_template(4)

@app.route('/division3A/data', methods=['GET', 'POST'])
@requires_auth
def data_json_3A():
    data = read_excel_data(4)
    return render_template('data.html', data=data.to_json())

@app.route('/division3B/table', methods=['GET', 'POST'])
@requires_auth
def data_table_3B():
    return render_data_template(5)

@app.route('/division3B/data', methods=['GET', 'POST'])
@requires_auth
def data_json_3B():
    data = read_excel_data(5)
    return render_template('data.html', data=data.to_json())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = "10000")
