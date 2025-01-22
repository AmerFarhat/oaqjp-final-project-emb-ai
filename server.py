from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")
@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route('/emotionDetector', methods = ['GET','POST'])
def emotion_detector_route():
    if request.method == 'GET':
        text_to_analyze = request.args.get('textToAnalyze', '')
    else:
        data = request.get_json()
        text_to_analyze = data.get('text_to_analyze', '') if data else ''
    # Check if 'text_to_analyze' is in the request data
    if not text_to_analyze:
        return jsonify({"error": "No text provided"}), 400
    
    # Call the emotion_detector function to get the analysis
    result = emotion_detector(text_to_analyze)
    
    if result['dominant_emotion'] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    # Prepare the response in the desired format
    emotions = result
    dominant_emotion = emotions['dominant_emotion']
    emotion_values = ', '.join([f"'{key}': {value}" for key, value in emotions.items() if key != 'dominant_emotion'])
    response_text = (f"For the given statement, the system response is {emotion_values}. "f"The dominant emotion is {dominant_emotion}.")
    
    # Return the response as a JSON object
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)