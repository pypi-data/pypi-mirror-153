import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()

from .hypergraph_layout import *
from .our_layout import *
