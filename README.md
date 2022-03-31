# Pipes Solver

Requirements: newest versions of `numpy` (2d array representation), `request` (download board from the website) and `pillow` (read the downloaded image).

## main.py

```bash
$ python3 main.py -h
```

```txt
usage: main.py [-h] [-d] [-a {blind,heuristic,improved}] [-s SEED] [-u URL] width height

solve pipes puzzle with selected algorithm

positional arguments:
  width
  height

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug
  -a {blind,heuristic,improved}, --algorithm {blind,heuristic,improved}
  -s SEED, --seed SEED  if there's no url then generate random board. seed can be specified
                        for reproducibility
  -u URL, --url URL     download board from www.puzzle-pipes.com (please use dark mode and
                        copy screenshot link from share button). this take precedence over
                        --seed
```

## bench.py

Run benchmarks in `input` folder.

```bash
$ python3 bench.py
```

## demo.py

Simple algorithm walkthrough.