#!/usr/bin/env python3
import argparse
import logging
from pipes_v2.agent import blind_search, heuristic_search, improved_search
from pipes_v2.board import Board
from pipes_v2.utils.generate import generate_board
from pipes_v2.utils.image_proc import download_board
import timeit


def solve(board: Board, search_algorithm):
    state = search_algorithm(board)
    if state is None:
        raise
    logging.info("Result:\n{}".format(state.joints))


parser = argparse.ArgumentParser(
    description="solve pipes puzzle with selected algorithm"
)
parser.add_argument("width", type=int)
parser.add_argument("height", type=int)
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument(
    "-a",
    "--algorithm",
    choices=["blind", "heuristic", "improved"],
    default="improved",
)
parser.add_argument(
    "-s",
    "--seed",
    help="if there's no url then generate random board. seed can be specified for reproducibility",
)
parser.add_argument(
    "-u",
    "--url",
    help="""download board from www.puzzle-pipes.com
(please use dark mode and copy screenshot link from share button). this take precedence over --seed""",
)
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

board = None
if args.url is not None:
    board = download_board(
        args.url,
        args.height,
        args.width,
    )
else:
    board = generate_board(args.height, args.width, args.seed)

logging.info(
    "time taken: {}".format(
        timeit.timeit(
            "solve(board, {alg}_search)".format(alg=args.algorithm),
            number=1,
            globals=locals(),
        )
    )
)
