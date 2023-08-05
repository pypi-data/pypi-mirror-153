"""
MeshNode - a Python Class to govern the data and metadata of mesh data (Open3D, RDF)
"""
#IMPORT PACKAGES
import open3d as o3d 
import numpy as np 
from rdflib import Graph, URIRef
import uuid    
import os

#IMPORT MODULES
from geomapi.geometrynode import GeometryNode
import geomapi.utils as ut
import geomapi.geometryutils as gt

class MeshNode (GeometryNode):
    # class attributes
    

    def __init__(self,  graph : Graph = None, 
                        graphPath:str=None,
                        subject : URIRef = None,
                        path : str=None, 
                        getGeometry : bool = False,
                        mesh:o3d.geometry.TriangleMesh = None, 
                        **kwargs): 
        """
        Creates a MeshNode. Overloaded function.

        Args:
            0.graph (RDFlib Graph) : Graph with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)
            
            1.graphPath (str):  Graph file path with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)

            2.path (str) : path to .obj or .ply file (Note that this node will also contain the data)

            3.mesh (o3d.geometry.TriangleMesh) : Open3D TriangleMesh (Note that this node will also contain the data)
                
        Returns:
            A MeshNode with metadata (if you also want the data, call node.get_geometry() method)
        """   
        #instance attributes        
        super().__init__(graph, graphPath, subject)     
        self.path=path   
        self.pointCount = None # (int) 
        self.faceCount = None # (int) 
        self.mesh = mesh 
        # self.guid='{'+str(uuid.uuid1())+'}'     
        self.__dict__.update(kwargs)

        if mesh is not None: #data + metadata
            if type(mesh) is o3d.geometry.TriangleMesh and len(mesh.triangles) >=2:
                self.get_metadata_from_mesh()
            else:
                raise ValueError('Mesh must be o3d.geometry.TriangleMesh and len(mesh.triangles) >=2')
        
        if path is not None:
            if path.endswith('.obj') or path.endswith('.ply'): #data + metadata
                self.name=ut.get_filename(path)
                self.timestamp=ut.get_timestamp(path)                
                self.get_metadata_from_mesh()
            else:
                raise ValueError('file must be .obj or .ply')
        
        if getGeometry:
            self.get_geometry()

    def clear_geometry(self):
        """Clear all geometries in the Node.
        """
        if getattr(self,'mesh',None) is not None:
            self.mesh=None

    def get_mesh(self) -> o3d.geometry.TriangleMesh:
        """Returns the mesh data in the node. If none is present, it will search for the data on drive.

        Returns:
            o3d.geometry.TriangleMesh or None
        """
        if getattr(self,'mesh',None) is not None and len(self.mesh.triangles)>1:
            return self.mesh 
        elif self.get_geometry():
            return self.mesh
        return None  

    def get_geometry(self)->bool: # deze class is gedeeld met de mesh class
        """
        get o3d.geometry.TriangleMesh from self.path or self.name
        """
        if getattr(self,'mesh',None) is None:
            if getattr(self,'path',None) is not None and os.path.exists(self.path) :
                mesh = o3d.io.read_triangle_mesh(self.path)
                if len(mesh.vertices) != 0:
                    self.mesh=mesh
                    return True

            if getattr(self,'name',None) is not None and getattr(self,'sessionPath',None) is not None:
                allSessionFilePaths=ut.get_list_of_files(self.sessionPath)
                testOBJPath= self.sessionPath +'\\'+ self.name + '.obj'
                testPLYPath= self.sessionPath + '\\'+ self.name + '.ply'
                if testOBJPath in allSessionFilePaths:
                    mesh = o3d.io.read_triangle_mesh(testOBJPath)  
                    if len(mesh.vertices) != 0:
                        self.path=testOBJPath
                        self.mesh=mesh
                        return True
                elif testPLYPath in allSessionFilePaths:
                    mesh = o3d.io.read_triangle_mesh(testPLYPath)  
                    if len(mesh.vertices) != 0:
                        self.path=testPLYPath
                        self.mesh=mesh
                        return True
        elif getattr(self,'mesh',None) is not None:
            if len(self.mesh.triangles)>1:
                return True
        return False
 
    def get_metadata_from_mesh(self) -> bool:
        self.get_geometry()
        if getattr(self,'mesh',None) is not None and len(self.mesh.triangles) >1:
            try:
                center=self.mesh.get_center()  
                self.cartesianTransform= np.array([[1,0,0,center[0]],
                                                    [0,1,0,center[1]],
                                                    [0,0,1,center[2]],
                                                    [0,0,0,1]])
                self.faceCount= len(self.mesh.triangles)
                self.pointCount= len(self.mesh.vertices)            
                self.cartesianBounds=gt.get_cartesian_bounds(self.mesh)
                self.orientedBounds = gt.get_oriented_bounds(self.mesh)
            except:
                pass
            return True
        else:
            print('No proper geometries found to extract the metadata. len(self.mesh.triangles) >1')
            return False
    
    def set_mesh(self, mesh): 
        self.mesh = mesh

    def set_path(self,path:str=None):
        if getattr(self, 'path',None) is None:        
            if getattr(self, 'graphPath',None) is not None:
                folder=ut.get_folder(self.graphPath)
            else:
                folder=ut.get_folder(os. getcwd())

            if getattr(self,'name',None) is not None:            
                self.path=folder+'\\'+self.name+'.pcd'
            elif getattr(self,'guid',None) is not None:         
                self.path=folder+'\\'+self.guid+'.pcd'
            else:
                self.path=folder+'\\'+str(uuid.uuid1()) +'.pcd'
        else:
            self.path=path
