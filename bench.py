#!/usr/bin/env python3
from numpy import number
import pyperf
from pipes_v2.agent import blind_search, heuristic_search
from pipes_v2.utils.generate import generate_board
from pipes_v2.utils.image_proc import download_board

if __name__ == "__main__":
    runner = pyperf.Runner()
    board = generate_board(15, 15)
    runner.timeit(
        "blind search 15x15",
        "blind_search(board)",
        inner_loops=1,
        duplicate=1,
        globals=locals(),
    )
    runner.timeit(
        "heuristic search 15x15",
        "heuristic_search(board)",
        inner_loops=1,
        duplicate=1,
        globals=locals(),
    )
