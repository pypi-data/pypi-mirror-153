"""
GeometryNode - a Python Class to govern the data and metadata of geometric data (Mesh, BIM, PCD)
"""

#IMPORT MODULES
import numpy as np
from geomapi.node import Node
import geomapi.utils as ut
import geomapi.geometryutils as gt
import open3d as o3d 
from rdflib import Graph, URIRef

class GeometryNode (Node):
    # class attributes

    def __init__(self,  graph: Graph = None, 
                        graphPath: str = None,
                        subject: URIRef = None,
                        **kwargs):
        """Creates a new Geometry

        Args:
            graph (Graph, optional): The RDF Graph to parse. Defaults to None.
            graphPath (str, optional): The path of the Graph. Defaults to None.
            subject (URIRef, optional): The subject to parse the Graph with. Defaults to None.
        """
                # set the graph and optional parameters
        super().__init__(   graph= graph,
                            graphPath= graphPath,
                            subject= subject,
                            kwargs = kwargs) 
        self.cartesianBounds=None     # (nparray [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]
        self.orientedBounds=None     # (nparray [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]
        self.oriendtedBoundingBox=None # (open3d.geometry.OrientedBoundingBox) 
        # self.features3d= None #o3d.registration.Feature() # http://www.open3d.org/docs/0.9.0/python_api/open3d.registration.Feature.html
    
    def get_bounding_box(self)->o3d.geometry.OrientedBoundingBox:
        """Gets the Open3D geometry from cartesianBounds or orientedBounds

        Returns:
            o3d.geometry.OrientedBoundingBox
        """
        if getattr(self,'oriendtedBoundingBox',None) is None:
            if getattr(self,'orientedBounds',None) is not None:
                self.oriendtedBoundingBox=gt.oriented_bounds_to_open3d_oriented_bounding_box(self.orientedBounds)
            elif getattr(self,'cartesianBounds',None) is not None:
                self.oriendtedBoundingBox=gt.cartesian_bounds_to_open3d_axis_aligned_bounding_box(self.cartesianBounds)        
            else:
                return None
        return self.oriendtedBoundingBox

    def get_center(self) -> np.ndarray:
        """Returns the center of the geometry coordinates.

        Returns:
            numpy.ndarray[numpy.float64[3, 1]]
        """        
        if getattr(self,'center',None) is None: 
            if getattr(self,'cartesianTransform',None) is not None: 
                self.center=gt.get_translation(self.cartesianTransform) 
            elif getattr(self,'cartesianBounds',None) is not None:
                self.center=gt.get_center_of_cartesian_bounds(self.cartesianBounds) 
            elif getattr(self,'mesh',None) is not None:
                self.center=self.mesh.get_center()
            elif getattr(self,'pcd',None) is not None:
                self.center=self.pcd.get_center()
            else:
                return None    
        return self.center    

    def visualize(self):
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        if getattr(self,'mesh',None) is not None:
            vis.add_geometry(self.mesh)
        elif getattr(self,'pcd',None) is not None:
            vis.add_geometry(self.pcd)
        else:
            return None
        vis.run()
        vis.destroy_window()