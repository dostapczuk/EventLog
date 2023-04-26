import json
import unittest
from datetime import datetime, timedelta
from event_log import EventLog, Event


class EventLogTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.times = [
            str(datetime.now()),
            str(datetime.now() - timedelta(days=2)),
            str(datetime.now() - timedelta(days=1))
        ]
        self.new_event = {
            "category": ["race_condition", ],
            "person": ["team", "John"],
            "time": self.times[0],
            "event": "@team we have #race_condition in chat service, @John fyi"
        }
        self.test_time = str(datetime.now() - timedelta(days=2))
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
        self.json_return = json.dumps(self.events)
        self.event_log = EventLog(events)

    def test_get_events(self):
        events = self.event_log.get_events()
        self.assertEqual(events, self.json_return)

    def test_add_event(self):
        event_str = "@team we have #race_condition in chat service, @John fyi"
        event = json.loads(self.event_log.add_event(event_str))
        for key in event.keys():
            if key == "time":
                self.assertEqual(event[key][:7], self.new_event[key][:7])
            else:
                self.assertEqual(event[key], self.new_event[key])

    def test_get_events_by_category(self):
        category = "Test"
        event = json.loads(self.event_log.get_events_by_category(category))
        self.assertIn(self.events[1], event)

    def test_get_events_by_person(self):
        person = "all"
        event = json.loads(self.event_log.get_events_by_person(person))
        self.assertIn(self.events[0], event)

    def test_get_events_by_time(self):
        time = self.times[2]
        event = json.loads(self.event_log.get_events_by_time(time))
        self.assertIn(self.events[1], event)


if __name__ == '__main__':
    unittest.main()