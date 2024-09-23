import geocoder
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import markdown
import os

# Configure Google API
GOOGLE_API_KEY = "AIzaSyCpDjrKq5lkm3LaW_U3N53IvNbHc4h5cnA"
genai.configure(api_key=GOOGLE_API_KEY)

# Flask app setup
app = Flask(__name__)
model = genai.GenerativeModel(model_name="gemini-pro")

# Function to convert text to markdown
def to_markdown(text):
    return markdown.markdown(text)

# Function to get live location based on IP
def get_location():
    g = geocoder.ip('me')
    if g.latlng:
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        return latitude, longitude
    else:
        return None, None

# Main route
@app.route('/')
def index():
    return render_template('index.html')

# Route to send message and get AI suggestions
@app.route('/send_message', methods=['POST'])
def send_message():
    # Get live location based on IP
    latitude, longitude = get_location()

    if latitude is None or longitude is None:
        return jsonify({"message": "Could not determine location."})
    
    # User message and additional request for suggestions 
    m = request.form['message']
    msg = f"Suggest some best {m} Tourist place   based on Latitude: {latitude}, Longitude: {longitude} and tell their specialty , provide the location not Latitude:, Longitude "

    print(f"Message to AI: {msg}")

    # Get response from Generative AI model
    response = model.generate_content(msg)

    # Return AI response in markdown format
    return jsonify({"message": to_markdown(response.text)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
