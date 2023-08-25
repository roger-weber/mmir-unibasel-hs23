from IPython.display import Markdown, display
from tabulate import tabulate
from itertools import islice
import builtins

def print(rows: list[list[str]], headers: list[str], max_rows: int = 20):
    if not rows or not headers: return
    # display(Markdown(tabulate(islice(rows, max_rows), headers, tablefmt="pipe")))
    builtins.print(tabulate(islice(rows, max_rows), headers, tablefmt="github"))

