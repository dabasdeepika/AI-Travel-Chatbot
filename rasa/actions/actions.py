from typing import Any, Dict, List, Text
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import re
from datetime import datetime

# ----------- FORM VALIDATION -----------
class ValidateUserDataForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_data_form"

    def validate_phone(
        self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict:
        if re.fullmatch(r"\d{10}", value):
            return {"phone": value}
        dispatcher.utter_message(response="utter_invalid_phone")
        return {"phone": None}

    def validate_email(
        self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict:
        if re.match(r"[^@]+@[^@]+\.[^@]+", value):
            return {"email": value}
        dispatcher.utter_message(response="utter_invalid_email")
        return {"email": None}

    def validate_pincode(
        self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict:
        if not re.fullmatch(r"\d{6}", value):
            dispatcher.utter_message(response="utter_invalid_pincode")
            return {"pincode": None}

        try:
            response = requests.get(f"https://api.postalpincode.in/pincode/{value}")
            data = response.json()

            if data[0]["Status"] == "Success":
                post_office = data[0]["PostOffice"][0]
                city = post_office["District"]
                state = post_office["State"]
                dispatcher.utter_message(text=f"📍 Auto-filled City: {city}, State: {state}")
                return {"pincode": value, "city": city, "state": state}
            else:
                dispatcher.utter_message(text="⚠️ Couldn't fetch city/state from the pin code.")
                return {"pincode": None}

        except Exception as e:
            dispatcher.utter_message(text="⚠️ Error while fetching location info.")
            print(f"[PINCODE API ERROR] {e}")
            return {"pincode": None}

    def validate_age(
        self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict:
        if value.isdigit() and 0 < int(value) < 120:
            return {"age": value}
        dispatcher.utter_message(text="❌ Please enter a valid age.")
        return {"age": None}


# ----------- TIME-BASED GREETING -----------
class ActionTimeBasedGreet(Action):
    def name(self) -> Text:
        return "action_time_based_greet"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "🌅 Good morning!"
        elif 12 <= hour < 17:
            greeting = "☀️ Good afternoon!"
        elif 17 <= hour < 21:
            greeting = "🌇 Good evening!"
        else:
            greeting = "🌙 Hello!"

        dispatcher.utter_message(text=f"{greeting} Let's get started with your details.")
        return []


# ----------- FORM SUBMISSION TO BACKEND -----------
class ActionSubmitUserData(Action):
    def name(self) -> Text:
        return "action_submit_user_data"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        data = {
            "name": tracker.get_slot("name"),
            "age": tracker.get_slot("age"),
            "phone": tracker.get_slot("phone"),
            "email": tracker.get_slot("email"),
            "gender": tracker.get_slot("gender"),
            "dob": tracker.get_slot("dob"),
            "state": tracker.get_slot("state"),
            "city": tracker.get_slot("city"),
            "address": tracker.get_slot("address"),
            "pincode": tracker.get_slot("pincode"),
        }

        try:
            data["age"] = int("".join(filter(str.isdigit, str(data["age"]))))
        except (ValueError, TypeError):
            dispatcher.utter_message(text="❌ Invalid age format.")
            return []

        try:
            response = requests.post("http://localhost:8000/api/userdata/", json=data)
            if response.status_code == 201:
                dispatcher.utter_message(text="✅ Your data was successfully saved!")
            else:
                dispatcher.utter_message(text="❌ Failed to save your data.")
        except Exception as e:
            dispatcher.utter_message(text="⚠️ Something went wrong while saving your data.")
            print(f"[API ERROR] {e}")

        return []
