from main import Morphy


@Morphy.register_node_type()
class Map(Morphy):
    def __init__(self, previous_self):
        super().__init__(previous_self)
