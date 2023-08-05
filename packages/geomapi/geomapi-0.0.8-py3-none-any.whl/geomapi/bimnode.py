"""
BIMNode - a Python Class to govern the data and metadata of BIM data (Open3D, RDF)
"""
#IMPORT PACKAGES
from ast import Raise
import open3d as o3d 
import numpy as np 
from rdflib import Graph, URIRef
import os
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util
#IMPORT MODULES
from geomapi.geometrynode import GeometryNode
import geomapi.utils as ut
import geomapi.geometryutils as gt


class BIMNode (GeometryNode):
    """
    This class stores a BIMNode, including the metadata from an ifcElement (OpenShell) and the data from the mesh geometry (Open3D)
    
    Goals:
    - Given a path, import all the linked resources including images, meshes, ect.
    - Convert non-RDF metadata files (.ifc, .obj, ect..) to BIMNodes and export them to RDF
    - use URIRef() to reference the node, ect...
    """
    # class attributes
    # ifcPath = None # (string) path to an ifc file
    # globalId=None # (string) ifc guid of the element e.g. 2DhaSlBmz2puIzqaWbJt0S
    # className=None #(string) ifcElement class e.g. ifcWall
    # mesh = None # (o3d.mesh) mesh geometry of the ifcElement (MB)
    # ifcElement = None # (ifcopenshell.entity_instance)  Don't store an ifcElement in your node. it can't be properly passed around
    # self.path = None # (string) path of the o3d.mesh geometry
    # self.ifc = None # (string) path to an ifc file => you don't want to store the entire ifc file!
    # self.ifcElement = None # (string) 
    # self.pcds = None #(List[URIRef]) => link to other pcd. 
    
    #Classification
    # self.label = None #(string) ??? (MB)
    # self.meshes = None # (List[URIRef]) => link to other meshes. (MB)
    
    #Geometry
    
    # # Monitoring
    # self.phase = None # (string) ??? this can't be really extracted from the IFC (MB)
    # self.progress = None # (double [0.0;1.0]) percentage of completion
    # self.quality = None # ([%LOA30,#LOA20,#LOA10]) inliers Level-of-Accuracy (LOA)
    # self.deviation = None # (np.array(4,4)) cartesian transform 
    # self.cracks = None # (bool) True if cracks are detected on the image texture

    #Questions
    # is phase and timestamp the same?
    # monenclature
    # where do we store the image masks?
    # do we also need a CAD node?

    def __init__(self,  graph : Graph = None, 
                        graphPath: str= None,
                        subject : URIRef = None,
                        path : str= None, 
                        mesh: o3d.geometry.TriangleMesh = None,
                        ifcPath : str = None,                        
                        globalId : str = None,
                        className : str = None, 
                        ifcElement : ifcopenshell.entity_instance = None,
                        getResource : bool = False,
                        **kwargs): 
        """Overloaded function.

        Args:
            0.graph (RDFlib Graph) : RDF Graph with a single subject. if no subject is present, the first subject in the Graph will be used to initialise the Node.
            
            1.graphPath (str)  + (optional) subject:  RDF Graph file path with a subject. if no subject is present, the first subject in the Graph will be used to initialise the Node.

            2.path (str) : path to .obj or .ply file (Note that this node will also contain the data)

            3.mesh (o3d.geometry.TriangleMesh) : Open3D TriangleMesh (Note that this node will also contain the data)

            4.ifcPath (str) + globalId (str) + (optional) getGeometry: (Note that this node will also contain the data)

            5.ifcElement (ifcopenshell.entity_instance) :  Warning, never attach an IfcElement to a node directly as this is very unstable!
                
        Returns:
            A BIMNode with metadata (if you also want the data, call node.get_resource() method)
        """   
        # set the graph and optional parameters
        super().__init__(   graph= graph,
                            graphPath= graphPath,
                            subject= subject,
                            kwargs = kwargs) 
        self.path=path
        self.mesh=mesh
        self.ifcName = None
        self.ifcPath=ifcPath
        self.globalId=globalId
        self.className=className

        if graph is not None: 
            if type(graph) is Graph : #metadata
                self.get_metadata_from_graph() 
            else:
                raise ValueError('graph must be RDF Graph')
     
        elif graphPath is not None:  #metadata
            if graphPath.endswith('.ttl'):
                self.timestamp=ut.get_timestamp(graphPath)
                self.get_metadata_from_graph_path() 
            else:
                raise ValueError('file must be .ttl')

        elif mesh is not None: #data + metadata
            if type(mesh) is o3d.geometry.TriangleMesh and len(mesh.triangles) >=2:
                self.get_metadata_from_mesh()
            else:
                raise ValueError('Mesh must be o3d.geometry. TriangleMesh and len(mesh.triangles) >=2')
        
        elif path is not None:
            if path.endswith('.obj') or path.endswith('.ply'): #data + metadata
                self.name=ut.get_filename(path)
                self.timestamp=ut.get_timestamp(path)                
                self.get_metadata_from_mesh()
            else:
                raise ValueError('file must be .obj or .ply')
        
        elif ifcPath is not None and globalId is not None:  #metadata
            if ifcPath.endswith('.ifc'):
                self.timestamp=ut.get_timestamp(ifcPath)
                self.get_metadata_from_ifc(getResource)
            else:
                raise ValueError('file must be .ifc and globalId not None')

        elif ifcElement is not None:
            if type(ifcElement) is ifcopenshell.entity_instance:  #metadata
                self.get_metadata_from_ifcElement(ifcElement,getResource)
            else:
                raise ValueError('type(ifcElement) must be ifcopenshell.entity_instance')

        if getResource:
            self.get_resource()

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
        elif self.get_resource():
            return self.mesh
        return None  

    def get_resource(self)->bool: 
        """
        get o3d.geometry.TriangleMesh from self.path or self.name
        """
        if getattr(self,'mesh',None) is None:
            self.mesh = o3d.io.read_triangle_mesh(self.get_resource_path(fileFormat=ut.MESH_EXTENSION))
                
            if getattr(self,'ifcPath',None) is not None and getattr(self,'globalId',None) is not None :
                try:
                    ifc = ifcopenshell.open(self.ifcPath)   
                    ifcElement= ifc.by_guid(self.globalId)
                    self.mesh=gt.ifc_to_mesh(ifcElement)
                    return True
                except:
                    pass
        elif getattr(self,'mesh',None) is not None:
            if len(self.mesh.triangles)>1:
                return True
        return False
 
    def export_geometry (self, extension = '.ply') ->bool:
        """_summary_

        Args:
            extension (str, optional): file extension. Defaults to '.ply'.

        Raises:
            ValueError: only .ply or .obj are allowed

        Returns:
            bool: return True if export was succesful
        """        
        #check path
        if getattr(self,'mesh',None) is not None:
            if getattr(self,'path',None) is not None and os.path.exists(self.path):
                pass
            else:
                #check name
                if getattr(self,'name',None) is not None:
                    self.name=ut.check_string_validity(self.name)
                else:
                    self.name=self.guid

                #check session/graphPath and directory
                if getattr(self,'sessionPath',None) is not None :
                    if os.path.exists((self.sessionPath +'\\BIM') ):
                        dir=self.sessionPath +'\\BIM'
                    else:
                        dir=os.mkdir((self.sessionPath+'\\BIM'))
                elif getattr(self,'graphPath',None) is not None: 
                    if os.path.exists(self.graphPath +'\\BIM' ):
                        dir=self.graphPath +'\\BIM'
                    else:
                        dir=os.mkdir((self.graphPath+'\\BIM'))                    
                else:
                    if os.path.exists((os.getcwd()+'\\BIM' )):
                        dir=os.getcwd()+'\\BIM'
                    else:
                        dir=os.mkdir((os.getcwd()+'\\BIM'))
                                    
                #check extension
                if extension == '.ply' or extension == '.obj':
                    self.path=dir+'\\'+self.name+extension
                else:
                    raise ValueError ('only .ply or .obj allowed') 
            try:
                o3d.io.write_triangle_mesh(self.path, self.mesh)
                return True
            except:
                print("Export failed of " + self.name )
        return False

    def get_metadata_from_mesh(self) -> bool:
        self.get_resource()
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
    
    def get_metadata_from_ifc(self, getGeometry = False) -> bool:
        try:
            ifc = ifcopenshell.open(self.ifcPath)   
            ifcElement= ifc.by_guid(self.globalId)
            self.ifcName=ifcElement.Name 
            if getattr(self,'ifcName',None) is not None:
                self.name=ut.check_string_validity(self.ifcName)
            self.className=ifcElement.is_a()
            if getGeometry:
                self.mesh=gt.ifc_to_mesh(ifcElement)
        except:
            print('IFC error')
            return False

    def get_metadata_from_ifcElement(self,ifcElement:ifcopenshell.entity_instance, getGeometry = False) -> bool:
        try:  
            self.ifcName=ifcElement.Name
            if getattr(self,'ifcName',None) is not None:
                self.name=ut.check_string_validity(self.ifcName)
            self.className=ifcElement.is_a()
            self.globalId=ifcElement.GlobalId
            if getGeometry:
                self.mesh=gt.ifc_to_mesh(ifcElement)
        except:
            print('ifcElement error')
            return False
