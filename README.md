# BinBuddy
![Desain tanpa judul](https://github.com/user-attachments/assets/5951d93b-8e03-4bdc-ace0-729f2373d234)
This project aims to develop a mobile application that classifies recyclable household waste in real-time, utilizing a cloud-based Convolutional Neural Network (CNN) model powered by TensorFlow. Aligned with the theme of "Sustainable Futures," this application promotes environmental sustainability by simplifying waste sorting and fostering responsible waste management.

## Team Members C242-PS025

| Member                | Student ID   | Path               | University     |
|----------------       |------------  |---------------     |----------------|
| Kent Cristopher       | M195B4KY2175 | Machine Learning   | Universitas Bunda Mulia |
| Alicia Silvia         | M195B4KX0373 | Machine Learning   | Universitas Bunda Mulia |
| Tamara                | M195B4KX4287 | Machine Learning   | Universitas Bunda Mulia |
| Nisa Hanifa Daniswari | C009B4KX3385 | Cloud Computing    | Universitas Gunadarma |
| Indah Sari Sitorus    | C134B4KX1971 | Cloud Computing    | Politeknik Negeri Sriwijaya |
| Albert Hansel         | A195B4KY0318 | Mobile Development | Universitas Bunda Mulia |
| Alvin Saputra         | A195B4KY0432 | Mobile Development | Universitas Bunda Mulia |

## API Documentation
### **Base URL**
> https://binbuddy-1033157844924.asia-southeast2.run.app

### 1. SignUp
* Url: /signup
* Method: Post
* Response Body (Success):
  ```json
  {
    "message": "Signup successful!",
    "user_id": "Q9telz7FcWXZuMTi4GWMmldLMhq2"
  }
  ```
  Failed :
  ```json
  {
    "error": "Username already exists"
  }
  ```
### 2. Login
* Url: /login
* Method: Post
* Response Body (Success):
  ```json
  {
    "error": "false",
    "exp": 1733475117,
    "message": "success",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiSW5kYWggU2FyaSIsImV4cCI6MTczMzQ3NTExN30.i4aGPNGacTwGL9X0owLxdqt-mfGApxcTtSkF1pAAX3I",
    "user": "Indah Sari"
  }
  ```
  Failed :
  ```json
  {
    "error": "Unable to verify"
  }
  ```
### 3. Classification
* Url: /classify
* Method: Post
* Response Body (Success):
  ```json
  {
    "class_name": "clothes",
    "probability": 0.9575
  }
  ```
  Failed :
  ```json
  {
    "Message": "Invalid token: Invalid header string: 'utf-8' codec can't decode byte 0x88 in position 6: invalid start byte"
  }
  ```
### 4. Save Classification
* Url: /save-classify
* Method: Post
* Response Body (Success):
  ```json
  {
    "document_id": "L8hiLw5bQY3ZfO1ZT8qZ",
    "image_url": "https://storage.googleapis.com/binbuddy-442205.firebasestorage.app/d93541ee-d983-432d-833a-eec1cb08deed__96913416_clothes1.jpg.webp",
    "message": "Classification saved successfully!"
  }
  ```
  Failed :
  ```json
  {
    "Message": "Invalid token: Invalid header string: 'utf-8' codec can't decode byte 0x88 in position 6: invalid start byte"
  }
  ```
### 5. Get Data
* Url: /get-data
* Method: Post
* Response Body (Success):
  ```json
  {
    "error": false,
    "listStory": [
        {
            "class_name": "clothes",
            "created_at": "2024-12-06T08:01:46.535000+00:00",
            "email": "indahsaa2003@gmail.com",
            "id": "bwA7R0ATgjOUKqTDDZ0L",
            "image_url": "https://storage.googleapis.com/binbuddy-442205.firebasestorage.app/2a881398-01e5-4762-a3c2-8b6d74854db7__96913416_clothes1.jpg.webp",
            "probability": 0.9575
        },
        {
            "class_name": "clothes",
            "created_at": "2024-12-06T08:01:20.869000+00:00",
            "email": "indahsaa2003@gmail.com",
            "id": "b3xRrK3Pa0YxwUV5oQ6a",
            "image_url": "https://storage.googleapis.com/binbuddy-442205.firebasestorage.app/fd3eca64-b8a1-486a-bef4-ffec88c6bb7d__96913416_clothes1.jpg.webp",
            "probability": 0.957
        },
        {
            "class_name": "clothes",
            "created_at": "2024-12-06T08:00:42.050000+00:00",
            "email": "indahsaa2003@gmail.com",
            "id": "L8hiLw5bQY3ZfO1ZT8qZ",
            "image_url": "https://storage.googleapis.com/binbuddy-442205.firebasestorage.app/d93541ee-d983-432d-833a-eec1cb08deed__96913416_clothes1.jpg.webp",
            "probability": 0.9575
        }
    ],
    "message": "Data fetched successfully"
  }
  ```
  Failed :
  ```json
  {
    "error": false,
    "listStory": [],
    "message": "No data found"
  }
  ```
### 6. Delete History
* Url: /delete-history
* Method: Post
* Response Body (Success):
  ```json
  {
    "deleted_document_id": "b3xRrK3Pa0YxwUV5oQ6a",
    "message": "Data deleted successfully."
  }
  ```
  Failed :
  ```json
  {
    "error": "No data found for the given document ID."
  }
  ```
## How to Replicate This Project
Follow these steps to replicate this project on your local machine:
### 1. Clone the Repository
First, clone the repository from GitHub using the following command:
```bash
git clone https:https://github.com/indahsaa/Cloud-Computing-BinBuddy.git
cd Cloud-Computing-Binbuddy
```
### 2. Install Dependencies
Install the dependencies using the following command:
```bash
pip install -r requirements.txt
```
### 3. Start The Project
Run the project using the appropriate command for your project type:
1. Run In your terminal 
```bash
python main.py
```
2. Access the App from browser
```bash
http://localhost:8080
```
3.  API Test
> Test the API using a testing application such as Postman, From our API documentation.

## Deploying to Google Cloud Run
1. Create an Artifact Registry repository:
   ```
   gcloud builds submit --tag gcr.io/[Your_PROJECT_ID/index
   ```
2. Deploy the container to Cloud Run:
   ```
   gcloud run deploy binbuddy --image gcr.io/[Your_PROJECT_ID/index --platform managed --region asia-southeast2
   ```
3. API URL
Once deployed, your API will be available at the URL provided by Google Cloud Run. Replace `[PROJECT_ID]` with your actual Google Cloud project ID in the following template:
`https://[SERVICE_NAME]-[REGION]-[PROJECT_ID].run.app`


