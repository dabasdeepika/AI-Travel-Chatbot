# AI-Travel-Chatbot
"A full-stack travel assistant chatbot built with Django, Rasa, and a responsive front-end."

## Features

- Conversational chatbot interface with nice chat bubble design.
- Collects user data (name, age, phone, email, address, etc.).
- Auto-fills city and state from pin code using postal API.
- Time-based greetings (Good morning, afternoon, evening, etc.).
- Multi-language support (English / Hindi).
- Backend storage using Django REST API.
- Rasa handles natural language understanding (NLU) and dialog management.


---

## Installation / Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/travel-chatbot.git
cd travel-chatbot


## Folder Structure
Travel-Chatbot/          <-- Root of repo
│
├── README.md            
├── .gitignore           
│
├── backend/             <-- Django backend + Chatbot API
│   ├── project/         <-- Your main Django project folder
│   │   ├── __init__.py  
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── manage.py
│   │
│   ├── chatbotapi/      <-- Django app folder
│   │   ├── __init__.py  
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests.py
│   │
│   └── load_sample_data.py
│
├── rasa/                <-- Rasa chatbot folder
│   ├── actions/         <-- Your custom actions
│   │   └── actions.py
│   ├── data/            <-- NLU, rules, stories
│   │   ├── nlu.yml
│   │   ├── rules.yml
│   │   ├── stories.yml
│   │   └── test_stories.yml
│   ├── config.yml
│   ├── domain.yml
│   └── endpoints.yml
│
└── frontend/            <-- Frontend code
    ├── chatbot.html
    ├── style.css
    └── script.js


## Setup Django backend

cd DjangoProject
python -m venv env
source env/bin/activate       
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Setup Rasa chatbot

cd rasa-bot
pip install -r requirements.txt
rasa train
rasa run actions            # Start actions server
rasa shell                  # Or run Rasa server

## Open Frontend

Open frontend/index.html in browser.
Chatbot will connect to Rasa + Django backend.

