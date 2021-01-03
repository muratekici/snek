def get_head_coord(coord: tuple, direction: int) -> tuple:
    if direction % 2 == 0:  # Horizontal movement
        return (coord[0] + (direction - 1), coord[1])
    else:  # Vertical movement
        return (coord[0], coord[1] + (direction - 2))
