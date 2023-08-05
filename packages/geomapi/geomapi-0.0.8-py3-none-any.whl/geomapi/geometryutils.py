"""
Geometryutils - a Python library for processing mesh and point cloud data.
"""

from xmlrpc.client import Boolean
import numpy as np 
import open3d as o3d 
import copy
import pye57 
import xml.etree.ElementTree as ET 
import math
from typing import List
import matplotlib

import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util
from scipy.spatial.transform import Rotation as R

#IMPORT MODULES watch out for circular imports
import geomapi
import geomapi.utils as ut


#### COORDINATE CONVERTERS ####

def belgian_datum_to_wgs84(latBel:float,lngBel:float) -> tuple:
    """
    Input parameters : Lat, Lng : latitude / longitude in decimal degrees and in Belgian 1972 datum
    Output parameters : LatWGS84, LngWGS84 : latitude / longitude in decimal degrees and in WGS84 datum
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    Haut = 0.0   
        
    #conversion to radians
    Lat = (math.PI / 180) * latBel
    Lng = (math.PI / 180) * lngBel
    
    SinLat = math.Sin(Lat)
    SinLng = math.Sin(Lng)
    CoSinLat = math.Cos(Lat)
    CoSinLng = math.Cos(Lng)
    
    dx = -125.8
    dy = 79.9
    dz = -100.5
    da = -251.0
    df = -0.000014192702
    
    LWf = 1 / 297
    LWa = 6378388
    LWb = (1 - LWf) * LWa
    LWe2 = (2 * LWf) - (LWf * LWf)
    Adb = 1 / (1 - LWf)
    
    Rn = LWa / math.Sqrt(1 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1 - LWe2) / (1 - LWe2 * Lat * Lat) ^ 1.5
    
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
    
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
    
    LatWGS84 = ((Lat + DLat) * 180) / math.PI
    LngWGS84 = ((Lng + DLng) * 180) / math.PI
    return LatWGS84,LngWGS84

def wgs84_to_belgian_datum(LatWGS84: float,LngWGS84:float) -> tuple:
    """
    Input parameters : Lat, Lng : latitude / longitude in decimal degrees and in WGS84 datum
    Output parameters : LatBel, LngBel : latitude / longitude in decimal degrees and in Belgian datum
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    Haut = 0    
    
    #conversion to radians
    Lat = (math.PI / 180) * LatWGS84
    Lng = (math.PI / 180) * LngWGS84
    
    SinLat = math.Sin(Lat)
    SinLng = math.Sin(Lng)
    CoSinLat = math.Cos(Lat)
    CoSinLng = math.Cos(Lng)
    
    dx = 125.8
    dy = -79.9
    dz = 100.5
    da = 251.0
    df = 0.000014192702
    
    LWf = 1 / 297
    LWa = 6378388
    LWb = (1 - LWf) * LWa
    LWe2 = (2 * LWf) - (LWf * LWf)
    Adb = 1 / (1 - LWf)
    
    Rn = LWa / math.Sqrt(1 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1 - LWe2) / (1 - LWe2 * Lat * Lat) ^ 1.5
    
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
    
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
    
    LatBel = ((Lat + DLat) * 180) / math.PI
    LngBel = ((Lng + DLng) * 180) / math.PI
    return  LatBel,LngBel

def spherical_coordinates_to_lambert72(latBel :float,lngBel:float) -> tuple:
    """
    Conversion from spherical coordinates to Lambert 72
    Input parameters : lat, lng (spherical coordinates)
    Spherical coordinates are in decimal degrees converted to Belgium datum!
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
 
    LongRef  = 0.076042943  #      '=4°21'24"983
    bLamb  = 6378388 * (1 - (1 / 297))
    aCarre  = 6378388 ^ 2
    eCarre = (aCarre - bLamb ^ 2) / aCarre
    KLamb = 11565915.812935
    nLamb = 0.7716421928
    
    eLamb  = math.Sqrt(eCarre)
    eSur2  = eLamb / 2
    
    #conversion to radians
    lat = (math.PI / 180) * latBel
    lng = (math.PI / 180) * lngBel
    
    eSinLatitude = eLamb * math.Sin(lat)
    TanZDemi = (math.Tan((math.PI / 4) - (lat / 2))) *  (((1 + (eSinLatitude)) / (1 - (eSinLatitude))) ^ (eSur2))
    
    RLamb= KLamb * ((TanZDemi) ^ nLamb)
    
    Teta  = nLamb * (lng - LongRef)
        
    x = 150000 + 0.01256 + RLamb * math.Sin(Teta - 0.000142043)
    y = 5400000 + 88.4378 - RLamb * math.Cos(Teta - 0.000142043)
    return x,y

def lambert72_to_spherical_coordinates(x :float ,y:float) -> tuple: 
    """"
    Belgian Lambert 1972---> Spherical coordinates
    Input parameters : X, Y = Belgian coordinates in meters
    Output : latitude and longitude in Belgium Datum!
    source: http://zoologie.umons.ac.be/tc/algorithms.aspx
    """
    LongRef = 0.076042943  #      '=4°21'24"983
    nLamb  = 0.7716421928 #
    aCarre = 6378388 ^ 2 #
    bLamb = 6378388 * (1 - (1 / 297)) #
    eCarre = (aCarre - bLamb ^ 2) / aCarre #
    KLamb = 11565915.812935 #
    
    eLamb = math.Sqrt(eCarre)
    eSur2 = eLamb / 2
    
    Tan1  = (x - 150000.01256) / (5400088.4378 - y)
    Lambda = LongRef + (1 / nLamb) * (0.000142043 + math.Atan(Tan1))
    RLamb = math.Sqrt((x - 150000.01256) ^ 2 + (5400088.4378 - y) ^ 2)
    
    TanZDemi = (RLamb / KLamb) ^ (1 / nLamb)
    Lati1 = 2 * math.Atan(TanZDemi)
    
    eSin=0.0
    Mult1=0.0
    Mult2=0.0
    Mult=0.0
    LatiN=0.0
    Diff=1     

    while math.Abs(Diff) > 0.0000000277777:
        eSin = eLamb * math.Sin(Lati1)
        Mult1 = 1 - eSin
        Mult2 = 1 + eSin
        Mult = (Mult1 / Mult2) ^ (eLamb / 2)
        LatiN = (math.PI / 2) - (2 * (math.Atan(TanZDemi * Mult)))
        Diff = LatiN - Lati1
        Lati1 = LatiN
    
    latBel = (LatiN * 180) / math.PI
    lngBel = (Lambda * 180) / math.PI
    return latBel,lngBel


#### FORMAT CONVERTERS ####

def cartesian_bounds_to_cartesian_transform(cartesianBounds:np.array) ->np.array:
    if len(cartesianBounds) !=6:
        return None
    else:
        matrix=np.zeros([4,4])
        np.fill_diagonal(matrix,1)
        matrix[3]=(cartesianBounds[1]-cartesianBounds[0])/2
        matrix[7]=(cartesianBounds[3]-cartesianBounds[2])/2
        matrix[11]=(cartesianBounds[5]-cartesianBounds[4])/2
        return matrix

def e57_to_pcd(e57Path, e57Index) ->o3d.geometry.PointCloud:
    """Convert pye57.E57scan to o3d.geometry.PointCloud

    Args:
        e57scan

    Returns:
        o3d.geometry.PointCloud
    """
    try:
        e57 = pye57.E57(e57Path)

        #get transformation
        header = e57.get_header(e57Index)
        quaternion=header.rotation
        translation=header.translation
        r = R.from_quat([quaternion[3],quaternion[0],quaternion[1],quaternion[2]])
        rotation_matrix=e57_fix_rotation_order(r.as_matrix())
        transform=rotation_and_translation_to_transformation_matrix(rotation_matrix,translation)

        #get raw geometry (no transformation)
        raw_data = e57.read_scan_raw(e57Index)        
        x_ndarray=raw_data.get('cartesianX')
        y_ndarray=raw_data.get('cartesianY')
        z_ndarray=raw_data.get('cartesianZ')
        array= np.vstack(( x_ndarray,y_ndarray,z_ndarray)).T
        points = o3d.utility.Vector3dVector(array)
        pcd=o3d.geometry.PointCloud(points)
        pcd.transform(transform)

        #get color or intensity
        colors=e57_get_colors(raw_data)
        if colors is not None:
            pcd.colors=colors

        #return transformed data
        return pcd
    except:
        print("Conversion from e57 to o3d.geometry.PointCloud failed!")
        return None    

def box_to_mesh(box:o3d.geometry) ->o3d.geometry.TriangleMesh:
    if type(box) is o3d.geometry.OrientedBoundingBox or type(box) is o3d.geometry.AxisAlignedBoundingBox:
        mesh=o3d.geometry.TriangleMesh()
        mesh.vertices=box.get_box_points()
        #triangles rotate counterclockwise
        mesh.triangles= o3d.cpu.pybind.utility.Vector3iVector(np.array([[0,2,1],
                            [0,1,3],
                            [0,3,2],
                            [1,6,3],
                            [1,7,6],
                            [1,2,7],
                            [2,3,5],
                            [2,5,4],
                            [2,4,7],
                            [3,4,5],
                            [3,6,4],
                            [4,6,7]])) 
        return mesh                  
    else:
        print('Incorrect geometry input. Only input o3d.geometry.AxisAlignedBoundingBox or o3d.geometry.OrientedBoundingBox or type(geometry)  ')
        return None 

def ifc_to_mesh(ifcElement:ifcopenshell.entity_instance)-> o3d.geometry.TriangleMesh: 
    """Convert an ifcOpenShell geometry to an Open3D TriangleMesh

    Args:
        ifcElement (ifcopenshell.entity_instance): IfcOpenShell Element parsed from and .ifc file. See BIMNode for more documentation.

    Returns:
        o3d.geometry.TriangleMesh: Open3D Mesh Geometry of the ifcElment boundary surface
    """    
    try:
        if ifcElement.get_info().get("Representation"): 
            # Set geometry settings and global coordinates as true
            settings = geom.settings() 
            settings.set(settings.USE_WORLD_COORDS, True) 
        
            # Extract vertices/faces of the IFC geometry
            shape = geom.create_shape(settings, ifcElement) 
            ifcVertices = shape.geometry.verts 
            ifcFaces = shape.geometry.faces 

            #Group the vertices and faces in a way they can be read by Open3D
            vertices = [[ifcVertices[i], ifcVertices[i + 1], ifcVertices[i + 2]] for i in range(0, len(ifcVertices), 3)]
            faces = [[ifcFaces[i], ifcFaces[i + 1], ifcFaces[i + 2]] for i in range(0, len(ifcFaces), 3)]

            #Convert grouped vertices/faces to Open3D objects 
            o3dVertices = o3d.utility.Vector3dVector(np.asarray(vertices))
            o3dTriangles = o3d.utility.Vector3iVector(np.asarray(faces))

            # Create the Open3D mesh object
            mesh=o3d.geometry.TriangleMesh(o3dVertices,o3dTriangles)
            if len(mesh.triangles)>1:
                return mesh
            else: 
                return None 
    except:
        print('ifcopenshell.entity_instance error')
        return None

def cartesian_bounds_to_open3d_axis_aligned_bounding_box(cartesianBounds:np.array) ->o3d.geometry.OrientedBoundingBox:
    """Convert cartesianBounds to Open3D Geometry

    Args:
        cartesianBounds (np.array): [xMin,xMax,yMin,yMax,zMin,zMax]

    Returns:
        o3d.geometry.OrientedBoundingBox: Open3D Geometry
    """
    points=get_bounding_points(cartesianBounds)
    open3dOrientedBoundingBox=o3d.geometry.OrientedBoundingBox.create_from_points(points)
    return open3dOrientedBoundingBox

def rotation_and_translation_to_transformation_matrix(rotation: np.array, translation: np.array)->np.array:
    """
    rotation [3,3]
    translation [3,1]
    """
    r=np.asarray(rotation)
    if r.size==9 and len(translation) ==3:    
        return np.array([[ r[0,0],r[0,1],r[0,2], translation[0]],
                        [ r[1,0],r[1,1],r[1,2], translation[1]],
                        [ r[2,0],r[2,1],r[2,2], translation[2]],
                        [ 0,0,0,1]])
    else:
        return None

def mesh_to_pcd(mesh:o3d.geometry.TriangleMesh,voxelSize : float = 0.1) -> o3d.geometry.PointCloud:
    """Sample a point cloud on a triangle mesh (Open3D)

    Args:
        mesh (o3d.geometry.TriangleMesh) : source geometry
        voxel_size (float) : spatial resolution of the point cloud e.g. 0.1m

    Returns:
        An o3d.geometry.PointCloud() 
    """
    pcd = o3d.geometry.PointCloud()
    for submesh in mesh:
        k = round(submesh.get_surface_area() * 1000)
        submeshpcd = submesh.sample_points_uniformly(number_of_points = k, use_triangle_normal=True)
        pcd.__iadd__(submeshpcd)
    pcd = pcd.voxel_down_sample(voxelSize)    
    return pcd

def oriented_bounds_to_open3d_oriented_bounding_box(orientedBounds : np.array) -> o3d.geometry.OrientedBoundingBox:
    """Convert 8 bounding points to Open3D Geometry

    Args:
        orientedBounds (np.array): [8x3] bounding points

    Returns:
        o3d.geometry.OrientedBoundingBox: Open3D Geometry
    """
    boxPointsVector = o3d.utility.Vector3dVector(orientedBounds)
    open3dOrientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(boxPointsVector)
    return open3dOrientedBoundingBox


#### GEOMETRY GENERATION ####

def generate_virtual_images(geometries: List[o3d.geometry.Geometry],cartesianTransforms: List[np.array],width:int=640,height:int=480,f:float=400)-> o3d.geometry.Image:
    """Generate a set of Open3D Images from cartesianTransforms and geometries. 
    The same intrinsic camera parameters are used for all cartesianTransforms that are passed to the function

    .. image:: ../pics/rendering3.PNG

    Args:
        geometries (List[o3d.geometry]):o3d.geometry.PointCloud or o3d.geometry.TriangleMesh
        cartesianTransforms (List[np.array 4x4]): [Rt]
        width (int, optional): image width in pix. Defaults to 640.
        height (int, optional): image height in pix. Defaults to 480.
        f (float, optional): focal length in pix. Defaults to 400.

    Returns:
        List[o3d.cpu.pybind.geometry.Image]
    """
    #set renderer
    render = o3d.visualization.rendering.OffscreenRenderer(width,height)
    mtl=o3d.visualization.rendering.MaterialRecord()
    mtl.base_color = [1.0, 1.0, 1.0, 1.0]  # RGBA
    mtl.shader = "defaultUnlit"

    # set internal camera orientation
    fx=f
    fy=f
    cx=width/2-0.5
    cy=width/2-0.5
    intrinsic=o3d.camera.PinholeCameraIntrinsic(width,height,fx,fy,cx,cy)
    
    #add geometries
    geometries=ut.item_to_list(geometries)
    for idx,geometry in enumerate(geometries):
        render.scene.add_geometry(str(idx),geometry,mtl) 

    #set cameras and generate images
    list=[]
    for cartesianTransform in cartesianTransforms:
        extrinsic=np.linalg.inv(cartesianTransform)
        render.setup_camera(intrinsic,extrinsic)
        img = render.render_to_image()
        list.append(img)

    if len(list) !=0:
        return list
    else:
        return None

def generate_virtual_image(geometries: List[o3d.geometry.Geometry],pinholeCamera: o3d.camera.PinholeCameraParameters)-> o3d.geometry.Image:
    """Generate an Open3D Image from a set of geometries and an Open3D camera (). 

    Args:
        geometries (List[o3d.geometry]):o3d.geometry.PointCloud or o3d.geometry.TriangleMesh
        pinholeCamera (o3d.camera.PinholeCameraParameters): extrinsic (cartesianTransform) and intrinsic (width,height,f,principal point U and V) camera parameters

    Returns:
        o3d.cpu.pybind.geometry.Image or None
    """
    #create renderer
    width=pinholeCamera.intrinsic.width
    height=pinholeCamera.intrinsic.height
    render = o3d.visualization.rendering.OffscreenRenderer(width,height)

    # Define a simple unlit Material. (The base color does not replace the geometry colors)
    mtl=o3d.visualization.rendering.MaterialRecord()
    mtl.base_color = [1.0, 1.0, 1.0, 1.0]  # RGBA
    mtl.shader = "defaultUnlit"

    #set camera
    render.setup_camera(pinholeCamera.intrinsic,pinholeCamera.extrinsic)

    #add geometries
    geometries=ut.item_to_list(geometries)

    for idx,geometry in enumerate(geometries):
        render.scene.add_geometry(str(idx),geometry,mtl) 

    #render image
    img = render.render_to_image()

    if img is not None:
        return img
    else:
        return None


#### GEOMETRY MANIPULATION ####

def e57_get_colors(raw_data):
    """
    Extract color of intensity information from e57 raw data (3D data) and output Open3D o3d.utility.Vector3dVector(colors) 
    """   
    try:
        colorRed=raw_data.get('colorRed')
        colorGreen=raw_data.get('colorGreen')
        colorBlue=raw_data.get('colorBlue')
        intensity=raw_data.get('intensity')

        if colorRed is not None and colorGreen is not None and colorBlue is not None:
            if np.amax(colorRed)<=1:
                colors=np.c_[colorRed , colorGreen,colorBlue ]  
            elif np.amax(colorRed) <=255:
                colors=np.c_[colorRed/255 , colorGreen/255,colorBlue/255 ]  
            else:
                colorRed=(colorRed - np.min(colorRed))/np.ptp(colorRed)
                colorGreen=(colorGreen - np.min(colorGreen))/np.ptp(colorGreen)
                colorBlue=(colorBlue - np.min(colorBlue))/np.ptp(colorBlue)
                colors=np.c_[colorRed , colorGreen,colorBlue ]  
            return o3d.utility.Vector3dVector(colors) 

        elif intensity is not None:
            if np.amax(intensity) <=1:
                colors=np.c_[intensity , intensity,intensity ]  
            else:
                intensity=(intensity - np.min(intensity))/np.ptp(intensity)
                colors=np.c_[intensity , intensity,intensity ]  
            return o3d.utility.Vector3dVector(colors) 
    except:
        return None
    return None

def e57_fix_rotation_order(rotation_matrix:np.array) -> np.array:
    """
    thix switches the rotation from clockwise to counter-clockwise
    https://robotics.stackexchange.com/questions/10702/rotation-matrix-sign-convention-confusion
    Currently only changes the signs of elements [0,1,5,8]
    """
    r=rotation_matrix
    return [[-r[0,0],-r[0,1],r[0,2]],
            [r[1,0],r[1,1],-r[1,2]],
            [r[2,0],r[2,1],-r[2,2]]]

def crop_geometry(geometry:o3d.geometry, box:o3d.geometry.OrientedBoundingBox, subdivide:int = 0) ->o3d.geometry.TriangleMesh:
    """"Crop portion of a mesh/pointcloud that lies within an OrientedBoundingBox 

    .. image:: ../pics/selection_BB_mesh2.PNG

    Args:
        geometry (o3d.geometry.TriangleMesh or o3d.geometry.PointCloud)
        box (o3d.geometry.OrientedBoundingBox )
        subdivide (int): number of interations to increase the density of the mesh (1=x4, 2=x16, etc.)
        
    Returns:
        o3d.geometry.TriangleMesh or None
    """
    # transform box to axis aligned box 
    r=box.R
    t=box.center
    transformedbox=copy.deepcopy(box)
    transformedbox=transformedbox.translate(-t)
    transformedbox=transformedbox.rotate(r.transpose(),center=(0, 0, 0))
    
    # transform geometry to coordinate system of the box
    transformedGeometry=copy.deepcopy(geometry)
    transformedGeometry=transformedGeometry.translate(-t)
    transformedGeometry=transformedGeometry.rotate(r.transpose(),center=(0, 0, 0))

    # convert to pcd if geometry is a mesh (crop fails with mesh geometry)
    if type(geometry) is o3d.geometry.PointCloud:
        croppedGeometry=geometry.crop(transformedbox)             
    elif type(geometry) is o3d.geometry.TriangleMesh:
        if subdivide!=0:
            transformedGeometry=transformedGeometry.subdivide_midpoint(subdivide)
        indices=transformedbox.get_point_indices_within_bounding_box(transformedGeometry.vertices) # this is empty
        if len(indices) !=0:
            croppedGeometry=transformedGeometry.select_by_index(indices,cleanup=True)
        else:
            return None

    # return croppedGeometry to original position
    if croppedGeometry is not None:
        croppedGeometry=croppedGeometry.rotate(r,center=(0, 0, 0))
        croppedGeometry=croppedGeometry.translate(t)
        return croppedGeometry
    else:
        return None

def expand_box (box: o3d.geometry.OrientedBoundingBox, u=5.0,v=5.0,w=5.0) -> o3d.geometry.OrientedBoundingBox:
    """expand an o3d.geometry.OrientedBoundingBox in u(x), v(y) and w(z) direction with a certain offset

    Args:
        box (o3d.geometry.OrientedBoundingBox)
        u (float, optional): Offset in X. Defaults to 5.0.
        v (float, optional): Offset in Y. Defaults to 5.0.
        w (float, optional): Offset in Z. Defaults to 5.0.

    Returns:
        o3d.geometry.OrientedBoundingBox
    """    
    center = box.get_center()
    orientation = box.R 
    extent = box.extent + [u, w, v] 
    return o3d.geometry.OrientedBoundingBox(center,orientation,extent) 

def join_geometries(geometries):
    if type(geometries) is o3d.geometry.TriangleMesh:
        joined=o3d.geometry.TriangleMesh()
        for geometry in geometries:
            if geometry is not None and len(geometry.vertices) != 0:
                joined +=geometry
        return joined
    elif type(geometries) is o3d.geometry.PointCloud:
        joined=o3d.geometry.PointCloud()
        for geometry in geometries:
            if geometry is not None and len(geometry.points) != 0:
                joined +=geometry
        return joined
    else:
        print('submit point clouds or meshes')
        return None

def pointcloud_filter_by_distance(source: o3d.geometry.PointCloud, cutters, threshold : float =0.10) -> o3d.geometry.PointCloud:
    """"Select the portion of a pointcloud that lies within a range of another mesh/point cloud 
    
    Args:
        source (o3d.geometry.PointCloud) : point cloud to filter
        cutters (o3d.geometry.TriangleMesh or o3d.geometry.PointCloud): list of reference data
        threshold (float): threshold Euclidean distance for the filtering
        invert (bool): 'True' to retain point closer by than a threshold

    Returns:
        outputmesh(o3d.geometry.PointCloud)
    """
    #if no list, list
    cutters=ut.item_to_list(cutters)
    joined=join_geometries(cutters)

    #if cutters are mesh, sample mesh
    if type(cutters) is o3d.geometry.TriangleMesh:
        reference=joined.sample_points_uniformly(number_of_points=1000000) 
    elif type(cutters) is o3d.geometry.PointCloud:
        reference=joined
    else:
        print('submit point cloud or  mesh as cutters')
        return None

    distances=source.compute_point_cloud_distance(reference) #10s to calculate
    indices=[ idx for idx,distance in enumerate(distances) if distance <threshold] #this takes 30s
    if len(indices) !=0:
        return source.select_by_index(indices)
    else:
        return None 


#### GEOMETRY PROPERTIES

def get_box_inliers(sourceBox:o3d.geometry.OrientedBoundingBox, testBoxes: List[o3d.geometry.OrientedBoundingBox])->List[int]:
    """"
    Return the indices of the testBoxes of which the bounding points lie within the sourceBox

    Args:
        sourceBox (o3d.geometry.OrientedBoundingBox):   box to test
        testBoxes (o3d.geometry.OrientedBoundingBox):   boxes to test
    Returns:
        list (List[int]):       indices of testBoxes

    """
    #Convert to list
    testBoxes=ut.item_to_list(testBoxes) 
    array= [False] * len(testBoxes)
    for idx,testbox in enumerate(testBoxes):
        if testbox is not None:
            points=testbox.get_box_points()
            indices=testbox.get_point_indices_within_bounding_box(points)        
            if len(indices) !=0:
                array[idx]= True
    list = [ i for i in range(len(array)) if array[i]]
    return list

def get_box_intersections(sourceBox:o3d.geometry.OrientedBoundingBox, testBoxes: List[o3d.geometry.OrientedBoundingBox])->List[int]:
    """" Return indices of testBoxes of which the geometry intersects with the sourceBox.
    2 oriented bounding boxes (A,B) overlap if the projection from B in the coordinate system of A on all the axes overlap. 
    The projection of B on the oriented axes of A is simply the coordinate range for that axis.

    Args:
        sourceBox (o3d.geometry.OrientedBoundingBox):   box to test
        testBoxes (o3d.geometry.OrientedBoundingBox):   boxes to test
    Returns:
        list (List[int]):       indices of testBoxes

    """       
    #convert to list
    testBoxes=ut.item_to_list(testBoxes)

    array= [False] * len(testBoxes)

    for idx,testbox in enumerate(testBoxes):
    # compute axes of box A
        if testbox is not None:
            #transform box to aligned coordinate system
            transformedboxA=copy.deepcopy(sourceBox)
            transformedboxA=transformedboxA.translate(-sourceBox.center)
            transformedboxA=transformedboxA.rotate(sourceBox.R.transpose(),center=(0, 0, 0))
            
            #transform testbox to aligned coordinate system
            transformedboxB=copy.deepcopy(testbox)
            transformedboxB=transformedboxB.translate(-sourceBox.center)
            transformedboxB=transformedboxB.rotate(sourceBox.R.transpose(),center=(0, 0, 0))

            # compute coordinates of bounding points of B in coordinate system of A
            minA=transformedboxA.get_min_bound()
            minB=transformedboxB.get_min_bound()
            maxA=transformedboxA.get_max_bound()
            maxB=transformedboxB.get_max_bound()

            if (maxB[0]>=minA[0] and minB[0]<=maxA[0]):
                if (maxB[1]>=minA[1] and minB[1]<=maxA[1]):
                    if (maxB[2]>=minA[2] and minB[2]<=maxA[2]):
                        array[idx]= True  
    # return index if B overlaps with A in all three axes u,v,w 
    list = [ i for i in range(len(array)) if array[i]]
    return list

def get_center(mesh:o3d.geometry.TriangleMesh,triangle:np.array) -> np.array:
    """
    Compute center of an Open3D mesh face
    """
    points=np.array([mesh.vertices[triangle[0]],
                    mesh.vertices[triangle[1]],
                    mesh.vertices[triangle[2]]])
    # point4=mesh.vertices[triangle[3]] # check if Open3D supports quads
    if points.shape[1] ==3:        
        return np.mean(points,axis=0)
    else:
        return None

def get_triangle_centers(mesh:o3d.geometry.TriangleMesh) -> np.array:
    """
    Compute centers of all Open3D mesh faces
    """
    centers=np.empty((len(mesh.triangles),3))
    for idx,row in enumerate(mesh.triangles):
        points=np.array([mesh.vertices[row[0]],
                    mesh.vertices[row[1]],
                    mesh.vertices[row[2]]])
        centers[idx]=np.mean(points,axis=0)
    return centers

def get_cartesian_bounds(geometry : o3d.geometry) ->np.array:
    """Get cartesian bounds from Open3D geometry

    Args:
        geometry (o3d.geometry): Open3D geometry supertype (PointCloud, TriangleMesh, OrientedBoundingBox, etc.)

    Returns:
        np.array: [xMin,xMax,yMin,yMax,zMin,zMax]
    """
    max=geometry.get_max_bound()
    min=geometry.get_min_bound()
    return np.array([min[0],max[0],min[1],max[1],min[2],max[2]])

def get_oriented_bounds(geometry : o3d.geometry.OrientedBoundingBox ) -> np.array:
    """Get the 8 corner points of the oriented bounding box. THIS CODE SEEMS OBSOLETE

    Args:
        geometry (o3d.geometry): Open3D geometry supertype (PointCloud, TriangleMesh, OrientedBoundingBox, etc.)

    Returns:
        np.array: [8x3]
    """
    orientedBoundingBox = geometry.get_oriented_bounding_box()
    return np.asarray(orientedBoundingBox.get_box_points())

def get_center_of_oriented_bounds(orientedBounds: np.array) -> np.array:
    boxPointsVector = o3d.utility.Vector3dVector(orientedBounds)
    open3dOrientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(boxPointsVector)
    return np.asarray(open3dOrientedBoundingBox.get_center())

def get_rotation_of_oriented_bounds(orientedBounds: np.array) -> np.array:
    boxPointsVector = o3d.utility.Vector3dVector(orientedBounds)
    open3dOrientedBoundingBox = o3d.geometry.OrientedBoundingBox.create_from_points(boxPointsVector)
    return np.asarray(open3dOrientedBoundingBox.R)

def get_center_of_cartesian_bounds(cartesianBounds:np.array)-> np.array:
    if cartesianBounds.size ==6:
        x=(cartesianBounds[1]-cartesianBounds[0])/2
        y=(cartesianBounds[3]-cartesianBounds[2])/2
        z=(cartesianBounds[5]-cartesianBounds[4])/2
        return np.array([x,y,z])
    else:
        return None

def get_center_of_points(points:np.array)-> np.array: 
    if points.shape[1] ==3:        
        return np.mean(points,axis=0)
    else:
        return None

def get_bounding_points(cartesianBounds:np.array) -> List[o3d.utility.Vector3dVector]:
    array=np.empty((8,3))
    xMin=cartesianBounds[0]
    xMax=cartesianBounds[1]
    yMin=cartesianBounds[2]
    yMax=cartesianBounds[3]
    zMin=cartesianBounds[4]
    zMax=cartesianBounds[5]

    #maybe these should be ordered a bit more 
    array[0]=np.array([xMin,yMin,zMin])
    array[1]=np.array([xMin,yMin,zMax])
    array[2]=np.array([xMin,yMax,zMin])
    array[3]=np.array([xMin,yMax,zMax])
    array[4]=np.array([xMax,yMin,zMin])
    array[5]=np.array([xMax,yMin,zMax])
    array[6]=np.array([xMax,yMax,zMin])
    array[7]=np.array([xMax,yMax,zMax])

    return o3d.utility.Vector3dVector(array)

def get_translation(cartesianTransform:np.array) -> np.array:
    if cartesianTransform.size ==16:
        return np.array([cartesianTransform[0,3],cartesianTransform[1,3],cartesianTransform[2,3]])
    else:
        return None
    
def get_rotation(cartesianTransform:np.array) -> np.array:
    if cartesianTransform.size ==16:
        return np.array([[cartesianTransform[0,1],cartesianTransform[0,2],cartesianTransform[0,3]],
                        [cartesianTransform[1,1],cartesianTransform[1,2],cartesianTransform[1,3]],
                        [cartesianTransform[2,1],cartesianTransform[2,2],cartesianTransform[2,3]]])
    else:
        return None


#### GEOMETRY TESTING ####

def mesh_collisions_open3d(sourceMesh: o3d.geometry.TriangleMesh, meshes: List[o3d.geometry.TriangleMesh], t_d:float=0.5) -> List[int]:
    """Return the index of the geometries that collide the sourceMesh
        NOT IMPLEMENTED
    """
    meshes=ut.item_to_list(meshes)
    if len(sourceMesh.triangles) !=0:
        # select those faces that are within proximity of each other
        box=sourceMesh.get_oriented_bounding_box()
        expand_box(box,u=t_d,v=t_d,w=t_d)

        boxes=np.empty(len(meshes),dtype=o3d.geometry.OrientedBoundingBox)
        for idx,mesh in enumerate(meshes):
            referenceBox=mesh.get_oriented_bounding_box()

            # crop both meshes based on the expanded bounding box
            croppedReferenceMesh=crop_geometry(mesh,box).triangles
            croppedSourceMesh=crop_geometry(sourceMesh,referenceBox).triangles

            # check if reference edges intersect with sourcemesh faces
            croppedReferenceMesh.edges

                # get all edges of refernence and traingles of source

                # compute mathmetical point of intersection between the lines and each plane

                # check if barymetric coordinates of intersection point lie within the triangle => if so, there is a collision#  
                # # if Mesh
                # # find vertices
                # mesh=o3d.geometry.TriangleMesh()
                # mesh.vertices 


                # mesh.remove_vertices_by_index()
                # mesh.remove_triangles_by_index()
                # points=mesh.vertices
                # faces=mesh.triangles
                # mesh.merge_close_vertices(0.01)
                # mesh.remove_duplicated_vertices()
                # triangle_mask=False*len(mesh.triangles)
                # cleanedMesh=mesh.remove_triangles_by_mask(triangle_mask)
                # mesh.remove_unreferenced_vertices()

                # CleanedMesh=mesh.select_by_index(indices,cleanup=True)
                # smoothMesh=mesh.subdivide_midpoint(1)
        return False

def mesh_intersection_raycasting(source:o3d.geometry.TriangleMesh, cutter: o3d.geometry.TriangleMesh, inside : Boolean = True,strict : Boolean = True ) -> o3d.geometry.TriangleMesh:
    """"Select portion of a mesh that lies within a mesh shape (if not closed, convexhull is called)
    
    Args:
        source (o3d.geometry.TriangleMesh) : mesh to cut
        cutter (o3d.geometry.TriangleMesh) : mesh that cuts
        inside (bool): 'True' to retain inside
        strict (bool): 'True' if no face vertex is allowed outside the bounds, 'False' allows 1 vertex to lie outside

    Returns:
        outputmesh(o3d.geometry.TriangleMesh)
    """
    #check if cutter is closed 
    if not cutter.is_watertight():
        cutter=cutter.compute_convex_hull()

    #check if mesh has normals? not needed

    #raycast the scene to determine which points are inside
    query_points=o3d.core.Tensor(np.asarray(source.vertices),dtype=o3d.core.Dtype.Float32 )
    cpuMesh = o3d.t.geometry.TriangleMesh.from_legacy(cutter)
    scene = o3d.t.geometry.RaycastingScene()
    geometry = scene.add_triangles(cpuMesh)
    ans=scene.compute_occupancy(query_points)
    
    if inside:
        occupancyList=ans==0
    else:
        occupancyList=ans>0

    outputmesh=copy.deepcopy(source)
    if strict:
        outputmesh.remove_vertices_by_mask(occupancyList)
        outputmesh.remove_degenerate_triangles()
        outputmesh.remove_unreferenced_vertices
    else:
        triangles=copy.deepcopy(np.asarray(outputmesh.triangles)) #can we remove this one?
        indices= [i for i, x in enumerate(occupancyList) if x == True]
        #mark all unwanted points as -1
        triangles[~np.isin(triangles,indices)] = -1
        # if 2/3 vertices are outside, flag the face
        occupancyList=np.ones ((triangles.shape[0],1), dtype=bool)

        for idx,row in enumerate(triangles):
            if (row[0] ==-1 and row[1]==-1) or (row[0] ==-1 and row[2]==-1) or (row[1] ==-1 and row[2]==-1):
                occupancyList[idx]=False
        outputmesh.remove_triangles_by_mask(occupancyList)
        outputmesh.remove_unreferenced_vertices()
    return outputmesh

def voxel_traversal(pcd, origin, direction, voxelSize, maxRange = 100): 
    """Cast a ray in a voxel array created from the pcd"""

    pcd_Voxel = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=voxelSize)
    #the starting index of the voxels
    voxel_origin = pcd.get_voxel(origin)
    iX = math.floor(origin[0] * voxelSize) / voxelSize
    iY = math.floor(origin[1] * voxelSize) / voxelSize
    iZ = math.floor(origin[2] * voxelSize) / voxelSize

    stepX = np.sign(direction[0])
    stepY = np.sign(direction[1])
    stepZ = np.sign(direction[2])

    tDeltaX = 1/direction[0] * voxelSize
    tDeltaY = 1/direction[1] * voxelSize
    tDeltaZ = 1/direction[2] * voxelSize

    tMaxX = origin[0]
    tMaxY = origin[1]
    tMaxZ = origin[2]

    for i in range(0,maxRange):
        # check if the current point is in a occupied voxel
        if(pcd_Voxel.check_if_included(o3d.utility.Vector3dVector([[iX * voxelSize, iY * voxelSize, iY * voxelSize]]))[0]):
            distance = np.linalg.norm(np.array([iX * voxelSize, iY * voxelSize, iY * voxelSize]) - origin)
            return True, distance

        if(tMaxX < tMaxY):
            if(tMaxX < tMaxZ):
                #traverse in the X direction
                tMaxX += tDeltaX
                iX += stepX
            else:
                #traverse in the Z direction
                tMaxZ += tDeltaZ
                iZ += stepZ
        else:
            if(tMaxY < tMaxZ):
                #traverse in the Y direction
                tMaxY += tDeltaY
                iY += stepY
            else:
                #traverse in the Z direction
                tMaxZ += tDeltaZ
                iZ += stepZ

    return False, math.inf


#### OPEN3D VISUALISATION ####

def create_3d_camera(pos = [0,0,0], rotation  = np.eye(3), scale = 1.0):
    "Returns a geometry lineset object that represents a camera in 3D space"

    box = o3d.geometry.TriangleMesh.create_box(1.6,0.9, 0.1)
    box.translate((-0.8, -0.45, -0.05))
    box.scale(scale, center=(0, 0, 0))
    box.rotate(rotation)
    box.translate(pos)
    return box

def show_geometries(geometries, color = False):
    "displays the array of meshes in a 3D view"

    viewer = o3d.visualization.Visualizer()
    viewer.create_window()
    frame = o3d.geometry.TriangleMesh.create_coordinate_frame()
    viewer.add_geometry(frame)
    for i, geometry in enumerate(geometries):
        if color:
            geometry.paint_uniform_color(matplotlib.colors.hsv_to_rgb([float(i)/len(geometries),0.8,0.8]))
        viewer.add_geometry(geometry)
    opt = viewer.get_render_option()
    opt.background_color = np.asarray([1,1,1])
    opt.light_on = True
    viewer.run()
    viewer.destroy_window()

def save_view_point(geometry, filename):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(geometry)
    vis.run()  # user changes the view and press "q" to terminate
    param = vis.get_view_control().convert_to_pinhole_camera_parameters()
    o3d.io.write_pinhole_camera_parameters(filename, param)
    vis.destroy_window()
