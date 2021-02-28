"""
Module to export to Wavefront .obj format.

See:
  https://en.wikipedia.org/wiki/Wavefront_.obj_file

Adapted from:
  https://github.com/FreeCAD/FreeCAD/blob/0.19/src/Mod/Arch/importOBJ.py#L149-L273

Adapting this code is somewhat of a hack, but in the future we will use glTF instead. 

Modifications:
  * Use object Label instead of Name for object name.
"""

import os
import sys

import Arch
import Draft
import DraftGeomUtils
import FreeCAD
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

if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open


def decode(txt):

    if sys.version_info.major < 3:
        if isinstance(txt, unicode):
            return txt.encode("utf8")
    return txt


def export(exportList, filename, colors=None):
    """export(exportList,filename,colors=None):
    Called when freecad exports a file. exportList is a list
    of objects, filename is the .obj file to export (a .mtl
    file with same name will also be created together), and
    optionally colors can be a dict containing ["objectName:colorTuple"]
    pairs for use in non-GUI mode."""

    import codecs
    outfile = codecs.open(filename, "wb", encoding="utf8")
    ver = FreeCAD.Version()
    outfile.write("# FreeCAD v" + ver[0] + "." +
                  ver[1] + " build" + ver[2] + " Arch module\n")
    outfile.write("# http://www.freecadweb.org\n")
    offsetv = 1
    offsetvn = 1
    # objectslist = Draft.getGroupContents(exportList, walls=True,
    #                                      addgroups=True)
    # objectslist = Arch.pruneIncluded(objectslist)
    filenamemtl = filename[:-4] + ".mtl"
    materials = []
    outfile.write("mtllib " + os.path.basename(filenamemtl) + "\n")
    for obj in exportList:
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
                    vlist, vnlist, elist, flist = getIndices(
                        obj, hires, offsetv, offsetvn)
                else:
                    if hasattr(obj, "Shape") and obj.Shape:
                        vlist, vnlist, elist, flist = getIndices(
                            obj, obj.Shape, offsetv, offsetvn)
                    elif hasattr(obj, "Mesh") and obj.Mesh:
                        vlist, vnlist, elist, flist = getIndices(
                            obj, obj.Mesh, offsetv, offsetvn)
                if vlist is None:
                    FreeCAD.Console.PrintError(
                        "Unable to export object "+obj.Label+". Skipping.\n")
                else:
                    offsetv += len(vlist)
                    offsetvn += len(vnlist)
                    outfile.write("o " + obj.Label + "\n")

                    # write material
                    m = False
                    if hasattr(obj, "Material"):
                        if obj.Material:
                            if hasattr(obj.Material, "Material"):
                                outfile.write(
                                    "usemtl " + obj.Material.Name + "\n")
                                materials.append(obj.Material)
                                m = True
                    if not m:
                        if colors:
                            if obj.Name in colors:
                                color = colors[obj.Name]
                                if color:
                                    if isinstance(color[0], tuple):
                                        # this is a diffusecolor. For now, use the first color - #TODO: Support per-face colors
                                        color = color[0]
                                    #print("found color for obj",obj.Name,":",color)
                                    mn = Draft.getrgb(color, testbw=False)[1:]
                                    outfile.write("usemtl color_" + mn + "\n")
                                    materials.append(("color_" + mn, color, 0))
                        elif FreeCAD.GuiUp:
                            if hasattr(obj.ViewObject, "ShapeColor") and hasattr(obj.ViewObject, "Transparency"):
                                mn = Draft.getrgb(
                                    obj.ViewObject.ShapeColor, testbw=False)[1:]
                                outfile.write("usemtl color_" + mn + "\n")
                                materials.append(
                                    ("color_" + mn, obj.ViewObject.ShapeColor, obj.ViewObject.Transparency))

                    # write geometry
                    for v in vlist:
                        outfile.write("v" + v + "\n")
                    for vn in vnlist:
                        outfile.write("vn" + vn + "\n")
                    for e in elist:
                        outfile.write("l" + e + "\n")
                    for f in flist:
                        outfile.write("f" + f + "\n")
    outfile.close()
    FreeCAD.Console.PrintMessage(
        translate("Arch", "Successfully written") + " " + decode(filename) + "\n")
    if materials:
        outfile = pythonopen(filenamemtl, "w")
        outfile.write(
            "# FreeCAD v" + ver[0] + "." + ver[1] + " build" + ver[2] + " Arch module\n")
        outfile.write("# https://www.freecadweb.org\n")
        kinds = {"AmbientColor": "Ka ", "DiffuseColor": "Kd ",
                 "SpecularColor": "Ks ", "EmissiveColor": "Ke ", "Transparency": "Tr "}
        done = []  # store names to avoid duplicates
        for mat in materials:
            if isinstance(mat, tuple):
                if not mat[0] in done:
                    outfile.write("newmtl " + mat[0] + "\n")
                    outfile.write(
                        "Kd " + str(mat[1][0]) + " " + str(mat[1][1]) + " " + str(mat[1][2]) + "\n")
                    outfile.write("Tr " + str(mat[2]/100) + "\n")
                    done.append(mat[0])
            else:
                if not mat.Name in done:
                    outfile.write("newmtl " + mat.Name + "\n")
                    for prop in kinds:
                        if prop in mat.Material:
                            outfile.write(
                                kinds[prop] + mat.Material[prop].strip("()").replace(',', ' ') + "\n")
                    done.append(mat.Name)
        outfile.write("# Material Count: " + str(len(materials)))
        outfile.close()
        FreeCAD.Console.PrintMessage(
            translate("Arch", "Successfully written") + ' ' + decode(filenamemtl) + "\n")


def getIndices(obj, shape, offsetv, offsetvn):
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
                vn[1]+offsetv)+"//"+str(i+offsetvn)+" "+str(vn[2]+offsetv)+"//"+str(i+offsetvn)+" ")
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
                            str(findVert(e.Vertexes[0],
                                         shape.Vertexes) + offsetv)
                        ei += " " + \
                            str(findVert(e.Vertexes[-1],
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
                                str(findVert(vdata, shape.Vertexes) + offsetv)
                        flist.append(fi)
                else:
                    fi = ""
                    for e in f.OuterWire.OrderedEdges:
                        # print(e.Vertexes[0].Point,e.Vertexes[1].Point)
                        v = e.Vertexes[0]
                        ind = findVert(v, shape.Vertexes)
                        if ind is None:
                            return None, None, None
                        fi += " " + str(ind + offsetv)
                    flist.append(fi)
    return vlist, vnlist, elist, flist
