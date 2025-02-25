import os
import json
import requests
from typing import Dict, Any

def generate_assignment_questions(topic: str, subject: str) -> Dict[str, Any]:
    """
    Generate assignment questions using Groq's LLM API
    """
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    prompt = f"""Generate a multiple choice quiz for {subject} focusing on {topic}. 
    Create 3 questions with 4 options each and one correct answer.
    Return the response in the following JSON format:
    {{
        "title": "Quiz title",
        "questions": [
            {{
                "id": 1,
                "question": "Question text",
                "options": ["option1", "option2", "option3", "option4"],
                "correctAnswer": "correct option",
                "points": 10
            }}
        ]
    }}
    Make sure the response is a valid JSON string."""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        # Extract the generated text from the response
        generated_text = response.json()['choices'][0]['message']['content']
        
        # Parse the JSON from the generated text
        # Find the first { and last } to handle any extra text
        start = generated_text.find('{')
        end = generated_text.rfind('}') + 1
        json_str = generated_text[start:end]
        
        assignment_data = json.loads(json_str)
        return assignment_data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling Groq API: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing LLM response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
