import requests
import json

url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}


def emotion_detector(text_to_analyze):
    input_json ={ "raw_document": { "text": text_to_analyze } }
    response = requests.post(url, headers=headers, json = input_json)
    response_data = response.json()

    # emotion scores dictionary
    predictions = response_data.get("emotionPredictions",[])
    emotions = predictions[0].get("emotion", {})

    # Extract the required emotions from the API response
    # If the response status code is 200
    if response.status_code == 200:
        relevant_emotions = {emotion: emotions.get(emotion) for emotion in["anger", "disgust", "fear", "joy", "sadness"]}
    if response.status_code == 400:
        return {emotion: None for emotion in ["anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"]}
    
    #extract dominant_emotions
    dominant_emotion = max(relevant_emotions, key=relevant_emotions.get)
    # Add the dominant emotion to the result
    relevant_emotions["dominant_emotion"] = dominant_emotion

    return relevant_emotions
