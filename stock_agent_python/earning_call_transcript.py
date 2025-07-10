import requests
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Union, Any, Dict, List
from loguru import logger
import os
import json

load_dotenv()
ALPHAVANTAGE_API = os.getenv("ALPHAVANTAGE_API")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_earning_call_transcript(symbol, quarter):
    url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={symbol}&quarter={quarter}&apikey={ALPHAVANTAGE_API}'
    r = requests.get(url)
    return r.json()

def query_ai(prompt: str) -> Union[Dict[str, Any], List[Any]]:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        return response.text
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        return {}

def get_earning_call_summary(symbol, quarter):
    earning_call_transcript = get_earning_call_transcript(symbol, quarter)['transcript']
    logger.info(f"Get earning call transcript: {earning_call_transcript}")
    prompt = f"""
              Give a short summary and sentiment analysis of the following earning call for {symbol} in quarter {quarter}:
            {earning_call_transcript}
            """
    response = query_ai(prompt)
    logger.info(response)
    try:
        data = json.loads(response)
        return data
    except Exception as e:
        logger.exception("Fail to get a json reply")
        return response
