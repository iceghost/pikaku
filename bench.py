#!/usr/bin/env python3
from numpy import number
import pyperf
from pipes_v2.agent import blind_search
from pipes_v2.image_proc import download_board

if __name__ == "__main__":
    runner = pyperf.Runner()
    with open("input/15x15.txt") as file:
        for i, url in enumerate(file.read().splitlines()):
            board = download_board(url, 15, 15)
            runner.bench_func(
                "#{}: blind search 15x15".format(i),
                blind_search,
                board,
                inner_loops=1,
            )
