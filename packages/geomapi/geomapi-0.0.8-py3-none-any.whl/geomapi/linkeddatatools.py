"""
linkeddatatools - a Python library for RDF graph structuring and exchange.
"""
#IMPORT PACKAGES
from lib2to3.pytree import Node
import numpy as np 
import cv2 
import open3d as o3d 
import os 
import re
import pye57 #conda install xerces-c  =>  pip install pye57
import xml.etree.ElementTree as ET 
from typing import List

# import APIs
import rdflib
from rdflib import Graph, plugin
from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util
from ifcopenshell.util.selector import Selector

#IMPORT MODULES watch out for circular imports
from geomapi.node import Node
from geomapi.pointcloudnode import PointCloudNode
from geomapi.meshnode import MeshNode
from geomapi.imagenode import ImageNode
from geomapi.bimnode import BIMNode
from geomapi.sessionnode import SessionNode

import geomapi.utils as ut
import geomapi.geometryutils as gt
import geomapi.geometryutils2 as gt2

from warnings import warn

#### NODE CREATION ####

def e57xml_to_nodes(e57XmlPath :str, **kwargs) -> List[PointCloudNode]:
    """Parse XML file that is created with E57lib e57xmldump.exe

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    try:
        #E57 XML file structure
        #e57Root
        #   >data3D
        #       >vectorChild
        #           >pose
        #               >rotation
        #               >translation
        #           >cartesianBounds
        #           >guid
        #           >name
        #           >points recordCount
        #   >images2D
        mytree = ET.parse(e57XmlPath)
        root = mytree.getroot()  
        nodelist=[]   
        e57Path=e57XmlPath.replace('.xml','.e57')       

        for idx,e57node in enumerate(root.iter('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}vectorChild')):
            nodelist.append(PointCloudNode(e57XmlPath=e57XmlPath,e57Index=idx,e57Path=e57Path,**kwargs))
        return nodelist
    except:
        print('xmlPath not recognized. Please run .\e57xmldump on target e57 files and store output xml files somewhere in session folder. If formatting error occurs, manually remove <?xml version="1.0" encoding="UTF-8"?> from xml file.')
        return None

def img_xml_to_nodes(xmlPath :str, **kwargs) -> List[ImageNode]:
    """Parse XML file that is created with https://www.agisoft.com/

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    try:
        mytree = ET.parse(xmlPath)
        root = mytree.getroot()  
        nodelist=[]   
        for idx,item in enumerate(root.iter('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}vectorChild')):
            nodelist.append(ImageNode(xmlPath=xmlPath,xmlIndex=idx,**kwargs))
        return nodelist
    except:
        print('xml parsing error')
        return None

def e57header_to_nodes(e57Path:str, **kwargs) -> List[PointCloudNode]:
    """
    Parse e57 file header that is created with E57lib e57xmldump.exe

    Args:
        path (string):  e57 xml file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
            
    Returns:
        A list of pointcloudnodes with the xml metadata 
    """
    try:
        nodelist=[]   
        e57 = pye57.E57(e57Path)   
        for idx in range(e57.scan_count):
            nodelist.append(PointCloudNode(e57Path=e57Path,e57Index=idx, **kwargs))
        return nodelist
    except:
        print('e57header error')
        return None

def ifc_to_nodes(ifcPath:str, classes:str='ifcElement',getGeometry=True,**kwargs)-> List[BIMNode]:
    """
    Parse ifc file to a list of BIMNodes, one for each ifcElement

    Args:
        path (string):  ifc file path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\PCD\\week 22 lidar_CC.xml"
        classes (string): ifcClasses seperated by | e.g. '.IfcWall | .IfcSlab'    
    Returns:
        A list of BIMNodes  
    """   
    try:
        nodelist=[]   
        ifc = ifcopenshell.open(ifcPath)   
        selector = Selector()
        for ifcElement in selector.parse(ifc, classes): 
            try:   
                node=BIMNode(ifcElement=ifcElement,ifcPath=ifcPath,getGeometry=getGeometry, **kwargs)
                if getattr(node,'mesh',None) is not None and len(node.mesh.triangles) !=0:
                    node.get_metadata_from_mesh()
            except:
                print('Node creation error')
                continue
            # if node.set_metadata_from_ifc_element(ifcElement):
            nodelist.append(node)
        return nodelist
    except:
        print('IfcOpenShell import error')
        return None

##### NODE SELECTION #####

def select_k_nearest_nodes(node:Node,nodelist:List[Node],k:int=10) -> List [Node]:
    """ Select k nearest nodes based on Euclidean distance between centroids

    .. image:: ../pics/selection_k_nearest.PNG

    Args:
        node (Node):
        nodelist (List[Node]): 
        k (int, optional): number of neighbors. Defaults to 10.

    Returns:
        List [Node]: 
    """
    #get node center
    if node.get_center() is not None:
        point=node.center
        #create pcd from nodelist centers
        pcd = o3d.geometry.PointCloud()
        array=np.empty(shape=(len(nodelist),3))
        for idx,node in enumerate(nodelist):
            node.get_center()
            if getattr(node,'center',None) is not None: 
                array[idx]=node.center   
            else:
                array[idx]=[-1000.0,-1000.0,-1000.0]
        pcd.points = o3d.utility.Vector3dVector(array)

        #Create KDTree from pcd
        pcdTree = o3d.geometry.KDTreeFlann(pcd)

        #Find 200 nearest neighbors
        [k1, idxList, _] = pcdTree.search_knn_vector_3d(point, k)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]

        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None

def select_nodes_with_centers_in_radius(node:Node,nodelist:List[Node],r:float=0.5) -> List [Node]:
    """Select nodes within radius of the node centroid based on Euclidean distance between node centroids

    .. image:: ../pics/selection_radius_nearest.PNG
    
    Args:
        node (Node): 
        nodelist (List[Node]):
        r (float, optional): radius to search. Defaults to 0.5m.

    Returns:
        List [Node]: 
    """
    #get node center
    if node.get_center() is not None:
        point=node.center
        #create pcd from nodelist centers
        pcd = o3d.geometry.PointCloud()
        array=np.empty(shape=(len(nodelist),3))
        for idx,node in enumerate(nodelist):
            node.get_center()
            if getattr(node,'center',None) is not None: 
                array[idx]=node.center 
            else:
                array[idx]=[-1000.0,-1000.0,-1000.0]
        pcd.points = o3d.utility.Vector3dVector(array)

        #Create KDTree from pcd
        pcdTree = o3d.geometry.KDTreeFlann(pcd)

        #Find 200 nearest neighbors
        [k1, idxList, _] = pcdTree.search_radius_vector_3d(point, r)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]

        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None

def select_nodes_with_centers_in_bounding_box(node:Node,nodelist:List[Node],u:float=0.5,v:float=0.5,w:float=0.5) -> List [Node]: 
    """Select the nodes of which the center lies within the oriented Bounding Box of the source node given an offset

    .. image:: ../pics/selection_box_inliers.PNG
    
    Args:
        node (Node): source Node
        nodelist (List[Node]): target nodelist
        u (float, optional): Offset in X. Defaults to 0.5.
        v (float, optional): Offset in Y. Defaults to 0.5.
        w (float, optional): Offset in Z. Defaults to 0.5.

    Returns:
        List [Node]
    """
    #get box source node
    if node.get_bounding_box() is not None:
        box=node.oriendtedBoundingBox
        box=gt.expand_box(box,u=u,v=v,w=w)

        # get centers
        centers=np.empty((len(nodelist),3),dtype=float)
        for idx,node in enumerate(nodelist):
            centers[idx]=node.get_center()

        #points are the centers of all the nodes
        pcd = o3d.geometry.PointCloud()
        points = o3d.utility.Vector3dVector(centers)
        pcd.points=points

        # Find the nodes that lie within the index box 
        idxList=box.get_point_indices_within_bounding_box(points)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None

def select_nodes_with_bounding_points_in_bounding_box(node:Node,nodelist:List[Node],u:float=0.5,v:float=0.5,w:float=0.5) -> List [Node]: 
    """Select the nodes of which atleast one of the bounding points lies within the oriented Bounding Box of the source node given an offset.

    .. image:: ../pics/selection_BB_intersection.PNG
    
    Args:
        node (Node): source Node
        nodelist (List[Node]): target nodelist
        u (float, optional): Offset in X. Defaults to 0.5.
        v (float, optional): Offset in Y. Defaults to 0.5.
        w (float, optional): Offset in Z. Defaults to 0.5.

    Returns:
        List [Node]
    """
    #get box source node
    if node.get_bounding_box() is not None:
        box=node.oriendtedBoundingBox
        box=gt.expand_box(box,u=u,v=v,w=w)

        # get boxes nodelist
        boxes=np.empty((len(nodelist),1),dtype=o3d.geometry.OrientedBoundingBox)
        for idx,node in enumerate(nodelist):
            boxes[idx]=node.get_bounding_box()

        # Find the nodes of which the bounding points lie in the source node box
        idxList=gt.get_box_inliers(box,boxes)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None
    
def select_nodes_with_intersecting_bounding_box(node:Node,nodelist:List[Node],u:float=0.5,v:float=0.5,w:float=0.5) -> List [Node]: 
    """Select the nodes of which the bounding boxes intersect

    .. image:: ../pics/selection_BB_intersection2.PNG

    Args:
        node (Node): source Node
        nodelist (List[Node]): target nodelist
        u (float, optional): Offset in X. Defaults to 0.5.
        v (float, optional): Offset in Y. Defaults to 0.5.
        w (float, optional): Offset in Z. Defaults to 0.5.

    Returns:
        List [Node]
    """
    #get box source node
    if node.get_bounding_box() is not None:
        box=node.oriendtedBoundingBox
        box=gt.expand_box(box,u=u,v=v,w=w)

        # get boxes nodelist
        boxes=np.empty((len(nodelist),1),dtype=o3d.geometry.OrientedBoundingBox)
        for idx,node in enumerate(nodelist):
            boxes[idx]=node.get_bounding_box()
        
        # Find the nodes of which the bounding box itersects with the source node box
        idxList=gt.get_box_intersections(box,boxes)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    else:
        return None

def select_nodes_with_intersecting_meshes(node:Node,nodelist:List[Node]) -> List [Node]: 
    """Select the nodes of which the o3d.geometry.TriangleMeshes intersect
    This method relies on trimesh and fcl libraries for collision detection

    .. image:: ../pics/collision_5.PNG

    Args:
        node (Node): source Node
        nodelist (List[Node]): target nodelist

    Returns:
        List [Node]: 
    """
    #get geometry source node
    if getattr(node,'get_mesh',None) is not None and node.get_mesh() is not None: 
        # get geometries nodelist        
        meshes=np.empty((len(nodelist),1),dtype=o3d.geometry.TriangleMesh)
        for idx,testnode in enumerate(nodelist):
            if getattr(testnode,'get_mesh',None) is not None and testnode.get_mesh() is not None: 
                    meshes[idx]=testnode.mesh

        # Find the nodes of which the geometry itersects with the source node box
        idxList=gt2.mesh_collisions_trimesh(node.mesh,meshes)
        selectedNodeList=[node for idx,node in enumerate(nodelist) if idx in idxList]
        if any(selectedNodeList):        
            return selectedNodeList
    return None

#### GRAPH CREATION #####

def nodes_to_graph(nodelist : List[Node]) -> Graph:
    """ Convert list of nodes to a graph"""
    g=Graph()
    g=ut.bind_ontologies(g)
    for idx,node in enumerate(nodelist):
        try:
            node.to_graph()
            g+=node.graph
        except:
            print('Node '+str(idx)+' could not be serialized.')
            continue
    return g  

#### OBSOLETE #####

def graph_to_nodes(graph : Graph,**kwargs) -> List[Node]:
    """Convert a graph to a set of Nodes

    Args:
        graph (RDFlib.Graph):  Graph to parse
        sessionPath (str): folder path of the graph 

    Returns:
        A list of pointcloudnodes, imagenodes, meshnodes, bimnodes, orthonodes with metadata 
    """
    warn("This function is depricated use a SessionNode instead")
    nodelist=[]
    for subject in graph.subjects(RDF.type): #iterate over subjects
        #create correct nodeType
        node=subject_to_node_type(graph,subject,**kwargs)
        node.name = str(subject).replace('http://','') 
        node.graph = Graph()
        node.graph += graph.triples((subject, None, None))

        for predicate,object in graph.predicate_objects(subject):# iterate over all predicates of a subject
            attr=ut.predicate_to_attribute(predicate)
            
            #GEOMETRY
            if attr == 'cartesianBounds':
                node.cartesianBounds=ut.literal_to_cartesianBounds(graph.value(subject=subject,predicate=predicate)) 
            elif attr == 'orientedBounds':
                node.orientedBounds=ut.literal_to_orientedBounds(graph.value(subject=subject,predicate=predicate)) 
            elif attr == 'cartesianTransform':
                node.cartesianTransform=ut.literal_to_cartesianTransform(graph.value(subject=subject,predicate=predicate))
            elif attr == 'geospatialTransform':
                node.geospatialTransform=ut.literal_to_geospatialTransform(graph.value(subject=subject,predicate=predicate))
            #PATHS
            elif re.search('path', attr, re.IGNORECASE):
                path=ut.literal_to_string(graph.value(subject=subject,predicate=predicate))
                if path is not None:
                    if getattr(node,'sessionPath',None) is not None:
                        setattr(node,attr,(node.sessionPath+'\\'+path)) 
                    elif getattr(node,'graphPath',None) is not None:
                        setattr(node,attr,(node.graphPath+'\\'+path)) 
                    else:
                        setattr(node,attr,(os.getcwd()+'\\'+path)) 
            #INT    
            elif attr in ['recordCount','faceCount','label','e57Index','imageWidth','imageHeight','resolutionUnit']:
                setattr(node,attr,ut.literal_to_int(object)) 
            #FLOAT
            elif attr in ['xResolution','yResolution','focalLength35mm','principalPointU','principalPointV','accuracy']:
                setattr(node,attr,ut.literal_to_float(object)) 
            #ARRAYS
            elif attr in ['hasBIM','hasCAD','hasPcd','hasMesh','hasImg','hasOrtho','hasChild','hasParent','distortionCoeficients']:
                setattr(node,attr,ut.literal_to_list(object)) 
            #LISTS   
            elif attr in ['linkedNodes']:
                setattr(node,attr,ut.literal_to_uriref(object)) 
            #STRINGS
            else:
                setattr(node,attr,object.toPython()) # this solely covers string
        nodelist.append(node)
    return nodelist

def subject_to_node_type(graph: Graph , subject:URIRef, **kwargs)-> Node:
    warn("This function is depricated use a SessionNode instead")
    nodeType = ut.literal_to_string(graph.value(subject=subject,predicate=RDF.type))
    g = Graph()
    g += graph.triples((subject, None, None))
    if 'BIMNode' in nodeType:
        node=BIMNode(graph=g,**kwargs)
    elif 'MeshNode' in nodeType:
        node=MeshNode(graph=g,**kwargs)
    elif 'PointCloudNode' in nodeType:
        node=PointCloudNode(graph=g,**kwargs)
    elif 'ImageNode' in nodeType:
        node=ImageNode(graph=g,**kwargs)
    elif 'SessionNode' in nodeType:
        node=SessionNode(graph=g,**kwargs)  
    else:
        node=Node(graph=g,**kwargs) 
    return node

def get_linked_nodes(node: Node ,graph:Graph, getGeometry=False, **kwargs) -> List[Node]:
    """Get related nodes based on linkedNodes variable

    Returns:
        List[Node]: List of linked Nodes
    """
    warn("This function is depricated use a SessionNode instead")
    nodelist=[]
    if getattr(node,'linkedNodes',None) is not None:  
        for subject in node.linkedNodes:
            if graph.value(subject=subject,predicate=RDF.type) is not None:
                nodelist.append(subject_to_node_type(graph=graph,subject=subject, getGeometry=getGeometry, **kwargs)) 
    return nodelist