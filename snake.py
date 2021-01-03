import util


class Snake(object):
    snake_id = 0
    name = ''
    length = 0

    # A list of (x, y) coordinates. First is the head.
    placement = []

    def __init__(self, snake_id: int, name: str, placement: list) -> None:
        self.snake_id = snake_id
        self.name = name
        self.length = len(placement)
        self.placement = placement

    # Move, 0:left, 1:up, 2:right, 3:down
    def move(self, direction: int):
        self.placement = [util.get_head_coord(coord=self.placement[0], direction=direction)] + self.placement[:-1]

    def grow(self):
        x_diff = self.placement[-1][0] - self.placement[-2][0]
        y_diff = self.placement[-1][1] - self.placement[-2][1]

        self.placement.append(
            (self.placement[-1][0] + x_diff, self.placement[-1][1] + y_diff))
        self.length = len(self.placement)

    def __str__(self) -> str:
        snake_str = f'Id: {self.snake_id} - Name: {self.name} - Length: {self.length} - Placement: {self.placement}'
        return snake_str
