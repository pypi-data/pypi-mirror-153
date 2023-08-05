
from rdflib import Graph, URIRef, Literal
import rdflib
from rdflib.namespace import RDF

#IMPORT MODULES
from geomapi.node import Node
from geomapi.pointcloudnode import PointCloudNode
from geomapi.meshnode import MeshNode
from geomapi.imagenode import ImageNode
from geomapi.bimnode import BIMNode
from geomapi.geometrynode import GeometryNode
import geomapi.utils as ut

class SessionNode(Node):
    """
    This class stores a full session, including all the images and meshes
    
    Goals:
    - Given a path, import all the linked images, meshes, ect... into a session class
    - Convert non-RDF metadata files (json, xml, ect..) to SessionsNodes and export them to RDF
    - get the boundingbox of the whole session
    - use URIRef() to reference the images ect...
    """

    def __init__(self,  graph: Graph = None, 
                        graphPath: str = None,
                        subject: URIRef = None):
        """Creates a new session node & all the child nodes

        Args:
            graph (Graph, optional): The RDF Graph to parse. Defaults to None.
            graphPath (str, optional): The path of the Graph. Defaults to None.
            subject (URIRef, optional): The subject to parse the Graph with. Defaults to None.

        Returns:
            Args(None): Create an empty Graph and Node with an unique subject guid
            Args(graph-path): parse the graph and search for a SessionNode
                - 1 or more are found: Use that node as the SessionNode
                - None are found: Create a new SessionNode with an unique id containing all the other Nodes
            Args(subject): create a new Graph and Node with the given subject
            Args(subject & graph-path): parse the graph with the given subject
                - 1 or more are matched: Use that node as the SessionNode
                - 1 or more are found but not matched: Raise an error
                - None are found: Create a new node with the given subject
        """

        self.subject = subject
        self.graph = graph
        self.graphPath = graphPath
        self.nodes = []

        if(not self.graph and self.graphPath):
            self.graph = Graph().parse(graphPath)

        if(self.graph):
            # Step 1: Find all the nodes and split the SessionNodes
            self.sessionGraph = self.graph #Store the Graph in a sessionNodeGraph to allow for a seperate NodeGraph
            subjects = self.sessionGraph.subjects(RDF.type)
            sessionNodeSubjects = []
            resourceNodeSubjects = []
            for sub in subjects:
                print(sub)
                nodeType = ut.literal_to_string(self.sessionGraph.value(subject=sub,predicate=RDF.type))
                if 'SessionNode' in nodeType:
                    sessionNodeSubjects.append(sub)
                else:
                    resourceNodeSubjects.append(sub)
            
            # Step 2: Parse all the other Nodes into the nodelist
            for resourceNode in resourceNodeSubjects:
                newNode = self.subject_to_node_type(graph = self.sessionGraph ,graphPath= self.graphPath,subject= resourceNode)
                self.nodes.append(newNode)

            # Step 3: Find the Session node in the graph (if it exists)
            # Step 3a: Create a new Graph
            if (len(sessionNodeSubjects) == 0): # There is no existing SessionNode, create a new one
                print("no sessionSubjects found")
                self.graph = None # Remove the old full graph to create a new SessionNodeGraph
                self.to_graph() #This uses None or the subject as the subject for a new empty graph
            
            # Step 3b: Parse the existing Graph
            else: # there is 1 or more sessionNodes, search for a match
                if (not self.subject): # no subject was given, pick one from the list
                    self.subject = sessionNodeSubjects[0]
                    if(len(sessionNodeSubjects) > 1): 
                        print("More than one SessionNode is present, while no subject was provided, picked:",self.subject,"out of", sessionNodeSubjects)
                else: # Check if the subject is in the list
                    if (self.subject in sessionNodeSubjects):
                        raise ValueError("The given subject is not in the Graph or is not a SessionNode")

                # Create The SessionNode and all its variables    
                print("Creating new SessionNode with subject:",self.subject)
                super().__init__(graph=self.graph, graphPath=self.graphPath, subject=self.subject)


    def set_imageNodes(self, images):
        """Sets the images of the session to a list of imagenodes

        Args:
            images (List <ImageNode>): A list of Imagenodes
        """
        #check if the list is of imagenodes
        for image in images:
            if (not isinstance(image, ImageNode)):
                return
        # set the imagenodes
        self.imageNodes = images

    def set_geometryNodes(self, geometries):
        """Sets the geometries of the session to a list of geometrynodes

        Args:
            geometries (List <GeometryNode>): A list of geometries
        """
        #check if the list is of imagenodes
        for geometry in geometries:
            if (not isinstance(geometry, GeometryNode)):
                return
        # set the imagenodes
        self.geometryNodes = geometries
    
    def get_boundingBox():
        pass

    def subject_to_node_type(self, graph: Graph, graphPath: str, subject:URIRef, **kwargs)-> Node:
    
        nodeType = ut.literal_to_string(graph.value(subject=subject,predicate=RDF.type))
        if 'BIMNode' in nodeType:
            node=BIMNode(graph=graph, graphPath=graphPath, subject=subject, **kwargs)
        elif 'MeshNode' in nodeType:
            node=MeshNode(graph=graph, graphPath=graphPath, subject=subject, **kwargs)
        elif 'GeometryNode' in nodeType:
            node=GeometryNode(graph=graph, graphPath=graphPath, subject=subject, **kwargs)
        elif 'PointCloudNode' in nodeType:
            node=PointCloudNode(graph=graph, graphPath=graphPath, subject=subject, **kwargs)
        elif 'ImageNode' in nodeType:
            node=ImageNode(graph=graph, graphPath=graphPath, subject=subject, **kwargs)
        elif 'SessionNode' in nodeType:
            node=SessionNode(graph=graph, graphPath=graphPath, subject=subject, **kwargs)  
        else:
            node=Node(graph=graph, graphPath=graphPath, subject=subject, **kwargs) 
        return node

