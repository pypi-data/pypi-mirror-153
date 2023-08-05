"""
Node - a Python Class to govern the data and metadata of remote sensing data (pcd, images, meshes, orthomozaik)
"""

#IMPORT PACKAGES
import os
import re

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF

#IMPORT MODULES
import geomapi.utils as ut

class Node:
    """The base class For all node Classes, contains r/w and parsing functionality from and to RDF files (.ttl)

    Features:
        Initialize empty node with name or graph with single subject (full graphs should be parsed by the sesssionNode)
        Base function for parsing a 
    """

    def __init__(self,  graph: Graph = None,
                        graphPath: str = None,
                        subject: URIRef = None,
                        **kwargs):
        """Creates a new node

        Args:
            graph (Graph, optional): The RDF Graph to parse. Defaults to None.
            graphPath (str, optional): The path of the Graph. Defaults to None.
            subject (URIRef, optional): The subject to parse the Graph with. Defaults to None.

        Returns:
            Args(None): Create an empty graph with an unique subject guid
            Args(graph-path): parse the graph and choose the first subject in the graph
            Args(subject): create a new graph with the given subject
            Args(subject & graph-path): parse the graph with the given subject
        """

        # Step 1: Get the graph or graphPath and parse the graph
        self.subject = subject #The subject serves as an identifier for the node in the Current graph
        self.graph=graph
        self.graphPath=graphPath
        if(graph):          # If we get a graph, parse the graph to a node
            self.get_metadata_from_graph() 
        elif (graphPath):   # if we only get a path, load the path and parse the graph
            self.get_metadata_from_graph_path()
        else:               # No graph is given, create a new one
            self.to_graph()

        # Step 2: Assign all the optional values to the new node

        self.__dict__.update(kwargs) 

    def get_metadata_from_graph(self, graph: Graph = None, subject: URIRef = None):
        """Convert a graph to a node object with a single subject, if there are more subjects, only the first is parsed.
        Use a Session if more subjects are present

        Args:
            graph (RDFlib.Graph):  Graph to parse, leave blank to use the instance graph. Defaults to None.
            subject (RDFlib.URIRef): The subject to parse the graph for, leave blank to use the instance subject. Defaults to None.
        
        """
        # Get the subjects and the graph
        self.get_subject_graph(graph, subject)
        self.get_name() # Get the name from the subject

        for predicate, object in self.graph.predicate_objects(subject=self.subject):
            attr= ut.get_attribute_from_predicate(self.graph, predicate) #ut.predicate_to_attribute(predicate)
            #GEOMETRY
            if attr == 'cartesianBounds':
                self.cartesianBounds=ut.literal_to_cartesianBounds(self.graph.value(subject=self.subject,predicate=predicate)) 
            elif attr == 'orientedBounds':
                self.orientedBounds=ut.literal_to_orientedBounds(self.graph.value(subject=self.subject,predicate=predicate)) 
            elif attr == 'cartesianTransform':
                self.cartesianTransform=ut.literal_to_cartesianTransform(self.graph.value(subject=self.subject,predicate=predicate))
            elif attr == 'geospatialTransform':
                self.geospatialTransform=ut.literal_to_geospatialTransform(self.graph.value(subject=self.subject,predicate=predicate))
            #PATHS
            elif re.search('path', attr, re.IGNORECASE):
                path=ut.literal_to_string(self.graph.value(subject=self.subject,predicate=predicate))
                if path is not None:
                    setattr(self,attr,path)    
            #INT    
            elif attr in ut.INT_ATTRIBUTES:
                setattr(self,attr,ut.literal_to_int(object)) 
            #FLOAT
            elif attr in ut.FLOAT_ATTRIBUTES:
                setattr(self,attr,ut.literal_to_float(object)) 
            #LISTS
            elif attr in ut.LIST_ATTRIBUTES:
                setattr(self,attr,ut.literal_to_list(object)) 
            #STRINGS
            else:
                setattr(self,attr,object.toPython()) # this solely covers strings
    
    def get_metadata_from_graph_path(self, graphPath: str = None, subject: URIRef = None):
        """Parses the graph by a given graphpath and Subject, if no subject is defined in the instance, the first is picked

        Args:
            path (str, optional): The path of the graph file. Defaults to None.
            subject (str, optional): The subject to parse in the Graph, of none, it picks the instance value or the first. Defaults to None.
        """
        if(graphPath): # Validate a correct graphpath
            if graphPath.endswith(tuple(ut.RDF_EXTENSIONS)):
                self.graphPath = graphPath # Get the graphPath
            else:
                raise ValueError('file must be one of the following: ', " ".join(ut.RDF_EXTENSIONS))
           
        self.graph = Graph().parse(self.graphPath) # Create a new graph 
        if(subject): # override the subject if a new one is given
            self.subject = subject
        self.get_metadata_from_graph() # parse the data
        
    def get_subject_graph(self, graph:Graph = None, subject:URIRef = None):
        """Subselects the full Graph to only contain 1 subject

        Args:
            graph (Graph, optional): The Graph. Defaults to None.
            subject (URIRef, optional): The Subject. Defaults to None.
        """
        if(graph): # A new graph is given, overwrite the existing nodeGraph
            self.graph = graph
        if(not self.graph):
            raise ValueError("No graph has been assigned to the object, please add one")

        if (subject): # A new subject is given, overwrite the existing subject
            self.subject = subject
        elif (not self.subject): # No subject is defined yet, pick the first one
            self.subject=next(self.graph.subjects())
        if(self.subject not in self.graph.subjects()): # Evaluate the subject
            raise(ValueError("The provided Subject is not in the Graph"))

        newGraph = Graph()
        newGraph += self.graph.triples((self.subject, None, None))  # Add all the triples of the subject
        newGraph._set_namespace_manager(self.graph._get_namespace_manager()) # Copy over the full namespace
        self.graph = newGraph # Set the Graph

    def get_subject(self) -> URIRef:
        """Returns and validates the current subject, if empty, a new one is created based on a unique UID

        Returns:
            URIRef: The subject
        """
        self.subject= ut.get_uriref(getattr(self,'subject',None))
        return self.subject

    def get_name(self) -> str:
        """Return the objects subject without the URI part

        Returns:
            str: The name of the object
        """
        if(not getattr(self,'name',None)):
            self.name = os.path.basename(os.path.normpath(self.get_subject())) #Get the endpoint of the path removes al the url parts
        return self.name

    def get_folder_path(self) -> str:
        """Returns the absulute folderPath of this Node

        Raises:
            ValueError: If neither graphPath or SessionPath is defined
            FileNotFoundError: If the given graphPath or sessionPath does not lead to a valid systempath

        Returns:
            str: The Full systempath to its folder
        """

        if getattr(self, 'graphPath',None) is not None: 
            folderPath= os.path.dirname(self.graphPath) #The graphpath is the filepath, we need to get a
        elif getattr(self, 'sessionPath',None) is not None:
            folderPath=self.sessionPath
        else:
            raise ValueError("There is no path defined in this instance")

        # Validate if folderpath actually exists
        if not os.path.isdir(folderPath): # if a folderpath does not end with a trailing slash, 'dirname' will return the parent directory, so an extra check is needed
            folderPath = os.path.dirname(folderPath)
            if not os.path.isdir(folderPath):
                raise FileNotFoundError("The given path is not a valid folder on this system.")    
        return folderPath

    def get_resource(self):
        """Returns the resource from the Node type. Overwrite this function for each node type
        """
        print("This is the base Node functionality, overwite for each childNode to import the relevant resource type")
        
    def get_resource_path(self, fileFormat: str = "") -> str:
        """Find the Full path of the resource from this Node

        Args:
            fileFormat (str, optional): The desired fileformat, leave empty to look for all files. Defaults to "".

        Raises:
            FileNotFoundError: If no file can be found within the sessionpath with this Node's name
            FileNotFoundError: If the combination of the relative path and the sessionpath does not result in an existing path

        Returns:
            str: The Full resource path
        """
        # We need to find the full resource path to get the Resource,
        # Vars to check: 
        # Get the resourcepath based on the available folderpath and name of the node
        if (getattr(self,"fullResourcePath", None) is None):
            if(not self.path): #Find the relative resource path first
                folderPath = self.get_folder_path()
                allSessionFilePaths=ut.get_list_of_files(folderPath) 
                for path in allSessionFilePaths:
                    if ((self.get_name() in path) and (path.endswith(fileFormat))):
                        self.path = os.path.relpath(path, folderPath)
                if(not self.path):
                    raise FileNotFoundError("No file containing this object's name and extension is found in the sessionfolder")
            
            self.fullResourcePath = os.path.join(self.get_folder_path(), self.path)
            if(not os.path.isfile(self.fullResourcePath)):
                raise FileNotFoundError("The combined path:",self.fullResourcePath,"does not exist on this system" )
       
        # return the full path
        return self.fullResourcePath

    def to_graph(self, savePath: str = None):
        """Converts the current Node variables to a graph and optionally save it

        Args:
            savePath (str, optional): The full path to wirte the graph to. Defaults to None.
        """
        self.get_subject()  
        # if graph does not exist => create graph
        if not self.graph: 
            self.graph=Graph()              
            ut.bind_ontologies(self.graph)             
            self.graph.add((self.get_subject(), RDF.type, Literal(str(type(self)))))
  
        # enumerate attributes in node and write them to triples
        attributes = ut.get_variables_in_class(self)
        attributes = ut.clean_attributes_list(attributes)        
        pathlist = ut.get_paths_in_class(self)
              
        for attribute in attributes: 
            value=getattr(self,attribute)
            if value is not None and attribute not in pathlist:
                #find appropriete RDF URI
                predicate = ut.match_uri(attribute)
                # Add triple to graph
                self.graph.add((self.subject, predicate, Literal(str(value))))
            elif value is not None and attribute in pathlist:
                predicate = ut.match_uri(attribute)
                folderPath=self.get_folder_path()
                relpath=os.path.relpath(value,folderPath)
                self.graph.add((self.subject, predicate, Literal(relpath)))

        if(savePath):
            ut.save_graph(self.graph, savePath)
        return self.graph