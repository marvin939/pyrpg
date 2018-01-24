class World:
    def __init__(self):
        self.entities = list()

    def add_entity(self, entity):
        entity.world = self
        self.entities.append(entity)

    def update(self, seconds_passed):
        for entity in self.entities:
            entity.update(seconds_passed)
