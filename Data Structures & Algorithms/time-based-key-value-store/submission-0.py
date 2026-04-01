class TimeMap:

    def __init__(self):
        self.keymap = {}
        

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.keymap:
            self.keymap[key] = {}
        if timestamp not in self.keymap[key]:
            self.keymap[key][timestamp] = []

        self.keymap[key][timestamp].append(value)
        

    def get(self, key: str, timestamp: int) -> str:
        seen = 0
        if key in self.keymap:
            for time in self.keymap[key]:
                if time <= timestamp:
                    seen = max(seen, time)
            if seen != 0:
                return self.keymap[key][seen][-1]
        
        return ""