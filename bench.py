#!/usr/bin/env python3
import logging
import timeit
from numpy import number
from pipes_v2.agent import blind_search, improved_search, heuristic_search
from pipes_v2.utils.image_proc import download_board

logging.basicConfig(level=logging.INFO)
file_logger = logging.getLogger("file")
file_logger.addHandler(logging.FileHandler("bench_results.txt"))
file_logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    for size, number in [
        (5, 10),
        (10, 10),
        (15, 5),
        (20, 1),
        (25, 1),
        (30, 1),
        (40, 1),
    ]:
        with open("input/{0}x{0}.txt".format(size)) as file:
            for i, url in enumerate(file.read().splitlines()):
                board = download_board(url, size, size)
                for func in [blind_search, heuristic_search, improved_search]:
                    name = "{size}x{size}.{i}.{func: >16}".format(
                        size=size, i=i, func=func.__name__
                    )

                    runs = (
                        number if func.__name__ != improved_search.__name__ else number * 10
                    )

                    time = (
                        timeit.timeit(
                            "{func}(board)".format(func=func.__name__),
                            number=runs,
                            globals=locals(),
                        )
                        / runs
                    )
                    file_logger.info("{name}: {time:3.3f}".format(name=name, time=time))
