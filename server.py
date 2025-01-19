from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    # Get the text from the POST request
    data = request.get_json()
    
    # Check if 'text_to_analyze' is in the request data
    if 'text_to_analyze' not in data:
        return jsonify({"error": "No text provided"}), 400

    text_to_analyze = data['text_to_analyze']
    
    # Call the emotion_detector function to get the analysis
    result = emotion_detector(text_to_analyze)
    
    # Prepare the response in the desired format
    emotions = result
    dominant_emotion = emotions['dominant_emotion']
    emotion_values = ', '.join([f"'{key}': {value}" for key, value in emotions.items() if key != 'dominant_emotion'])
    
    response_text = (f"For the given statement, the system response is {emotion_values}. "
                     f"The dominant emotion is {dominant_emotion}.")
    
    # Return the response as a JSON object
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5001)