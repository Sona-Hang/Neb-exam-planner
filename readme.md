\# 📚 Exam Strategy \& Study Planner AI (Class 12 – Nepal)



A simple AI-based study planner designed to help Class 12 students in Nepal prepare more effectively for exams.



\## Why I built this

Exam preparation is often unstructured.  

Students:

\- focus on easy subjects

\- ignore weak areas

\- start late and cram

\- don’t analyze past question patterns  



This project helps make studying more, planned and targeted



\- What it does

\- Takes input:

&#x20; - subjects

&#x20; - confidence level (1–5)

&#x20; - past scores

&#x20; - daily study hours

&#x20; - exam date  

\- Prioritizes subjects based on weakness  

\- Generates a daily study plan  

\- Explains why each subject is important  

\- Gives \*\*AI-generated study tips and strategies\*\*



\## AI Features

\- Random Forest model → assigns subject priority  

\- OpenAI (`gpt-oss-120b`) → generates:

&#x20; - personalized study tips  

&#x20; - explanations  

&#x20; - strategy suggestions  

\- Can improve over time with saved data  



\## Example output

> “Math is high priority because your confidence and past score are low.”  

> “Focus on past questions and practice weak topics first.”



\## Tech stack

\- Python  

\- Pandas, NumPy  

\- scikit-learn  

\- Streamlit  

\- OpenAI (via OpenRouter API)  



\## Run locally

```bash

pip install -r requirements.txt

python train\_model.py

streamlit run app.py

