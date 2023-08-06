class Something:

    def __init__(self, thing):
        self.thing = thing

    def rename_thing(self, new_name):
        self.thing = self._double_thing(new_name)

    @staticmethod
    def _double_thing(value):
        return value * 2

    def get_thing(self):
        return self.thing
