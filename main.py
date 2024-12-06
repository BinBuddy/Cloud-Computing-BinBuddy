import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import io
import tensorflow as tf
import keras
import numpy as np
from PIL import Image
from functools import wraps
from flask import Flask, request, jsonify, make_response, render_template, session, flash
import jwt
import bcrypt
from flask_bcrypt import Bcrypt
from firebase_admin import credentials, initialize_app, firestore, auth, storage
import firebase_admin
import uuid
import time  

# model = keras.models.load_model("./mobilenetv3large_waste_finetune_base.keras")
model = keras.models.load_model("./model/mobilenetv3large_waste_finetune_64_latest.keras")


def transform_image(pillow_image):
    data = np.asarray(pillow_image)
    data = np.float32((data / 127.5) - 1)
    data = np.expand_dims(data, axis=0)

    data = keras.layers.Resizing(224, 224, pad_to_aspect_ratio=True)(data) # resized to model input; only accepts 1:1 images to be accurate
    # data = keras.layers.CenterCrop(224, 224)(data)
    return data


def predict(data):
    class_names = ['battery', 'biological', 'cardboard', 'clothes', 'glass', 'metal', 'paper', 'plastic', 'shoes', 'trash']

    # class_names = ['battery', 'biological', 'brown-glass', 
    #                'cardboard', 'clothes', 'green-glass', 
    #                'metal', 'paper', 'plastic', 
    #                'shoes', 'trash', 'white-glass']

    predictions = model.predict(data, verbose=0)
    prediction_sort = np.argsort(predictions[0])[::-1]
    prediction_confidence = predictions[0][prediction_sort]

    # result_dict = {}
    # for i in range(len(class_names)):
    #     result_dict[class_names[prediction_sort[i]]] = {
    #         "probability": round(float(prediction_confidence[i]), 4)
    #     }

    return_dict = {
        "class_name": class_names[prediction_sort[0]],
        "probability": round(float(prediction_confidence[0]), 4)
    }

    # return_dict = { class_names[prediction_sort[0]]: round(float(prediction_confidence[0]), 4) }
        
    return return_dict

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        
        try:
            # Memisahkan "Bearer" dari token
            token = auth_header.split(" ")[1] if "Bearer" in auth_header else auth_header
            
            # Debug: Print current time
            current_time = int(time.time())
            print(f"Current timestamp: {current_time}")
            
            # Decode token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Debug: Print token data and expiration
            print(f"Token data: {data}")
            print(f"Token expiration: {data.get('exp')}")
            
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Token has expired'}), 403
        except jwt.InvalidTokenError as e:
            return jsonify({'Message': f'Invalid token: {str(e)}'}), 403
        except IndexError:
            return jsonify({'Message': 'Invalid token format'}), 403

        return func(*args, **kwargs)
    return decorated



app = Flask(__name__)

app.config['SECRET_KEY'] = 'a084f6bb5df7401a8dd0fba140f26cbc'
bcrypt = Bcrypt()
cred = credentials.Certificate("./firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'binbuddy-442205.firebasestorage.app'
})
db = firestore.client()
bucket = storage.bucket()

@app.route("/classify", methods=["GET", "POST"])
@token_required
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes))
            pillow_img = pillow_img.convert("RGB")
            tensor = transform_image(pillow_img)
            prediction = predict(tensor)
            return jsonify(prediction)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "APINYA JALAN GAIS!!"

@app.route('/login', methods=['POST'])
def login():
    try:
        # Ambil data dari request
        email = request.form['email']
        password = request.form['password'] 

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

    
        user_ref = db.collection("users").where("email", "==", email).get()
        if not user_ref:
            return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

        # Ambil data pengguna
        user_doc = user_ref[0].to_dict()
        stored_password = user_doc.get('password')

        # Verifikasi password
        if not bcrypt.check_password_hash(stored_password, password):
            return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

        username = user_doc.get('username')

        # Buat token JWT
        current_time = int(time.time())
        exp_time = current_time + 3600  # 1 jam dari sekarang
        token = jwt.encode({
            'user': username,
            'exp': exp_time,
            # 'iat': current_time
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            'error': "false",
            'message': "success",
            'token': token,
            'exp': exp_time,
            'user': username,
            # 'expires_in': 3600,
            # 'token_type': 'Bearer'
        }), 200

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Service is Ready!"



@app.route("/signup", methods=["POST"])
def signup():

    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'] 

        if not email or not password or not username:
            return jsonify({"error": "Email, username, and password are required"}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
       
        user_ref = db.collection("users").where("username", "==", username).get()
        if user_ref:
            return jsonify({"error": "Username already exists"}), 400

        try:
            auth.get_user_by_email(email)
            return jsonify({"error": "Email is already registered with Firebase Authentication"}), 400
        except firebase_admin.exceptions.FirebaseError:
            pass

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user_ref = db.collection('users').document(email) 
        user_ref.set({
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username
        )
        return jsonify({"message": "Signup successful!", "user_id": user.uid}), 201

    except firebase_admin.exceptions.FirebaseError as e:
        return jsonify({"error": f"Firebase error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/save-classify", methods=["POST"])
@token_required
def save_classify():
    try:
        image_file = request.files.get('image')  
        class_name = request.form.get('class_name')
        probability = request.form.get('probability')
        email = request.form.get('email') 
        
        if not image_file or not class_name or not probability:
            return jsonify({"error": "All fields (image, class_name, probability) are required."}), 400
        
        # Menyimpan gambar ke Firebase Storage
        filename = f"{str(uuid.uuid4())}_{image_file.filename}"
        blob = bucket.blob(filename)
        blob.upload_from_file(image_file)
        blob.make_public()  

        image_url = blob.public_url

        # Simpan data klasifikasi ke Firestore
        classification_ref = db.collection('classifications').document()
        classification_ref.set({
            'image_url': image_url,
            'class_name': class_name,
            'probability': float(probability),
            'email': email,
            'created_at': firestore.SERVER_TIMESTAMP,
        })
        document_id = classification_ref.id
        return jsonify({"message": "Classification saved successfully!",
         "image_url": image_url,
         "document_id": document_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-data", methods=["GET"])
@token_required
def get_data():
    try:

        email = request.args.get('email')

        if not email:
            return jsonify({"error": "Email is required as query parameter."}), 400

        classifications = db.collection('classifications') \
            .where('email', '==', email) \
            .order_by('created_at', direction=firestore.Query.DESCENDING) \
            .stream()
        
        results = []

        for classification in classifications:
            data = classification.to_dict()
            results.append({
                "id": classification.id,
                "email": data.get('email'),
                "image_url": data.get('image_url'),
                "class_name": data.get('class_name'),
                "probability": data.get('probability'),
                "created_at": data.get('created_at').isoformat() if data.get('created_at') else None
            })
        
        if not results:
            return jsonify({"error": False, "message": "No data found", "listStory": []}), 404

        return jsonify({
            "error": False,
            "message": "Data fetched successfully",
            "listStory": results
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete-history", methods=["POST"])
@token_required
def delete_history():
    try:
        email = request.form.get('email')
        document_id = request.form.get('document_id')
    
        if not email or not document_id:
            return jsonify({"error": "Document_id and Email is required in the form data."}), 400
        classification_ref = db.collection('classifications').document(document_id)
        doc = classification_ref.get()

        if not doc.exists:
            return jsonify({"error": "No data found for the given document ID."}), 404
        
        data = doc.to_dict()
        
        if data.get('email') != email:
            return jsonify({"error": "Email does not match the document's email."}), 400

        classification_ref.delete()

        return jsonify({"message": "Data deleted successfully.", "deleted_document_id": document_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  
    app.run(host="0.0.0.0", port=port, debug=True)
    # app.run(debug=True)
