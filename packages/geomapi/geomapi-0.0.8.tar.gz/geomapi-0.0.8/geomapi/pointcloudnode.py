"""
PointCloudNode - a Python Class to govern the data and metadata of point cloud data (Open3D, RDF)
"""
#IMPORT PACKAGES
import xml.etree.ElementTree as ET
from xmlrpc.client import Boolean 
import open3d as o3d 
import numpy as np 
import quaternion
import os
import uuid    

# import rdflib #https://rdflib.readthedocs.io/en/stable/
# from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph, URIRef

import pye57 #conda install xerces-c  =>  pip install pye57
#from scipy.spatial.transform import Rotation as R
# from typing import Optional

#IMPORT MODULES
import geomapi.geometrynode 
import geomapi.utils as ut
import geomapi.geometryutils as gt

class PointCloudNode (geomapi.geometrynode.GeometryNode):
    # class attributes
    # def __init__(self): # initialize with a path?
    #     super().__init__() 
    #     self.pointCount = None # (int) number of vertices
    #     self.labels = None # (int[]) list of point classificaitons
    #     self.labelInfo = None # (string) relation between labels and classes, models used, training, etc.
    #     self.classification = None # (string) class of the node
        
    #     #data
    #     self.pcd = None # (o3d.geometry.PointCloud) # Open3D point cloud
    #     # self.e57Pointcloud = None # raw E57 data file => Do we really want to retain this link?
    #     # self.e57xmlNode = None # (xml.etree.ElementTree)
   
    #     self.e57Image = None # (URIRef) pointer to ImageNode (xml.etree.ElementTree) 

    #     #Questions
    #     # where do we store normals?
    #     # where do we selections + classifications? => subnodes
        # the e57 images should be defined as imagenodes and a link should be added to the graph


    def __init__(self,  graph : Graph = None, 
                        graphPath: str = None,
                        subject : URIRef = None,
                        path : str = None, 
                        e57Path : str = None, 
                        e57XmlPath: str = None, 
                        e57Index : int =None, 
                        getGeometry : bool = False,
                        pcd:o3d.geometry.PointCloud = None, 
                        **kwargs):
        """
        Creates a PointCloudNode. Overloaded function.

        Args:
            0.graph (RDFlib Graph) : Graph with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)
            
            1.graphPath (str):  Graph file path with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)

            2.path (str) : path to .pcd file (Note that this node will also contain the data)

            3.e57Path (str) + e57Index (int) : path to e57 file + index of the scan you want to import

            4.e57XmlPath (str) + e57Index (int) : path to e57 XML file + index of the scan you want to import

            5.pcd (o3d.geometry.PointCloud) : Open3D point cloud file (Note that this node will also contain the data)
                
        Returns:
            A pointcloudnode with metadata (if you also want the data, call node.get_geometry() method)
        """   
        # set the graph and optional parameters
        super().__init__(   graph= graph,
                            graphPath= graphPath,
                            subject= subject,
                            kwargs = kwargs) 
        self.path=path
        self.e57XmlPath = e57XmlPath # (string) full path to the e57 xml file
        self.e57Path = e57Path # (string) full path to e57 file
        self.e57Index = e57Index # (int) index of scan in e57 file
        self.pcd = pcd

        if pcd is not None: #data + metadata
            if type(pcd) is o3d.geometry.PointCloud and len(pcd.points) >=3:
                self.get_metadata_from_pcd()
            else:
                raise ValueError('Invalid pcd')

        elif e57XmlPath is not None and e57Index is not None:  #metadata
            if e57XmlPath.endswith('.xml') and e57Index >=0:
                self.timestamp=ut.get_timestamp(e57XmlPath)
                self.get_metadata_from_e57xml()
            else:
                raise ValueError('file must be .xml and e57Index >=0')

        elif e57Path is not None and e57Index is not None:  #metadata
            if e57Path.endswith('.e57') and e57Index >=0:
                self.timestamp=ut.get_timestamp(e57Path)
                self.get_metadata_from_e57()
            else:
                raise ValueError('file must be .e57 and e57Index >=0')

        elif path is not None:
            if path.endswith('.pcd'): #data + metadata
                self.name=ut.get_filename(path)
                self.timestamp=ut.get_timestamp(path)                
                self.get_metadata_from_pcd()
            else:
                raise ValueError('file must be .pcd')
        
        if getGeometry:
            self.get_geometry()

    def clear_geometry(self):
        """Clear all geometries in the Node.
        """
        if getattr(self,'pcd',None) is not None:
            self.pcd=None

    def get_pcd(self) -> o3d.geometry.PointCloud:
        """Returns the pointcloud data in the node. If none is present, it will search for the data on drive.

        Returns:
            o3d.geometry.PointCloud or None
        """
        if getattr(self,'pcd',None) is not None and len(self.pcd.points)>3:
            return self.pcd 
        elif self.get_geometry():
            return self.pcd
        return None  

    def get_metadata_from_pcd(self) ->bool:
        """Gets the PointCount, cartesianTransform, cartesianBounds and orientedBounds from an o3d.geometry.PointCloud

        Returns:
            bool: True if exif data is successfully parsed
        """
        self.get_geometry()
        if getattr(self,'pcd',None) is not None and len(self.pcd.points) >=4:
            self.PointCount=len(self.pcd.points)
            center=self.pcd.get_center()  
            self.cartesianTransform= np.array([[1,0,0,center[0]],
                                                [0,1,0,center[1]],
                                                [0,0,1,center[2]],
                                                [0,0,0,1]])
            try:
                self.cartesianBounds=gt.get_cartesian_bounds(self.pcd)
                self.orientedBounds = gt.get_oriented_bounds(self.pcd)
            except:
                pass
            return True
        else:
            print('No or not enough geometries found to extract the metadata. len(self.pcd.points) >=4')
            return False

    def get_geometry(self)->bool:
        """Get the o3d.geometry.pointcloud from self.path or self.name
        
        Returns:
            bool: True if geometry is successfully loaded
        """
        if getattr(self,'pcd',None) is None:
            if getattr(self,'path',None) is not None and os.path.exists(self.path) :
                pcd = o3d.io.read_point_cloud(self.path)
                if len(pcd.points) != 0:
                    self.pcd=pcd
                    return True
            if  getattr(self,'e57Index',None) is not None:                    
                if getattr(self,'e57XmlPath',None) is not None:                    
                    e57Path=self.e57XmlPath.replace('.xml','.e57')                    
                    if os.path.exists(e57Path):
                        self.e57Path=e57Path
                        pcd=gt.e57_to_pcd(self.e57Path, self.e57Index)
                        if len(pcd.points) != 0:
                            self.pcd=pcd
                        return True

                if getattr(self,'e57Path',None) is not None and os.path.exists(self.e57Path):            
                    pcd=gt.e57_to_pcd(self.e57Path, self.e57Index)
                    if len(pcd.points) != 0:
                        self.pcd=pcd
                        return True

                if getattr(self,'name',None) is not None and getattr(self,'sessionPath',None) is not None:
                    allSessionFilePaths=ut.get_list_of_files(self.path)
                    testE57Path= self.sessionPath +'\\'+ self.name + '.e57'
                    testPcdPath= self.sessionPath + '\\'+ self.name + '.pcd'
                    if testPcdPath in allSessionFilePaths:
                        pcd = o3d.io.read_point_cloud(testPcdPath)
                        if len(pcd.points) != 0:
                            self.path=testPcdPath
                            self.pcd=pcd
                            return True
                    elif testE57Path in allSessionFilePaths:
                        self.e57Path=testE57Path
                        pcd=gt.e57_to_pcd(self.e57Path, self.e57Index)
                        if len(pcd.points) != 0:
                            self.pcd=pcd
                            return True
        elif getattr(self,'pc',None) is not None:
            if len(self.pc.points)>3:
                return True            
        return False
    
    def get_metadata_from_e57(self) -> bool:
        """Gets the PointCount, guid, cartesianTransform and cartesianBounds from an e57 pointcloud

        Returns:
            bool: True if meta data is successfully parsed
        """
        e57 = pye57.E57(self.e57Path)   
        header = e57.get_header(self.e57Index)
        try:
            self.name=ut.get_filename(self.e57Path) +'_'+str(self.e57Index)
            self.pointCount=header.point_count
            self.guid=header["guid"].value()
            r=header.rotation_matrix
            t=header.translation
            self.cartesianTransform=np.array([[r[0,0],r[0,1],r[0,2],t[0]],
                                            [r[1,0],r[1,1],r[1,2],t[1]],
                                            [r[2,0],r[2,1],r[2,2],t[2]],
                                            [0,0,0,1]])
            c=header.cartesianBounds
            self.cartesianBounds=np.array([c["xMinimum"].value(),
                                            c["xMaximum"].value(), 
                                            c["yMinimum"].value(),
                                            c["yMaximum"].value(),
                                            c["zMinimum"].value(),
                                            c["zMaximum"].value()])     
            return True
        except:
            print("Parsing e57 header failed (maybe some missing metadata?)!")
            return False

    def get_metadata_from_e57xml(self) ->bool:
        """Gets the name, timestamp, e57Path, pointCount, guid, cartesianTransform and cartesianBounds from an e57 XML file generated by .e57xmldump.exe
        from an e57 pointcloud. Note that the XML file should not contain the first rule <?xml version="1.0" encoding="UTF-8"?> 
        as this breaks the code

        Returns:
            bool: True if meta data is successfully parsed
        """
        self.name=ut.get_filename(self.e57XmlPath) +'_'+str(self.e57Index)
        self.timestamp=ut.get_timestamp(self.e57XmlPath)
        self.e57Path=self.e57XmlPath.replace('.xml','.e57')
        try:
            mytree = ET.parse(self.e57XmlPath)
            root = mytree.getroot()         
            for idx,e57xml in enumerate(root.iter('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}vectorChild')):
                if idx == self.e57Index:
                    self.guid=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}guid').text
                    cartesianBoundsnode=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}cartesianBounds') 
                    if cartesianBoundsnode is not None:
                        try:
                            cartesianBounds=np.array([ut.xml_to_float(cartesianBoundsnode[0].text),
                                                    ut.xml_to_float(cartesianBoundsnode[1].text),
                                                    ut.xml_to_float(cartesianBoundsnode[2].text),
                                                    ut.xml_to_float(cartesianBoundsnode[3].text),
                                                    ut.xml_to_float(cartesianBoundsnode[4].text),
                                                    ut.xml_to_float(cartesianBoundsnode[5].text)])
                            cartesianBounds=cartesianBounds.astype(np.float)
                            cartesianBounds=np.nan_to_num(cartesianBounds)
                        except:
                            cartesianBounds=np.array([0.0,0.0,0.0,0.0,0.0,0.0])
                    self.cartesianBounds=cartesianBounds

                    #POSE
                    posenode=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}pose')
                    if posenode is not None:
                        rotationnode=posenode.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}rotation')
                        if rotationnode is not None:               
                            try:
                                quatArray=np.array([ ut.xml_to_float(rotationnode[3].text),
                                                ut.xml_to_float(rotationnode[0].text),
                                                ut.xml_to_float(rotationnode[1].text),
                                                ut.xml_to_float(rotationnode[2].text) ])
                                quatArray=quatArray.astype(np.float)   
                                quatArray=np.nan_to_num(quaternion)                
                            except:
                                quatArray=np.array([0,0,0,1])

                            rotationMatrix = np.quaternion.as_rotation_matrix(np.quaternion.from_float_array(quatArray))

                        translationnode=posenode.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}translation')
                        if translationnode is not None: 
                            try:
                                translationVector= np.array([ut.xml_to_float(translationnode[0].text),
                                                            ut.xml_to_float(translationnode[1].text),
                                                            ut.xml_to_float(translationnode[2].text)])
                                translationVector=translationVector.astype(np.float)
                                translationVector=np.nan_to_num(translationVector)       
                            except:
                                translationVector=np.array([0.0,0.0,0.0])
                        self.cartesianTransform=gt.rotation_and_translation_to_transformation_matrix(rotationMatrix,translationVector)
                    # SET POSE FROM cartesianBounds
                    elif self.cartesianBounds is not None:            
                        self.cartesianTransform=gt.cartesian_bounds_to_cartesian_transform(self.cartesianBounds)

                    pointsnode=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}points')
                    if not pointsnode is None:
                        self.pointCount=int(pointsnode.attrib['recordCount'])
            return True
        except:
            print("Parsing e57 header failed (maybe some missing metadata?)!")
            return False

    def set_pcd(self, pcd): 
        self.pcd = pcd

    def set_pcd_path_from_e57(self,path:str=None):
        """Set the path to the .pcd file manually or from the name or guid combined with the e57Path, e57XmlPath, graphPath or working directory. 

        Args:
            path (str, optional): Path to the .pcd file. Defaults to None.
        """
        if getattr(self, 'path',None) is None:        
            if getattr(self, 'e57Path',None) is not None:
                    folder=ut.get_folder(self.e57Path)
            elif getattr(self, 'e57XmlPath',None) is not None:
                folder=ut.get_folder(self.e57XmlPath)
            elif getattr(self, 'graphPath',None) is not None:
                folder=ut.get_folder(self.graphPath)
            else:
                folder=ut.get_folder(os.getcwd())

            if getattr(self,'name',None) is not None:            
                self.path=folder+'\\'+self.name+'.pcd'
            elif getattr(self,'guid',None) is not None:         
                self.path=folder+'\\'+self.guid+'.pcd'
            else:
                self.path=folder+'\\'+str(uuid.uuid1()) +'.pcd'
        else:
            self.path=path
