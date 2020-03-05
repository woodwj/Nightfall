import math
from settings import *
import pygame as pg
import math
import utils

# how I think this will work. sends out lines from a point and if it hits an line
# that is not parralel


class lightSource():
    def __init__(self, source, mType = "static", strength = 300):
        # init some functions
        self.strength = strength
        self.range = self.strength * 2
        self.scanRect = l_scanRange
        self.scanRect.center = source.rect.center
        self.type = mType
        self.source = source
        self.points = []
        self.scanSegments = []
        self.angles = []
        self.intersects = []

    def get_intersection(self, ray, segment):
        ''' Find intersection of RAY & SEGMENT '''
        # RAY in parametric: Point + Direction*T1
        r_px = ray['a']['x']
        r_py = ray['a']['y']
        r_dx = ray['b']['x'] - ray['a']['x']
        r_dy = ray['b']['y'] - ray['a']['y']

        # SEGMENT in parametric: Point + Direction*T2
        s_px = segment['a']['x']
        s_py = segment['a']['y']
        s_dx = segment['b']['x'] - segment['a']['x']
        s_dy = segment['b']['y'] - segment['a']['y']

        # Are they parallel? If so, no intersect
        r_mag = math.sqrt(r_dx*r_dx+r_dy*r_dy)
        s_mag = math.sqrt(s_dx*s_dx+s_dy*s_dy)
        if r_dx/r_mag == s_dx/s_mag and r_dy/r_mag == s_dy/s_mag:
            return None

        # SOLVE FOR T1 & T2
        # r_px+r_dx*T1 = s_px+s_dx*T2 && r_py+r_dy*T1 = s_py+s_dy*T2
        # ==> T1 = (s_px+s_dx*T2-r_px)/r_dx = (s_py+s_dy*T2-r_py)/r_dy
        # ==> s_px*r_dy + s_dx*T2*r_dy - r_px*r_dy = s_py*r_dx + s_dy*T2*r_dx - r_py*r_dx
        # ==> T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)

        try:
            T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
        except ZeroDivisionError:
            T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx-0.01)

        try:
            T1 = (s_px+s_dx*T2-r_px)/r_dx
        except ZeroDivisionError:
            T1 = (s_px+s_dx*T2-r_px)/(r_dx-0.01)

        # Must be within parametic whatevers for RAY/SEGMENT
        if T1 < 0: return None
        if T2 < 0 or T2>1: return None

        # Return the POINT OF INTERSECTION
        return {
                "x": r_px+r_dx*T1,
                "y": r_py+r_dy*T1,
                "param": T1
        }

    def update(self):
        
        # clean points from segments
        self.points = []
       
        for sprite in self.source.gameScene.objects.groupAll.sprites():
            if self.scanRect.contains(sprite.rect):
                for segment in sprite.segments:
                    if segment not in self.scanSegments:
                        self.scanSegments.append(segment)
                        self.points.append((segment['a'], segment['b']))
        
        #for segment in self.scanSegments:
            #self.points.append((segment[0]['a'], segment['b']))
        
        self.points = utils.cleanDuplicates(self.points)

        # calculate angles and before and past the point
        self.angles = []
        for point in self.points:
            angle = math.atan2(point[0]['y']- self.source.rect.centery, point[0]["x"]-self.source.rect.centerx)
            point[0]["angle"] = angle
            self.angles.append(angle-0.00001)
            self.angles.append(angle)
            self.angles.append(angle+0.00001)

        # ray calculations
        self.intersects = []
        for angle in self.angles:
            # chane in y and x based off angle - diagram to explain required
            del_x = math.cos(angle)
            del_y = math.sin(angle)
        
            # ray from center to source
            ray = {
                "a": {"x": self.source.rect.centerx, "y": self.source.rect.centery},
                "b" : {"x":self.source.rect.centerx + del_x, "y": self.source.rect.centery + del_y}
            }

            # calculate closest intersection
            closestIntersect = None
            for segment in self.scanSegments:
                intersect = self.get_intersection(ray, segment)
                if not intersect: continue
                if not closestIntersect or intersect["param"] < closestIntersect["param"]:
                    closestIntersect = intersect
                
            # Intersect angle
            if not closestIntersect: continue
            closestIntersect["angle"] = angle

            # Add to list of intersects
            self.intersects.append(closestIntersect)

        # Sort intersects by angle
        self.intersects = sorted(self.intersects, key=lambda k: k['angle'])
        return self.intersects
