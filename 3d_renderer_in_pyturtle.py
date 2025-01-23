import turtle
import keyboard
import math
from time import sleep

screen = turtle.Screen()
screen.tracer(0)

turtle_ = turtle.Turtle()
turtle_.speed("fastest")
turtle_.hideturtle()

user_points = {"x":0,"y":0,"z":0}
focal_length = 240

yaw = 0
pitch = 0

far = 50000
near = 0.1

def cross_product(v1,v2):
    return (v1[1]*v2[2]-v1[2]*v2[1],v1[2]*v2[0]-v1[0]*v2[2],v1[0]*v2[1]-v1[1]*v2[0])

def sub_v(v1,v2):
    return (v1[0]-v2[0],v1[1]-v2[1],v1[2]-v2[2])

def dot_product(v1,v2):
    return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]

def draw_2d_tri(p1,p2,p3,color,filled:bool):
    turtle_.up()
    turtle_.home()
    if filled:
        turtle_.begin_fill()
    turtle_.color(color)
    turtle_.goto(*p1)
    turtle_.down()
    turtle_.goto(*p2)
    turtle_.goto(*p3)
    turtle_.goto(*p1)
    if filled:
        turtle_.end_fill()

def draw_3d_tri(p1,p2,p3,color,filled:bool):
    centroid = []
    for i in range(3):
        centroid.append(p1[i] + p2[i] + p3[i] / 3)
    dist = math.sqrt(((user_points["x"]-centroid[0])**2) + ((user_points["y"]-centroid[1])**2) + ((user_points["z"]-centroid[2])**2))
    N = cross_product(sub_v(p2,p1),sub_v(p3,p1))
    V = sub_v((user_points["x"],user_points["y"],user_points["z"]),p1)
    D = dot_product(N,V)
    if near < dist < far and D < 0:
        p1 = transform_point(p1)
        p2 = transform_point(p2)
        p3 = transform_point(p3)

        visible_v = []
        clipped_v = []

        for p in (p1,p2,p3):
            if p[2] < near:
                clipped_v.append(p)
            else:
                visible_v.append(p)
        if len(visible_v) == 3:
            draw_2d_tri(project_point(p1),project_point(p2),project_point(p3),color,filled)
        elif len(visible_v) == 2:
            z_clip_A(*clipped_v,*visible_v,color,filled)
        elif len(visible_v) == 1:
            z_clip_B(*clipped_v,*visible_v,color,filled)
        
def z_clip_A(p1,p2,p3,color,filled:bool):
    x1,y1,z1,x2,y2,z2,x3,y3,z3 = (*p1,*p2,*p3)
    z1_ = (z2-1)/(z2-z1)
    x1_ = focal_length*(x2-((x2-x1)*z1_))
    y1_ = focal_length*(y2-((y2-y1)*z1_))
    z2_ = (z3-1)/(z3-z1)
    x2_ = focal_length*(x3-((x3-x1)*z2_))
    y2_ = focal_length*(y3-((y3-y1)*z2_))
    draw_2d_tri((x1_,y1_),project_point((x2,y2,z2)),project_point((x3,y3,z3)),color,filled)
    draw_2d_tri((x1_,y1_),(x2_,y2_),project_point((x3,y3,z3)),color,filled)

def z_clip_B(p1,p2,p3,color,filled:bool):
    x1,y1,z1,x2,y2,z2,x3,y3,z3 = (*p1,*p2,*p3)
    z1_ = (z3-1)/(z3-z1)
    x1_ = focal_length*(x3-((x3-x1)*z1_))
    y1_ = focal_length*(y3-((y3-y1)*z1_))
    z2_ = (z3-1)/(z3-z2)
    x2_ = focal_length*(x3-((x3-x2)*z2_))
    y2_ = focal_length*(y3-((y3-y2)*z2_))
    draw_2d_tri((x1_,y1_),(x2_,y2_),project_point((x3,y3,z3)),color,filled)

def transform_point(p):
    s_height = screen.window_height()
    s_width = screen.window_width()
    
    x,y,z = p
    dx = x - user_points["x"]
    dy = y - user_points["y"]
    dz = z - user_points["z"]
    
    dx_rot = dx * math.cos(yaw) - dz * math.sin(yaw)
    dz_rot = dx * math.sin(yaw) + dz * math.cos(yaw)

    dy_rot = dy * math.cos(pitch) - dz_rot * math.sin(pitch)
    dz_rot = dy * math.sin(pitch) + dz_rot * math.cos(pitch)

    return (dx_rot,dy_rot,dz_rot)

def project_point(p):
    x,y,z = p
    projected_x = x*focal_length / z
    projected_y = y*focal_length / z

    return (projected_x,projected_y)

tri_printed = 0
while True:
    turtle_.clear()
    try:
        if keyboard.is_pressed("w"):
            user_points["x"] += 0.3 * math.sin(yaw)
            user_points["z"] += 0.3 * math.cos(yaw)
        if keyboard.is_pressed("s"):
            user_points["x"] -= 0.3 * math.sin(yaw)
            user_points["z"] -= 0.3 * math.cos(yaw)
        if keyboard.is_pressed("a"):
            user_points["x"] -= 0.3 * math.cos(yaw)
            user_points["z"] += 0.3 * math.sin(yaw)
        if keyboard.is_pressed("d"):
            user_points["x"] += 0.3 * math.cos(yaw)
            user_points["z"] -= 0.3 * math.sin(yaw)
        if keyboard.is_pressed("space"):
            user_points["y"] += 0.3
        if keyboard.is_pressed("shift"):
            user_points["y"] -= 0.3
        if keyboard.is_pressed("up"):
            pitch += 0.003
        if keyboard.is_pressed("down"):
            pitch -= 0.003
        if keyboard.is_pressed("right"):
            yaw += 0.003
        if keyboard.is_pressed("left"):
            yaw -= 0.003
    except Exception:
        pass
    draw_3d_tri((-100,-100,150),(100,-100,150),(100,110,150),"red",True)
    screen.update()
    sleep(0.0001)
