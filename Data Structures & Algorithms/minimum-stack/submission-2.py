class MinStack:

    def __init__(self):
        self.stack = []
        self.mn = float('inf')
        

    def push(self, val: int) -> None:
        self.stack.append(val)
        self.mn = min(self.mn, val)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.mn:
            if self.stack:
                self.mn = min(self.stack)
            else:
                self.mn = float('inf')

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        if self.stack:
            return self.mn
