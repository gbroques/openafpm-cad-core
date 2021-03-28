"""
Module to export to Wavefront .obj format.

See:
  https://en.wikipedia.org/wiki/Wavefront_.obj_file

Adapted from:
  https://github.com/FreeCAD/FreeCAD/blob/0.19.1/src/Mod/Arch/importOBJ.py#L149-L273

Adapting this code is somewhat of a hack, but in the future we will use glTF instead. 

Modifications:
  * Use object Label instead of Name for object name.
  * Remove mtl or materials generation.
  * Return .obj file contents as string instead of writing to a file.
"""

import os
import sys

import Draft
import DraftGeomUtils
import FreeCAD
import Mesh
import MeshPart
import Part

if FreeCAD.GuiUp:
    from DraftTools import translate
else:
    # \cond
    def translate(context, text):
        return text
    # \endcond


p = Draft.precision()

__all__ = ['export']


def export(exportList) -> str:
    """
    Transforms a list of objects into a Wavefront .obj file contents.
    """
    lines = []

    offsetv = 1
    offsetvn = 1

    objects = _ungroup_objects(exportList)
    for obj in objects:
        if obj.isDerivedFrom("Part::Feature") or obj.isDerivedFrom("Mesh::Feature") or obj.isDerivedFrom("App::Link"):
            hires = None
            if FreeCAD.GuiUp:
                visible = obj.ViewObject.isVisible()
                if obj.ViewObject.DisplayMode == "HiRes":
                    # check if high-resolution object is available
                    if hasattr(obj, "HiRes"):
                        if obj.HiRes:
                            if obj.HiRes.isDerivedFrom("Mesh::Feature"):
                                m = obj.HiRes.Mesh
                            else:
                                m = obj.HiRes.Shape
                            hires = m.copy()
                            hires.Placement = obj.Placement.multiply(
                                m.Placement)
                    if not hires:
                        if hasattr(obj, "CloneOf"):
                            if obj.CloneOf:
                                if hasattr(obj.CloneOf, "HiRes"):
                                    if obj.CloneOf.HiRes:
                                        if obj.CloneOf.HiRes.isDerivedFrom("Mesh::Feature"):
                                            m = obj.CloneOf.HiRes.Mesh
                                        else:
                                            m = obj.CloneOf.HiRes.Shape
                                        hires = m.copy()
                                        hires.Placement = obj.Placement.multiply(
                                            obj.CloneOf.Placement).multiply(m.Placement)
            else:
                visible = True
            if visible:
                if hires:
                    vlist, vnlist, elist, flist = _getIndices(
                        obj, hires, offsetv, offsetvn)
                else:
                    if hasattr(obj, "Shape") and obj.Shape:
                        vlist, vnlist, elist, flist = _getIndices(
                            obj, obj.Shape, offsetv, offsetvn)
                    elif hasattr(obj, "Mesh") and obj.Mesh:
                        vlist, vnlist, elist, flist = _getIndices(
                            obj, obj.Mesh, offsetv, offsetvn)
                if vlist is None:
                    FreeCAD.Console.PrintError(
                        "Unable to export object " + obj.Label + ". Skipping.\n")
                else:
                    offsetv += len(vlist)
                    offsetvn += len(vnlist)
                    lines.append('o ' + obj.Label)

                    for v in vlist:
                        lines.append('v' + v)
                    for vn in vnlist:
                        lines.append('vn' + vn)
                    for e in elist:
                        lines.append('l' + e)
                    for f in flist:
                        lines.append('f' + f)
    return '\n'.join(lines) + '\n'


def _getIndices(obj, shape, offsetv, offsetvn):
    "returns a list with 2 lists: vertices and face indexes, offset with the given amount"
    vlist = []
    vnlist = []
    elist = []
    flist = []
    curves = None
    mesh = None

    if isinstance(shape, Part.Shape):
        for e in shape.Edges:
            try:
                if not isinstance(e.Curve, Part.LineSegment):
                    if not curves:
                        if obj.isDerivedFrom("App::Link"):
                            myshape = obj.LinkedObject.Shape.copy(False)
                            myshape.Placement = obj.LinkPlacement
                        else:
                            myshape = obj.Shape.copy(False)
                            myshape.Placement = obj.getGlobalPlacement()
                        mesh = MeshPart.meshFromShape(
                            Shape=myshape, LinearDeflection=0.1, AngularDeflection=0.7, Relative=True)
                        FreeCAD.Console.PrintWarning(
                            translate("Arch", "Found a shape containing curves, triangulating")+"\n")
                        break
            except Exception:  # unimplemented curve type
                if obj.isDerivedFrom("App::Link"):
                    if obj.Shape:
                        myshape = obj.Shape.copy(False)
                        myshape.Placement = obj.LinkPlacement
                    else:
                        myshape = obj.Shape.copy(False)
                        myshape.Placement = obj.getGlobalPlacement()
                    mesh = MeshPart.meshFromShape(
                        Shape=myshape, LinearDeflection=0.1, AngularDeflection=0.7, Relative=True)
                    FreeCAD.Console.PrintWarning(
                        translate("Arch", "Found a shape containing curves, triangulating")+"\n")
                    break
    elif isinstance(shape, Mesh.Mesh):
        mesh = shape
        curves = shape.Topology
    if mesh:
        for v in mesh.Topology[0]:
            vlist.append(" "+str(round(v[0], p))+" " +
                         str(round(v[1], p))+" "+str(round(v[2], p)))

        for vn in mesh.Facets:
            vnlist.append(
                " "+str(vn.Normal[0]) + " " + str(vn.Normal[1]) + " " + str(vn.Normal[2]))

        for i, vn in enumerate(mesh.Topology[1]):
            flist.append(" "+str(vn[0]+offsetv)+"//"+str(i+offsetvn)+" "+str(
                vn[1]+offsetv)+"//"+str(i+offsetvn)+" "+str(vn[2]+offsetv)+"//"+str(i+offsetvn))
    else:
        if curves:
            for v in curves[0]:
                vlist.append(" "+str(round(v.x, p))+" " +
                             str(round(v.y, p))+" "+str(round(v.z, p)))
            for f in curves[1]:
                fi = ""
                for vi in f:
                    fi += " " + str(vi + offsetv)
                flist.append(fi)
        else:
            for v in shape.Vertexes:
                vlist.append(" "+str(round(v.X, p))+" " +
                             str(round(v.Y, p))+" "+str(round(v.Z, p)))
            if not shape.Faces:
                for e in shape.Edges:
                    if DraftGeomUtils.geomType(e) == "Line":
                        ei = " " + \
                            str(_findVert(e.Vertexes[0],
                                          shape.Vertexes) + offsetv)
                        ei += " " + \
                            str(_findVert(e.Vertexes[-1],
                                          shape.Vertexes) + offsetv)
                        elist.append(ei)
            for f in shape.Faces:
                if len(f.Wires) > 1:
                    # if we have holes, we triangulate
                    tris = f.tessellate(1)
                    for fdata in tris[1]:
                        fi = ""
                        for vi in fdata:
                            vdata = Part.Vertex(tris[0][vi])
                            fi += " " + \
                                str(_findVert(vdata, shape.Vertexes) + offsetv)
                        flist.append(fi)
                else:
                    fi = ""
                    for e in f.OuterWire.OrderedEdges:
                        v = e.Vertexes[0]
                        ind = _findVert(v, shape.Vertexes)
                        if ind is None:
                            return None, None, None
                        fi += " " + str(ind + offsetv)
                    flist.append(fi)
    return vlist, vnlist, elist, flist


def _findVert(aVertex, aList):
    "finds aVertex in aList, returns index"
    for i in range(len(aList)):
        if (round(aVertex.X, p) == round(aList[i].X, p)):
            if (round(aVertex.Y, p) == round(aList[i].Y, p)):
                if (round(aVertex.Z, p) == round(aList[i].Z, p)):
                    return i
    return None


def _ungroup_objects(objects):
    ungrouped = []
    for obj in objects:
        if _is_group(obj):
            objs = _ungroup_objects(obj.Group)
            ungrouped.extend(objs)
        else:
            ungrouped.append(obj)
    return ungrouped


def _is_group(obj):
    group_types = {
        'App::DocumentObjectGroup',
        'App::Part'
    }
    return obj.TypeId in group_types
