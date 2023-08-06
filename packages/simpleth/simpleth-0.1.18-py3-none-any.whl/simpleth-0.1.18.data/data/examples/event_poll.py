"""Simple program to periodically check for an event"""

import time
from simpleth import Contract, EventSearch

poll_freq = 3    # number of seconds between checks
num_polls = 10   # number of checks
contract_name = 'TEST'    # contract emitting event
event_name = 'NumsStore'    # check for this event

c = Contract('Test')
c.connect()
e = EventSearch(c, 'NumsStored')

while num_polls > 0:
    events = e.get_new()
    num_events = len(events)
    if num_events:
        print(f'Found {num_events} new events')
    else:
        print(f'No new events')
    num_polls = num_polls - 1
    time.sleep(poll_freq)