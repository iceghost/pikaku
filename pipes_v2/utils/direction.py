def dir_to_dx_dy(dir: int):
    """
    Convert direction to displacement, following this convention:
    - 0 is top
    - 1 is right
    - 2 is bottom
    - 3 is left
    """
    if dir % 2 == 0:
        # map 0 -> ( 0, -1) (top)
        #     2 -> ( 0,  1) (bottom)
        return 0, dir - 1
    else:
        #     1 -> ( 1,  0) (right)
        #     3 -> (-1,  0) (left)
        return 2 - dir, 0
