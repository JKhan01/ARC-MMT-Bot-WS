# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ValidateDetailsForm(Action):
    def name(self) -> Text:
        return "details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["source", "destination", "date_travel", "trip_type"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 Source=tracker.get_slot("source"),
                                 Destination=tracker.get_slot("destination"))

        data = requests.get(f"https://ae6226edecd0.ngrok.io/fetch_details/{tracker.slots.get('source')}/{tracker.slots.get('destination')}/oneway/{tracker.slots.get('date_travel')}")
        if data.status_code == 200:
            resp_dict = json.loads(data.text)
            response_message = ""
            if resp_dict["error_flag"] == "0":
                c = 1
                for j in resp_dict["response_list"]:
                    response_message += f"Flight: {c} \n"
                    response_message += f"Flight Company: {j['flight_company']} \n Departure: {j['departure_time']} \n"
                    response_message += f"Arrival: {j['arrival_time']} \n Duration: {j['flight_duration']} \n Ticket Price: {j['flight_price']}"
                    c += 1

            else:
                response_message = "No flights were found matching your requirement. Sorry"

        else:
            response_message = "Sorry We could not connect to the server to fetch the Flight data"

        dispatcher.utter_message(text=str(response_message))