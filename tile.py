class Tile:
    def __init__(self, image, collision):
        self.image = image
        self.rect = image.get_rect()
        self.collision = collision