# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 20:40:37 2022

@author: Will

Provides modelling functionality 
"""
# Modelling options
##############################################################################
def add(mws, component1, compenent2):
    
    solid = mws.Solid
    solid.Add(component1, compenent2)
    
def subtract(mws, component1, component2):
    
    solid = mws.Solid
    solid.Subtract(component1, component2)
    
def align_wcs_with_face(mws):
    
    wcs = mws.WCS
    wcs.AlignWCSWithSelected('Face')

def align_wcs_with_point(mws):
    
    wcs = mws.WCS
    wcs.AlignWCSWithSelected('Point')

def clear_picks(mws):
    
    pick = mws.Pick
    pick.ClearAllPicks()
    
def pick_edge(mws, componentName, position):
    
    pick = mws.Pick
    pick.PickEdgeFromId((f'component1:{componentName}'), str(position), str(position))

def pick_face(mws, name, _id):
    
    pick = mws.Pick
    pick.PickFaceFromId((f'component1:{name}'), str(_id))   
    
def pick_face_from_point(mws, component, name, xPoint, yPoint, zPoint):
    
    pick = mws.Pick
    pick.PickFaceFromPoint((f'component1:{name}'), str(xPoint), str(yPoint), str(zPoint))
    
def pick_mid_point(mws, name, _id):
    
    pick = mws.Pick
    pick.PickMidpointFromId((f'component1:{name}'), str(_id))

    
# Shapes
##############################################################################
def brick(mws, Name, component, material, xrange, yrange, zrange):
    
    brick = mws.Brick
    brick.Reset()
    brick.Name(Name)
    brick.component(component)
    brick.Material(material)
    brick.xrange(str(xrange[0]), str(xrange[1]))
    brick.yrange(str(yrange[0]), str(yrange[1]))
    brick.zrange(str(zrange[0]), str(zrange[1]))
    brick.Create
    format(brick)

def cylinder(mws, Name, component, material, Axis, OuterRadius, InnerRadius, Xcenter, Ycenter, Zrange):
    
    cylinder = mws.Cylinder
    cylinder.Reset()
    cylinder.Name(Name)
    cylinder.Component(component)
    cylinder.Material(material)
    cylinder.Axis(Axis)
    cylinder.Outerradius(OuterRadius)
    cylinder.Innerradius(InnerRadius)

    if Axis == 'Z':
        cylinder.Xcenter(str(Xcenter))
        cylinder.Ycenter(str(Ycenter))
        cylinder.Zrange(str(Zrange[0]), str(Zrange[1]))
    elif Axis == 'X':
        cylinder.Ycenter(str(Ycenter))
        cylinder.Zcenter(str(Xcenter))
        cylinder.Xrange(str(Zrange[0]), str(Zrange[1]))
    elif Axis == 'Y':
        cylinder.Xcenter(str(Xcenter))
        cylinder.Zcenter(str(Ycenter))
        cylinder.Yrange(str(Zrange[0]), str(Zrange[1]))

    cylinder.Create()
    format(cylinder)

def sphere(mws, name, component, material, axis, centreRadius, topRadius, bottomRadius, centre):
    
    sphere = mws.Sphere
    sphere.Reset()
    sphere.Name(name)
    sphere.Component(component)
    sphere.Material(material)
    sphere.Axis(axis)
    sphere.CenterRadius(str(centreRadius))
    sphere.TopRadius(str(topRadius))
    sphere.BottomRadius(str(bottomRadius))
    sphere.Centre(str(centre(0)), str(centre(1)), str(centre(2)))
    sphere.Segments('0')
    sphere.Create()
