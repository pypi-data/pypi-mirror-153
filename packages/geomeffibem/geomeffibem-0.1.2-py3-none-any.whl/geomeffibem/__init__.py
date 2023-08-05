"""Top-level package for GeomEffiBEM."""

__author__ = """Julien Marrec"""
__email__ = 'contact@effibem.com'
__version__ = '0.1.2'

from geomeffibem.plane import Plane
from geomeffibem.polyhedron import Polyhedron
from geomeffibem.surface import Surface, Surface3dEge, plot_vertices
from geomeffibem.vertex import Vertex, distance, distanceFromPointToLine, isAlmostEqual3dPt
