import cv2 

class Detector:
    def __init__(self):
        self.green = (0, 255, 0)
        self.red = (0, 0, 255)
        self.blue = (255, 0, 0)

        self.slots = []
        self.slot_removed = None
        self.coin_ids = set(range(3,13))

    def check_coin(self, ids):
        ids = set(ids)

        intersection = self.coin_ids & ids

        if len(intersection) > 0:
            return intersection
        else:
            return None
    
    def just_slots_ids(self, ids):
        slots = list(filter(lambda x: x > 13, ids))

        if self.slots and self.slots != slots:
            removed_slot = set(slots) ^ set(self.slots)
            
            if removed_slot:
                self.slot_removed = removed_slot.pop()
        
        self.slots = slots
        return self.slots

