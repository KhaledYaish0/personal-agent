# Khaled Yaish — Personal Agent (Gradio + OpenAI)

This project is a personal **Chat Agent** for **Khaled Yaish**, built with **Python**, **Gradio**, and **OpenAI**.  
The agent loads context from `summary.txt` and `me/linkedin.pdf` and answers visitors as if Khaled himself.  
It includes multiple tools such as:  
- Booking meetings  
- Sending CV / Portfolio  
- Recording job offers  
- Auto-generating Zoom links  
- Mentorship requests  
- Feedback collection  
- Special alerts when certain names are mentioned  

**Important:** Never commit `.env` or API keys to GitHub.  

---

## Project Structure
```
/my-agent-project
  |-- app.py              # Main code (Gradio + OpenAI Agent)
  |-- requirements.txt    # Project dependencies
  |-- README.md           # Project documentation (this file)
  |-- .gitignore          # Protects secrets and unnecessary files
  |-- me/
       |-- summary.txt    # Personal summary
       |-- linkedin.pdf   # LinkedIn profile (optional)
```

---

## Requirements
- Python 3.10+  
- OpenAI API key  
- Pushover API token + user  

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/USERNAME/personal-agent.git
cd personal-agent
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your keys:
```
OPENAI_API_KEY=sk-...
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user
```

---

## Run
Run the app:
```bash
python app.py
```

Gradio will provide a local URL (and sometimes a public share link).

---


## .gitignore
Make sure `.env` is ignored:
```txt
.env
__pycache__/
*.pyc
.venv/
venv/
```

---

## Deploying on Hugging Face Spaces

1. Create a new Space (select **Gradio** as SDK).  
2. Upload your project files.  
3. Add `requirements.txt` and `.gitignore`.  
4. Go to **Settings → Repository secrets** and add:
   - `OPENAI_API_KEY`
   - `PUSHOVER_TOKEN`
   - `PUSHOVER_USER`

---

## requirements.txt
```
openai
python-dotenv
gradio
pypdf
requests
```

---

## Security Best Practices
- **Never** commit `.env` or any API keys.  
- If a key leaks, **rotate it immediately**.  
- Use **GitHub Secrets** or **Hugging Face Secrets** for deployment.  

---
## Live Demo
Check out the live demo on Hugging Face Spaces:  
👉 [Personal Agent on Hugging Face](https://huggingface.co/spaces/KhaledYaish/personal-agent)
