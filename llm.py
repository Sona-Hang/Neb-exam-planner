import requests
import os

def generate_tips(subjects, confidence, days_left, department):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "⚠️ API key not found. Please set OPENROUTER_API_KEY."

    weak = [s for s, c in zip(subjects, confidence) if c <= 2]

    prompt = f"""
Exams in {days_left} days.
Subjects: {', '.join(subjects)}.
Department: {department}.
Weak subjects: {', '.join(weak)}.
Confidence levels: {confidence}.
This is for NEB Class 12 (Plus Two) exam preparation in Nepal.
Give practical study tips based on question patterns, repeated NEB questions, and smart use of time.
Use short headings for each main topic, with a brief paragraph and a small bullet list under each heading.
Avoid long paragraphs. Make the advice easy to scan for a Class 12 student.
Focus on useful actions for Maths and Nepali, methods to practice, and how to stay calm and focused.
Write in a conversational, senior student tone rather than a formal AI style.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://study-planner-ai.local"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a practical study coach for NEB Class 12 students in Nepal, focused on useful study habits and exam-ready preparation."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        },
        timeout=30
    )

    # Check if response is HTML (auth failure)
    if "text/html" in response.headers.get("content-type", ""):
        return "⚠️ API Error: Authentication failed. Check your OPENROUTER_API_KEY."

    if response.status_code != 200:
        return f"⚠️ API Error ({response.status_code}): {response.text[:200]}"

    try:
        data = response.json()
    except Exception as e:
        return f"⚠️ API Error: Invalid response. Status: {response.status_code}"

    if "error" in data:
        return f"⚠️ API Error: {data['error'].get('message', str(data['error']))}"

    if "choices" not in data:
        return f"⚠️ API Error: Unexpected response format"

    return data["choices"][0]["message"]["content"]