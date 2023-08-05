import trimesh
import fcl
import open3d as o3d
import numpy as np
from typing import List
from xmlrpc.client import Boolean
import geomapi.geometryutils as gt1
import geomapi.utils as ut
#trimesh
#PyMesh
#pygalmesh => builds upon eigen and cgal
#Plyable

#IMPORT PACKAGES
# import trimesh


def cap_mesh(test):
    """UNTESTED CODE
    """
      # the plane we're using
    normal = trimesh.unitize([1,1,1])
    origin = m.center_mass

    # get a section as a Path3D object
    s = m.section(plane_origin=origin,
                  plane_normal=normal)

    # transform the Path3D onto the XY plane so we can triangulate
    on_plane, to_3D = s.to_planar()

    # triangulate each closed region of the 2D cap
    v, f = [], []
    for polygon in on_plane.polygons_full:
        tri = trimesh.creation.triangulate_polygon(polygon)
        v.append(tri[0])
        f.append(tri[1])
        
    # append the regions and re- index
    vf, ff = trimesh.util.append_faces(v, f)
    # three dimensionalize polygon vertices
    vf = np.column_stack((vf, np.zeros(len(vf))))
    # transform points back to original mesh frame
    vf = trimesh.transform_points(vf, to_3D)
    # flip winding of faces for cap
    ff = np.fliplr(ff)

    # the mesh for the planar cap
    cap = trimesh.Trimesh(vf, ff)

    # get the uncapped slice
    sliced = m.slice_plane(plane_origin=origin,
                           plane_normal=normal)

    # append the cap to the sliced mesh
    capped = sliced + cap


def mesh_to_trimesh(geometry: o3d.geometry) -> trimesh.Trimesh:
    """
    Convert open3D.geometry.TriangleMesh to trimesh.Trimesh
    """
    if type(geometry) is o3d.geometry.OrientedBoundingBox or type(geometry) is o3d.geometry.AxisAlignedBoundingBox:
        geometry=gt1.box_to_mesh(geometry)
    
    if type(geometry) is o3d.geometry.TriangleMesh and len(geometry.vertices) !=0:
        vertices= geometry.vertices
        faces= geometry.triangles
        face_normals=None
        vertex_normals=None
        face_colors=None
        vertex_colors=None

        if geometry.has_triangle_normals():
            face_normals=geometry.triangle_normals
        if geometry.has_vertex_normals():
            vertex_normals=geometry.vertex_normals
        if geometry.has_triangle_uvs(): # this is probably not correct
            face_colors=geometry.triangle_uvs
        if geometry.has_vertex_colors():
            vertex_colors=geometry.vertex_colors

        try:
            triMesh= trimesh.Trimesh(vertices, faces, face_normals=face_normals, vertex_normals=vertex_normals, face_colors=face_colors, vertex_colors=vertex_colors)
            return triMesh
        except:
            print('Open3D to Trimesh failed')
            return None
    else:
        print('Incorrect geometry input. Only input o3d.geometry.TriangleMesh,o3d.geometry.AxisAlignedBoundingBox or o3d.geometry.OrientedBoundingBox or type(geometry)  ')
        return None

def mesh_intersection_convex_hull(source:trimesh.Trimesh, cutter: trimesh.Trimesh, inside : Boolean = True ) -> trimesh.Trimesh:
    """"Cut a portion of a mesh that lies within/outside the convex hull of another mesh
    
    Args:
        source (trimesh.Trimesh):   mesh that will be cut
        cutter (trimesh.Trimesh):   mesh of which the faces are used for the cuts. Face normals should point outwards (positive side)
        inside (Boolean):           True if retain the inside of the intersection
    Returns:
        mesh:       trimesh.Trimesh 
        None:       if no data was retained
    """
    #compute faces and centers
    convexhull=cutter.convex_hull
    plane_normals=convexhull.face_normals
    plane_origins=convexhull.triangles_center

    if inside: # retain inside
        return(source.slice_plane(plane_origins, -1*plane_normals))
    else:# retain outside
        #cut source mesh for every slicing plane on the box
        meshes=[]
        for n, o in zip(plane_normals, plane_origins):
            tempMesh= source.slice_plane(o, n)
            if not tempMesh.is_empty:
                meshes.append(tempMesh)
        if len(meshes) !=0: # gather pieces
            combined = trimesh.util.concatenate( [ meshes ] )
            combined.merge_vertices(merge_tex =True,merge_norm =True )
            combined.remove_duplicate_faces()
            return combined
        else:
            return None


def mesh_collisions_trimesh(sourceMesh: o3d.geometry.TriangleMesh, meshes: List[o3d.geometry.TriangleMesh]) -> List[int]:

    if type(sourceMesh) is o3d.geometry.TriangleMesh and len(sourceMesh.triangles) >0:
        myTrimesh=mesh_to_trimesh(sourceMesh)
        meshes=ut.item_to_list(meshes)
        # add all geometries to the collision manager
        collisionManager=trimesh.collision.CollisionManager()
        for idx,mesh in enumerate(meshes):
            if type(mesh) is o3d.geometry.TriangleMesh and len(mesh.triangles) >1:
                referenceTrimesh=mesh_to_trimesh(mesh)
                collisionManager.add_object(idx,referenceTrimesh)

        # report the collisions with the sourceMesh
        (is_collision, names ) = collisionManager.in_collision_single(myTrimesh, transform=None, return_names=True, return_data=False)    
        if is_collision:
            list=[int(name) for name in names]
            return list
    return None
