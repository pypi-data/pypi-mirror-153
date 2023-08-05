"""
General Basic functions to support Other modules
"""

import os
import rdflib
from rdflib import Graph,URIRef,Literal
import re
import numpy as np
import ntpath
from datetime import datetime
import PIL.Image
from PIL.ExifTags import GPSTAGS, TAGS
import uuid
from typing import List
from warnings import warn


#### GLOBAL VARIABLES ####

RDF_EXTENSIONS = [".ttl"]
IMG_EXTENSION = [".jpg", ".png", ".JPG", ".PNG", ".JPEG"]
MESH_EXTENSION = [".obj",".fbx" ]
PCD_EXTENSION = [".pcd", ".pts", ".ply"]
INT_ATTRIBUTES = ['recordCount','faceCount','e57Index'] #'label'
FLOAT_ATTRIBUTES = ['xResolution','yResolution','imageWidth','imageHeight','focalLength35mm','principalPointU','principalPointV','accuracy']
LIST_ATTRIBUTES =  ['hasBIM','hasCAD','hasPcd','hasMesh','hasImg','hasOrtho','hasChild','hasParent','distortionCoeficients']


#### BASIC OPERATIONS ####

def replace_str_index(text,index=0,replacement='_'):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def get_variables_in_class(cls) -> list: 
    """
    returns list of variables in the class
    """  
    return [i for i in cls.__dict__.keys() if i[:1] != '_'] 

def get_list_of_files(directoryPath:str) -> list:
    """Get a list of all files in the directory and subdirectories (getListOfFiles)

    Args:
        directoryPath: directory path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\"
            
    Returns:
        A list of files 
    """
    # names in the given directory 
    listOfFile = os.listdir(directoryPath)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(directoryPath, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)                
    return allFiles

def get_paths_in_class(cls) -> list: 
    """
    returns list of paths in the class
    """  
    from re import search
    return [i for i in cls.__dict__.keys() if search('Path',i) or search('path',i)] 

def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def get_exif_data(img:PIL.Image):
    """Returns a dictionary from the exif data of an Image item. Also
    converts the GPS Tags
    
    Returns:
        bool: True if exif data is sucesfully parsed
    """
    exifData = {}
    info = img._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exifData[decoded] = gps_data
            else:
                exifData[decoded] = value        
        return exifData      
    else:
        return None        

def get_filename(path :str) -> str:
    """ Deconstruct path into filename"""
    path=ntpath.basename(path)
    head, tail = ntpath.split(path)
    array=tail.split('.')
    return array[0]

def get_folder(path :str) -> str:
    """ Deconstruct path and return forlder"""
    return os.path.dirname(os.path.realpath(path))

def get_timestamp(path : str) -> str:
    ctime=os.path.getctime(path)
    dtime=datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
    return dtime


#### CONVERSIONS ####

def literal_to_cartesianTransform(literal:Literal) -> np.array:
    cartesianTransform=str(literal)
    if 'None' not in cartesianTransform:
        transform=np.empty([0,0], dtype=float)
        stringList = re.findall(r"\[(.+?)\]", cartesianTransform)
        for list in stringList:
            temp=list.strip('[]')
            res=np.fromstring(temp, dtype=float, sep=' ')
            transform=np.append(transform,res)
        transform = transform.reshape((4,4))
        return transform
    else:
        return None  

def literal_to_geospatialTransform(literal: Literal) -> np.array:
    temp=str(literal)
    if 'None' not in temp:
        temp=temp.strip('[]') 
        temp=re.sub(' +', ' ',temp)      #test 
        temp=temp.split(' ')
        temp=[x for x in temp if x]
        res = list(map(float, temp))        
        return np.array([res[0],res[1],res[2]])
    else:
        return None  

def literal_to_cartesianBounds(literal: Literal)-> np.array:
    """
    Convert URIRef to cartesian bounds

    Args:
        literal (URIRef):  
    Returns:
        np.array ([xMin,xMax,yMin,yMax,zMin,zMax]) or None  
    """   
    temp=str(literal)
    if 'None' not in temp:
        temp=str(literal)
        temp=temp.replace("\n","")
        temp=temp.replace(",","")
        temp=temp.strip('[]')        
        temp=re.sub(' +', ' ',temp)     #test
        temp=temp.split(' ')
        temp=[x for x in temp if x]
        res = list(map(float, temp))           
        return np.array([res[0],res[1],res[2],res[3],res[4],res[5]])
    else:
        return None  

def literal_to_orientedBounds(literal: Literal)-> np.array:
    """
    Convert URIRef to cartesian bounds

    Args:
        literal (URIRef):  
    Returns:
        np.array ([xMin,xMax,yMin,yMax,zMin,zMax]) or None  
    """   
    string=str(literal)
    if 'None' not in string:
        array=np.empty([0,0], dtype=float)
        stringList = re.findall(r"\[(.+?)\]", string)
        for list in stringList:
            temp=list.strip('[]')
            res=np.fromstring(temp, dtype=float, sep=' ')
            array=np.append(array,res)
        array = array.reshape((8,3))
        return array
    else:
        return None 

def literal_to_float(literal: Literal) -> float:
    string=str(literal)
    if 'None' in string:
        return None
    else:
        return float(string)

def literal_to_string(literal: Literal)->str:
    string=str(literal)
    if 'None' in string:
        return None
    else:
        return string

def literal_to_list(literal: Literal)->list:
    string=str(literal)
    if 'None' in string:
        return None
    else: 
        return string_to_list(string)

def literal_to_int(literal: Literal) -> int:
    string=str(literal)
    if 'None' in string:
        return None
    else:
        return int(string)

def literal_to_uriref(literal: Literal)->URIRef:
    string=str(literal)
    if 'None' in string:
        return None
    else:
        for idx,element in enumerate(string):
            if element in "[' ]":
                string=replace_str_index(string,index=idx,replacement='$')
        res=[]
        itemList=list(string.split(","))
        for item in itemList:      
            item=item.strip("$")
            res.append(URIRef(item))
    return res

def predicate_to_attribute(predicate:Literal) -> str:
    warn("This function is depricated use get_attribute_from_predicate() instead, this will filter out the namespaces instead of splitting by #")
    p=str(predicate)
    list=p.split('#')
    return list[-1]

def string_to_list(string:str)->list:
    """
    Convert string of items to a list of their respective types
    """
    string=string.strip("[!@#$%^&*()-+?_ =,<>]'")
    string=re.sub(' +', ' ',string)
    res=[]
    itemList=list(string.split(" "))
    for item in itemList:
        if is_float(item): 
            res.append(float(item))
        elif is_int(item): 
            res.append(int(item))
        elif is_string(item): #isn't this always the case
            res.append(str(item))
        elif is_uriref(item): 
            res.append(URIRef(item))
    return res

def string_to_rotation_matrix(matrixString :str) -> np.array:
    list=matrixString.split(' ')
    rotationMatrix=np.array([[float(list[0]),float(list[1]),float(list[2]),0],
                             [float(list[3]),float(list[4]),float(list[5]),0],
                             [float(list[6]),float(list[7]),float(list[8]),0],
                             [0,0,0,1]])
    return rotationMatrix

def string_to_array(string : str)-> np.array:
    list=string.split(' ')
    floatlist=[]
    for x in list:
        floatlist.append(float(x))
    return np.array(floatlist)

def xml_to_float(xml) -> float:
    if xml is None:
        return None
    else:
        return float(xml)

def xcr_to_lat(xcr:str) -> float:
    if xcr is not None:
        list=list=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?', xcr)
        if 'N' in list[-1]:
            return float(list[0])
        elif 'Z' in list[-1]:
            return - float(list[0])
    else:
        return None

def xcr_to_long(xcr:str) -> float:
    if xcr is not None:
        list=list=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?', xcr)
        if 'E' in list[-1]:
            return float(list[0])
        elif 'W' in list[-1]:
            return - float(list[0])
    else:
        return None

def xcr_to_alt(xcr:str) -> float:
    if xcr is not None:
        list=list=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?', xcr)
        return float(list[0])/float(list[-1])       
    else:
        return None

def cartesianTransform_to_literal(matrix : np.array) -> str:
    """ convert nparray [4x4] to str([16x1])"""
    if matrix.size == 16: 
        return str(matrix.reshape(16,1))
    else:
        Exception("wrong array size!")    

def featured3d_to_literal(value) -> str:
    "No feature implementation yet"

def featured2d_to_literal(value) -> str:
    "No feature implementation yet"

def item_to_list(item):
    if type(item) is np.ndarray:
        item=item.flatten()
        return item.tolist()
    elif type(item) is np.array:
        item=item.flatten()
        return item.tolist()
    elif type(item) is list:
        return item
    else:
        return [item]


#### VALIDATION ####

def check_string_validity(path:str, replacement ='_') -> str:
    """Checks path validity. If not valid, The function adjusts path naming to be Windows compatible

    Args:
        path (str): _description_

    Returns:
        str: _description_
    """
    if os.path.isdir(path):
        return path
    else:
        for idx,element in enumerate(path):
            if element in "^[^<>/{}[\] ~`]:|*$":
                path=replace_str_index(path,index=idx,replacement=replacement)
        return path

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def is_int(element) -> bool:
    try:
        int(element)
        return True
    except ValueError:
        return False

def is_string(element) -> bool:
    special_characters = "[!@#$%^&*()-+?_= ,<>/]'"
    if not any(c in special_characters for c in element):
        str(element)
        return True
    else:
        return False

def is_uriref(element) -> bool:
    try:
        URIRef(element)
        return True
    except ValueError:
        return False


#### RDF ####

def save_graph(graph, savePath) -> None:
    with open(savePath, 'w') as f:
        f.write(graph.serialize())

def get_attribute_from_predicate(graph: Graph, predicate : Literal) -> str:
    """Returns the attribute witout the namespace

    Args:
        graph (Graph): The Graph containing the namespaces
        predicate (Literal): The Literal to convert

    Returns:
        str: The attribute name
    """
    predStr = str(predicate)
    #Get all the namespaces in the graph
    for nameSpace in graph.namespaces():
        nameSpaceStr = str(nameSpace[1])
        if(predStr.__contains__(nameSpaceStr)):
            predStr = predStr.replace(nameSpaceStr, '')
            break
    return predStr

def bind_ontologies(graph : Graph) -> Graph:
    """
    Bind additional ontologies that aren't in rdflib
    """
    exif = rdflib.Namespace('http://www.w3.org/2003/12/exif/ns#')
    graph.bind('exif', exif)
    geo=rdflib.Namespace('http://www.opengis.net/ont/geosparql#') #coordinate system information
    graph.bind('geo', geo)
    gom=rdflib.Namespace('https://w3id.org/gom#') # geometry representations => this is from mathias
    graph.bind('gom', gom)
    omg=rdflib.Namespace('https://w3id.org/omg#') # geometry relations
    graph.bind('omg', omg)
    fog=rdflib.Namespace('https://w3id.org/fog#')
    graph.bind('fog', fog)
    v4d=rdflib.Namespace('https://w3id.org/v4d/core#')
    graph.bind('v4d', v4d)
    v4d3D=rdflib.Namespace('https://w3id.org/v4d/3D#')
    graph.bind('v4d3D', v4d3D)
    openlabel=rdflib.Namespace('https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f#')
    graph.bind('openlabel', openlabel)
    e57=rdflib.Namespace('http://libe57.org#')
    graph.bind('e57', e57)
    xcr=rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    graph.bind('xcr', xcr)
    ifc=rdflib.Namespace('http://ifcowl.openbimstandards.org/IFC2X3_Final#')
    graph.bind('ifc', ifc)
    return graph

def clean_attributes_list(list:list) -> list:
    #NODE
    excludedList=['graph','graphPath','subject','name','sessionPath','fullResourcePath']
    #BIMNODE    
    excludedList.extend(['ifcElement'])
    #MESHNODE
    excludedList.extend(['mesh'])
    #IMGNODE
    excludedList.extend(['exifData','img','features2d','pinholeCamera'])
    #PCDNODE
    excludedList.extend(['pcd','e57Pointcloud','e57xmlNode','e57image','features3d'])
    cleanedList = [ elem for elem in list if elem not in excludedList]
    return cleanedList

def match_uri(attribute :str):
    """
    Match attribute name with Linked Data URI's. Non-matches are serialized as v4d."attribute"
    """
    #NODE
    
    exif = rdflib.Namespace('http://www.w3.org/2003/12/exif/ns#')
    geo=rdflib.Namespace('http://www.opengis.net/ont/geosparql#') #coordinate system information
    gom=rdflib.Namespace('https://w3id.org/gom#') # geometry representations => this is from mathias
    omg=rdflib.Namespace('https://w3id.org/omg#') # geometry relations
    fog=rdflib.Namespace('https://w3id.org/fog#')
    v4d=rdflib.Namespace('https://w3id.org/v4d/core#')
    v4d3D=rdflib.Namespace('https://w3id.org/v4d/3D#')
    openlabel=rdflib.Namespace('https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f#')
    e57=rdflib.Namespace('http://libe57.org#')
    xcr=rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    ifc=rdflib.Namespace('http://ifcowl.openbimstandards.org/IFC2X3_Final#')

    #OPENLABEL
    if attribute in ['timestamp','sensor']:
        return openlabel[attribute]
    #E57
    elif attribute in ['cartesianBounds','cartesianTransform','geospatialTransform','pointCount','e57XmlPath','e57Path','e57Index','e57Image']:
        return  e57[attribute]
    #GOM
    elif attribute in ['coordinateSystem','']:
        return  gom[attribute]
    #IFC
    elif attribute in ['ifcPath','className','globalId','phase','ifcName']:
        return  ifc[attribute]
    #EXIF
    elif attribute in ['xResolution','yResolution','resolutionUnit','imageWidth','imageHeight']:
        return  exif[attribute]
    #XCR
    elif attribute in ['focalLength35mm','principalPointU','principalPointV','distortionCoeficients','gsd']:
        return  xcr[attribute]
    #V4D
    else:
        return v4d[attribute]

def get_uriref(value) -> URIRef:
    if (not value):
         return URIRef('http://' + check_string_validity(str(uuid.uuid1())))
    if not is_uriref(value):            
        return URIRef('http://' + check_string_validity(str(value)))
    return value

