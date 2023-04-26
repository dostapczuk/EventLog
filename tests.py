import json
import unittest
from datetime import datetime, timedelta
from unittest import mock

from event_log import EventLog, Event


class EventLogTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        time = datetime.now()
        self.times = [
            time.strftime("%d-%m-%Y %H:%M:%S"),
            (time - timedelta(days=2)).strftime("%d-%m-%Y %H:%M:%S"),
            (time - timedelta(days=1)).strftime("%d-%m-%Y %H:%M:%S")
        ]
        self.new_event = {
            "category": ["race_condition", ],
            "person": ["team", "John"],
            "time": self.times[0],
            "event": "@team we have #race_condition in chat service, @John fyi"
        }
        self.events = [
           {
                "category": ["update", ],
                "person": "all",
                "time": self.times[1],
                "event": "I just won a lottery #update @all"
            },
            {
                "category": ["Test", "task"],
                "person": "",
                "time": self.times[2],
                "event": "#Test #task is difficult"
            }
        ]
        events = [Event(**x) for x in self.events]
        self.json_return = self.events
        self.event_log = EventLog(events)

    def test_get_events(self):
        events = self.event_log.get_events()
        self.assertEqual(events, self.json_return)

    def test_add_event(self):
        event_str = "@team we have #race_condition in chat service, @John fyi"
        with mock.patch('datetime.datetime', wraps=datetime) as dt:
            dt.now.return_value = self.times[0]
            event = self.event_log.add_event(event_str)
        self.assertEqual(event, self.new_event)

    def test_get_events_by_category(self):
        category = "Test"
        event = self.event_log.get_events_by_category(category)
        self.assertIn(self.events[1], event)

    def test_get_events_by_person(self):
        person = "all"
        event = self.event_log.get_events_by_person(person)
        self.assertIn(self.events[0], event)

    def test_get_events_by_time(self):
        time = self.times[2]
        event = self.event_log.get_events_by_time(time)
        self.assertIn(self.events[1], event)


if __name__ == '__main__':
    unittest.main()