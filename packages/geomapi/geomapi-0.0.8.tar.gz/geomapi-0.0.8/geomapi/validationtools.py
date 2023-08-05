"""
validationtools - a Python library for validating objects.
"""
#IMPORT PACKAGES
from lib2to3.pytree import Node
import numpy as np 
import cv2 
import open3d as o3d 
import json  
import os 
import re
import matplotlib.pyplot as plt #conda install -c conda-forge matplotlib
#import torch #conda install -c pytorch pytorch
# import pye57 #conda install xerces-c  =>  pip install pye57
import xml.etree.ElementTree as ET 
# from pathlib import Path
import math
import xlsxwriter
import csv

# import ifcopenshell.util
# import ifcopenshell.geom as geom
# from ifcopenshell.util.selector import Selector
# from ifcopenshell.ifcopenshell_wrapper import file

# import APIs
import rdflib
from rdflib import Graph, plugin
from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD


#IMPORT MODULES watch out for circular imports
import geomapi
# from geomapi.node import Node
# from geomapi.geometrynode import GeometryNode
from geomapi.bimnode import BIMNode
# from geomapi.meshnode import MeshNode
from geomapi.pointcloudnode import PointCloudNode
# from geomapi.imagenode import ImageNode
import geomapi.linkeddatatools as ld


def create_meshpcd(element : BIMNode, Resolution = 10000, sampleSize = None, path = None) -> PointCloudNode:
    
    if element.mesh or os.path.exists(element.meshPath):
        mesh_points = round(element.mesh.get_surface_area()*Resolution)
        if mesh_points > 0:
            pcdNode = PointCloudNode()
            pcdNode.name = element.name + "-MESHPCD"
            pcdNode.pcd = element.mesh.sample_points_uniformly(number_of_points = mesh_points, use_triangle_normal=True) #Sample the amount of points on the mesh and preserve the corresponding normals of the msh object
            if sampleSize:
                pcdNode.pcd = pcdNode.pcd.voxel_down_sample(sampleSize)
                pcdNode.voxelSize = sampleSize
            pcdNode.set_from_pcd()
            if path:
                pcdNode.path = path
                o3d.io.write_point_cloud(pcdNode.path, pcdNode.pcd)
            pcdNode.sensor = "Sampled " + str(element.name) + " mesh"

            return pcdNode
        else:
            print('Error, no point cloud was sampled from the mesh')
            return None
    else:
        print('No geometry found to extract the sampled point cloud. Set the geometry first.')
        return None
    
def create_croppedpcd(element : BIMNode, target : PointCloudNode, sampleSize = None, path = None) -> PointCloudNode:
    bimOrientedBoundingBox = ld.oriented_bounds_to_open3d_oriented_bounding_box(element.orientedBounds)
    expandedBimOrientedBoundingBox = ld.expand_box(bimOrientedBoundingBox,  u=0.3, v=0.3, z=0)
    if target.pcd or os.path.exists(target.path):
        pcdNode = PointCloudNode()
        pcdNode.name = element.name + "-CROPPEDPCD"
        pcdNode.pcd = target.pcd.crop(expandedBimOrientedBoundingBox)
        if sampleSize:
            pcdNode.pcd = pcdNode.pcd.voxel_down_sample(sampleSize)
            pcdNode.voxelSize = sampleSize
        pcdNode.set_from_pcd()
        if path:
            pcdNode.path = path
            o3d.io.write_point_cloud(pcdNode.path, pcdNode.pcd)
        pcdNode.sensor = "Cropped from" + str(pcdNode.sensor)
        return pcdNode
        
    else:
        print('No geometry found to crop the element from. Set the geometry first.')
        return None

def filter_pointcloud(target : geomapi.pointcloudnode.PointCloudNode, reference : geomapi.pointcloudnode.PointCloudNode, normals = True, path = None,):

    if not normals:
        filtered = distance_filtering(target, reference, path=path)
    elif normals:
        filtered = normal_filtering(target, reference, path = path)
    
    if filtered:
        return filtered
    else: 
        print("ERROR: Filtering Failed")

def distance_filtering(target : geomapi.pointcloudnode.PointCloudNode, reference: geomapi.pointcloudnode.PointCloudNode, distanceTreshold = 0.1, path = None):

    distances = target.pcd.compute_point_cloud_distance(reference.pcd)
    distanceInlierIndeces = []
    i = 0
    while i < len(distances):
        if distances [i] <= distanceTreshold:
            distanceInlierIndeces.append(i)
        i = i + 1
    if len(distanceInlierIndeces) > 0:
        distanceFilteredPcdNode = geomapi.pointcloudnode.PointCloudNode()
        distanceFilteredPcdNode.pcd = o3d.geometry.PointCloud()
        distanceFilteredPcdNode.pcd = target.pcd.select_by_index(distanceInlierIndeces)
        distanceFilteredPcdNode.set_from_pcd()
        distanceFilteredPcdNode.sensor = "Filtered on distance"
        distanceFilteredPcdNode.name = reference.name.split("-")[0] + "-disFILTERED"
        if path:
            distanceFilteredPcdNode.path = path
            o3d.io.write_point_cloud(distanceFilteredPcdNode.path, distanceFilteredPcdNode.pcd)

        return distanceFilteredPcdNode
    else:
        print("ERROR: No points within treshold distance")
        return None
 

def normal_filtering(target : geomapi.pointcloudnode.PointCloudNode, reference: geomapi.pointcloudnode.PointCloudNode, distanceTreshold = 0.1, path = None, searchRadius=0.1, dotTreshold = 0.7):
   

    if not target.pcd.has_normals():
        target.pcd.estimate_normals()
    if not reference.pcd.has_normals():
        reference.pcd.estimate_normals()
                
    distances = target.pcd.compute_point_cloud_distance(reference.pcd)

    distanceInlierIndeces = []
    i = 0
    while i < len(distances):
        if distances [i] <= distanceTreshold:
            distanceInlierIndeces.append(i)
        i = i + 1
    if len(distanceInlierIndeces) > 0:
        normalInlierIndeces = []
        kdtree = o3d.geometry.KDTreeFlann(reference.pcd)
        for index in distanceInlierIndeces:
            [k, idx, d] = kdtree.search_radius_vector_3d(target.pcd.points[index], searchRadius)
            matched = False
            i = 0 
            while not matched and i < len(idx) and len(idx) > 0:
                if np.abs(np.dot(np.asarray(target.pcd.normals[index]), np.asarray(reference.pcd.normals[idx[i]]))) > dotTreshold:
                    matched = True
                    normalInlierIndeces.append(index)
                i = i + 1
        if len(normalInlierIndeces) > 0:
            normalFilteredPcdNode = geomapi.pointcloudnode.PointCloudNode()
            normalFilteredPcdNode.pcd = o3d.geometry.PointCloud()
            normalFilteredPcdNode.pcd = target.pcd.select_by_index(normalInlierIndeces)
            normalFilteredPcdNode.set_from_pcd()
            normalFilteredPcdNode.sensor = "Filtered on normal"
            normalFilteredPcdNode.name = reference.name.split("-")[0] + "-norFILTERED"

            if path:
                normalFilteredPcdNode.path = path
                o3d.io.write_point_cloud(normalFilteredPcdNode.path, normalFilteredPcdNode.pcd)
            
            return normalFilteredPcdNode
    else:
        print("ERROR: No points within treshold distance")
        return None


def compute_LOA(target : geomapi.pointcloudnode.PointCloudNode, reference: geomapi.pointcloudnode.PointCloudNode, t30 = 0.015, t20 = 0.05, t10 = 0.1, t00 =5, abs = True):
        
        distances = target.pcd.compute_point_cloud_distance(reference.pcd)
        LOA10Inliers = 0
        LOA20Inliers = 0
        LOA30Inliers = 0
        usedPointCount = 0
        pointCount = len(distances)
        
        for distance in np.asarray(distances):
            if distance < t00:
                usedPointCount += 1 
            if distance < t10:
                LOA10Inliers += 1
            if distance < t20:
                LOA20Inliers += 1
            if distance < t30:
                LOA30Inliers += 1
        if not abs:
            pointCount = usedPointCount

        if pointCount > 0:
            LOA00 = usedPointCount/pointCount
            LOA10 = LOA10Inliers/pointCount
            LOA20 = LOA20Inliers/pointCount
            LOA30 = LOA30Inliers/pointCount
        
        
            return [LOA00, LOA10, LOA20, LOA30]

def report_LOAs(element : geomapi.bimnode.BIMNode, path, mesh = True,csvWriter = None,xlsxWorksheet = None,xlsxRow=None, p10 = 0.95, p20 = 0.95, p30 = 0.95):
    if float(element.LOAs[3]) > p30:
        element.accuracy = "LOA30"
    elif float(element.LOAs[2]) > p20:
        element.accuracy = "LOA20"
    elif float(element.LOAs[1]) > p10:
        element.accuracy = "LOA10"
    elif float(element.LOAs[1]) > 0:
        element.accuracy = "LOA00"
    else:
        element.accuracy = "NO LOA"

    if not os.path.exists(path):
        os.makedirs(path)
    if csvWriter:
        LOA_to_csv(element, csvWriter)
    if xlsxWorksheet:
        LOA_to_xlsx(element,xlsxWorksheet, xlsxRow)
    if mesh:
        LOA_to_mesh(element, path)

def LOA_to_mesh(element : geomapi.bimnode.BIMNode, path):
    
    meshResultDirectory = os.path.join(path, "PLY")
    if not os.path.isdir(meshResultDirectory): #check if the folder exists
        os.mkdir(meshResultDirectory)
    
    meshResultName = element.name
    meshResultFileName = meshResultName + ".ply"
    meshResultPath = os.path.join(meshResultDirectory, meshResultFileName)

    if not element.LOAs == None:
        if element.mesh or os.path.exists(element.meshPath):
            loaded = False
            if not element.mesh and element.meshPath:
                #Load the meshobject from disk
                element.mesh = o3d.io.read_triangle_mesh(element.meshPath)
                loaded = True
        result = element.mesh
        if element.accuracy == "LOA30":
            result.paint_uniform_color([0,0,1])
        elif element.accuracy == "LOA20":
            result.paint_uniform_color([0,1,0])
        elif element.accuracy == "LOA10":
            result.paint_uniform_color([1,1,0])
        elif element.accuracy == "LOA00":
            result.paint_uniform_color([1,0,0])
        else:
            result.paint_uniform_color([1,1,1])
        
        if loaded:
            element.mesh = None
        
        o3d.io.write_triangle_mesh(meshResultPath,result)
        print("OBJ file saved in %s" %meshResultPath)

    else: 
        print("ERROR no LOAs where computed in previous steps") 
    
def LOA_to_csv(element : geomapi.bimnode.BIMNode, csvWriter):

    data = [element.name, element.globalId, element.label, element.accuracy, element.LOAs[1], element.LOAs[2], element.LOAs[3]]
    csvWriter.writerow(data)

def LOA_to_xlsx(element : geomapi.bimnode.BIMNode, xlsxWorksheet = None, xlsxRow=None):

    xlsxWorksheet.write(xlsxRow, 0, element.name)
    xlsxWorksheet.write(xlsxRow, 1, element.globalId)
    xlsxWorksheet.write(xlsxRow, 2, element.label)
    xlsxWorksheet.write(xlsxRow, 3, element.accuracy)
    xlsxWorksheet.write(xlsxRow, 4, element.LOAs[1])
    xlsxWorksheet.write(xlsxRow, 5, element.LOAs[2])
    xlsxWorksheet.write(xlsxRow, 6, element.LOAs[3])
    
