"""
This is a generic solution that would require SqlAlchemy
or Django models to get and serialize the data to work properly
"""

from datetime import datetime


class Event(object):
    def __init__(self,  **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __str__(self):
        return self.__getattribute__("event")

    def __repr__(self):
        return self.__getattribute__("event")


class EventLog(object):
    def __init__(self, events=None):
        self.events = events

    def get_events(self, events=None):
        if not events:
            events = self.events
        event_logs = []
        for event in events:
            event_log = {
                "category": event.category,
                "person": event.person,
                "time": str(event.time),
                "event": event.event
            }
            event_logs.append(event_log)
        return event_logs[:10]

    def add_event(self, event: str):
        event_words = event.split(" ")
        person = []
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        category = []
        for word in event_words:
            if word.startswith("@"):
                person.append(word[1:])
            if word.startswith("#"):
                category.append(word[1:])
        event_log = {
            "category": category,
            "person": person,
            "time": time,
            "event": event
        }
        event_obj = Event(**event_log)
        self.events.append(event_obj)
        return event_log

    def get_events_by_category(self, category):
        filtered_events = [event for event in self.events if category in event.category]
        return self.get_events(filtered_events)

    def get_events_by_time(self, time):
        filtered_events = [event for event in self.events if event.time == time]
        return self.get_events(filtered_events)

    def get_events_by_person(self, person):
        filtered_events = [event for event in self.events if person in event.person]
        return self.get_events(filtered_events)

