import json
import requests
TRANSFORMERS_API_TOKEN = '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'

def get_articles_summary(text):
    """function to call Hugging face endpoint to get summary opf the text."""
    
    payload = {'inputs': text}
    headers = {"Authorization": f"Bearer {TRANSFORMERS_API_TOKEN}"}
    SUMMARY_HF_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    data = json.dumps(payload)
    response = requests.request("POST", 
                                SUMMARY_HF_URL, 
                                headers=headers, 
                                data=data)
    return json.loads(response.content.decode("utf-8"))[0]['summary_text']


