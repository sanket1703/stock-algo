import json

def get_slots():
    with open('slots.json', 'r') as f:
        return json.load(f)
    
def update_slots(slots):
    with open('slots.json', 'w') as f:
        json.dump(slots, f)