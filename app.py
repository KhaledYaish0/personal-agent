from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)

# ================== PUSHOVER ==================
def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

# ================== BASE TOOLS ==================
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Unknown question: {question}")
    return {"recorded": "ok"}

# ================== NEW TOOLS ==================
# 1. Booking Meeting
def book_meeting(date, time, method="Zoom", notes=""):
    push(f"Meeting booked on {date} at {time} via {method}. Notes: {notes}")
    return {"status": "meeting recorded"}

book_meeting_json = {
    "name": "book_meeting",
    "description": "Record a meeting booking request from the user",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {"type": "string","description": "Date (YYYY-MM-DD)"},
            "time": {"type": "string","description": "Time (HH:MM)"},
            "method": {"type": "string","description": "Zoom, Google Meet, etc."},
            "notes": {"type": "string","description": "Extra details"}
        },
        "required": ["date","time"],
        "additionalProperties": False
    }
}

# 2. Request Portfolio / CV
def request_portfolio(email):
    push(f"Portfolio requested. Send to: {email}")
    return {"status": "portfolio request recorded"}

request_portfolio_json = {
    "name": "request_portfolio",
    "description": "User requests a copy of Khaled's CV/Portfolio",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string","description": "Email to send portfolio"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

# 3. Custom Notes / Follow-up
def record_followup(note):
    push(f"Follow-up note: {note}")
    return {"status": "follow-up recorded"}

record_followup_json = {
    "name": "record_followup",
    "description": "Record a custom note or follow-up request",
    "parameters": {
        "type": "object",
        "properties": {
            "note": {"type": "string","description": "The note or follow-up request"}
        },
        "required": ["note"],
        "additionalProperties": False
    }
}

# 4. Send Materials
def send_materials(email, material_type="Portfolio/GitHub", notes=""):
    push(f"Send {material_type} to {email}. Notes: {notes}")
    return {"status": "materials request recorded"}

send_materials_json = {
    "name": "send_materials",
    "description": "Send requested materials like CV, Portfolio, or GitHub",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string","description": "Receiver email"},
            "material_type": {"type": "string","description": "Portfolio, GitHub, Code"},
            "notes": {"type": "string","description": "Extra details"}
        },
        "required": ["email","material_type"],
        "additionalProperties": False
    }
}

# 6. Collect Feedback
def record_feedback(feedback, email=""):
    push(f"Feedback: {feedback}, Contact: {email}")
    return {"status": "feedback recorded"}

record_feedback_json = {
    "name": "record_feedback",
    "description": "Record feedback from the user",
    "parameters": {
        "type": "object",
        "properties": {
            "feedback": {"type": "string","description": "Feedback text"},
            "email": {"type": "string","description": "Optional contact email"}
        },
        "required": ["feedback"],
        "additionalProperties": False
    }
}

# 7. Job Offer Recording
def record_job_offer(company, title, description="", salary="", location="", contact=""):
    push(f"Job Offer from {company}: {title}, {location}, Salary: {salary}, Contact: {contact}, Desc: {description}")
    return {"status": "job offer recorded"}

record_job_offer_json = {
    "name": "record_job_offer",
    "description": "Record a job offer",
    "parameters": {
        "type": "object",
        "properties": {
            "company": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "salary": {"type": "string"},
            "location": {"type": "string"},
            "contact": {"type": "string"}
        },
        "required": ["company","title"],
        "additionalProperties": False
    }
}

# 8. Interview Request
def record_interview_request(company, date, time, method="Zoom", notes=""):
    push(f"Interview request from {company} on {date} at {time} via {method}. Notes: {notes}")
    return {"status": "interview request recorded"}

record_interview_request_json = {
    "name": "record_interview_request",
    "description": "Record interview request details",
    "parameters": {
        "type": "object",
        "properties": {
            "company": {"type": "string"},
            "date": {"type": "string"},
            "time": {"type": "string"},
            "method": {"type": "string"},
            "notes": {"type": "string"}
        },
        "required": ["company","date","time"],
        "additionalProperties": False
    }
}

# 9. Request Code Samples
def request_code_samples(project_type, email=""):
    push(f"Code sample requested: {project_type}. Send to: {email}")
    return {"status": "code sample request recorded"}

request_code_samples_json = {
    "name": "request_code_samples",
    "description": "Request code samples from Khaled",
    "parameters": {
        "type": "object",
        "properties": {
            "project_type": {"type": "string","description": "ML, Web, IoT, etc."},
            "email": {"type": "string"}
        },
        "required": ["project_type"],
        "additionalProperties": False
    }
}

# 10. Ask for Mentorship
def request_mentorship(topic, email):
    push(f"Mentorship request on {topic}. Contact: {email}")
    return {"status": "mentorship request recorded"}

request_mentorship_json = {
    "name": "request_mentorship",
    "description": "Record a mentorship request",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "email": {"type": "string"}
        },
        "required": ["topic","email"],
        "additionalProperties": False
    }
}

# 11. Auto-Send Zoom Link
def auto_send_zoom(email, date, time):
    zoom_link = f"https://zoom.us/fake-meeting/{date}-{time}"
    push(f"Zoom link auto-generated: {zoom_link} for {email}")
    return {"zoom_link": zoom_link}

auto_send_zoom_json = {
    "name": "auto_send_zoom",
    "description": "Auto-generate a Zoom link and send to user",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "date": {"type": "string"},
            "time": {"type": "string"}
        },
        "required": ["email","date","time"],
        "additionalProperties": False
    }
}

# 12. Multi-language Support
def set_language_preference(language):
    push(f"User language set to: {language}")
    return {"status": f"language set to {language}"}

set_language_preference_json = {
    "name": "set_language_preference",
    "description": "Record user's preferred language",
    "parameters": {
        "type": "object",
        "properties": {
            "language": {"type": "string","description": "Language name"}
        },
        "required": ["language"],
        "additionalProperties": False
    }
}

# 13. Amr Qamhieh Alert
def record_amr_qamhieh(message=""):
    if "amr qamhieh" in message.lower():
        push(f"Mentioned Amr Qamhieh!\n💬 Message: {message}")
        return {"status": "amr qamhieh recorded"}
    return {"status": "ignored"}

record_amr_qamhieh_json = {
    "name": "record_amr_qamhieh",
    "description": "Send an alert if the user message mentions 'Amr Qamhieh' (case-insensitive)",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {"type": "string","description": "The full user message"}
        },
        "required": ["message"],
        "additionalProperties": False
    }
}



# ================== TOOLS LIST ==================
tools = [
    {"type": "function", "function": {
        "name": "record_user_details",
        "description": "Record that a user provided email",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "name": {"type": "string"},
                "notes": {"type": "string"}
            },
            "required": ["email"],
            "additionalProperties": False
        }
    }},
    {"type": "function", "function": {
        "name": "record_unknown_question",
        "description": "Record unknown questions",
        "parameters": {
            "type": "object",
            "properties": {"question": {"type": "string"}},
            "required": ["question"],
            "additionalProperties": False
        }
    }},
    {"type": "function", "function": book_meeting_json},
    {"type": "function", "function": request_portfolio_json},
    {"type": "function", "function": record_followup_json},
    {"type": "function", "function": send_materials_json},
    {"type": "function", "function": record_feedback_json},
    {"type": "function", "function": record_job_offer_json},
    {"type": "function", "function": record_interview_request_json},
    {"type": "function", "function": request_code_samples_json},
    {"type": "function", "function": request_mentorship_json},
    {"type": "function", "function": auto_send_zoom_json},
    {"type": "function", "function": set_language_preference_json},
    {"type": "function", "function": record_amr_qamhieh_json},
]

# ================== MAIN CLASS ==================
class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Khaled Yaish"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website. Be professional and engaging.\n\n"
        system_prompt += f"## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"If user asks for CV or resume, call the send_cv tool."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
