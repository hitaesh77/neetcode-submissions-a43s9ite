class LRUCache:

    def __init__(self, capacity: int):
        self.cache = {}
        self.lru = deque()
        self.capacity = capacity
        

    def get(self, key: int) -> int:
        if key in self.cache:
            self.lru.remove(key)
            self.lru.append(key)
            return self.cache[key]
        else:
            return -1
        
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.lru.remove(key)
            self.lru.append(key)
        else:
            if len(self.cache) == self.capacity:
                temp = self.lru.popleft()
                del self.cache[temp]

            self.lru.append(key)
            self.cache[key] = value

                
        
