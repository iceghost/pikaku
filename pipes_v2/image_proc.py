from PIL import Image
import numpy
import requests

from pipes_v2.board import Board, PipeType


def image_from_url(url):
    response = requests.get(url, stream=True)
    return Image.open(response.raw)


def convert_bw(image: Image.Image):
    return image.convert("L").point(lambda x: 0 if x < 250 else 255, "1")


CORNER_OFFSET = 41
TILE_SIZE = 40
THICKNESS = 2


def generate_tiles(image: Image.Image, height, width):
    for row in range(0, height):
        for col in range(0, width):
            x = CORNER_OFFSET + (TILE_SIZE + THICKNESS) * col
            y = CORNER_OFFSET + (TILE_SIZE + THICKNESS) * row
            yield image.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))


def categorize_tile(tile: Image.Image):
    positions = [
        (TILE_SIZE // 2, TILE_SIZE // 5),
        (4 * TILE_SIZE // 5, TILE_SIZE // 2),
        (TILE_SIZE // 2, 4 * TILE_SIZE // 5),
        (TILE_SIZE // 5, TILE_SIZE // 2),
    ]
    has_pipes = [*map(
        lambda pos: tile.getpixel(pos) == 255,
        positions
    )]
    if sum(has_pipes) == 1:
        return PipeType.End
    if sum(has_pipes) == 3:
        return PipeType.Split
    if sum(has_pipes) == 2:
        if (has_pipes[0] and has_pipes[2]) or (has_pipes[1] and has_pipes[3]):
            return PipeType.Long
        return PipeType.Corner
    raise


def download_board(url, height, width):
    image = image_from_url(url)
    image = convert_bw(image)
    return Board(numpy.array([*map(
        categorize_tile,
        generate_tiles(image, height, width)
    )]).reshape((height, width)))
