# Spinning 3D Cube 
# By Dennis Huang, 3rd Year MSE Student at Simon Fraser University
# Date: Nov 19, 2023
import simplegui, math, numeric

WIDTH = 500
HEIGHT = 500

# Vertex Properties
vertexRadius = 5
vertexLineWidth = 10
vertexLineColour = "Red"
running = False

# Edge Properties
edgeLineWidth = 5
edgeLineColour = "Black"

yaw = math.radians(0)
pitch = math.radians(0)
roll = math.radians(0)

speed = 0.02
scale = 150
origin = (WIDTH/2, HEIGHT/2)

cube = [(-1,-1,-1),
      (1,-1,-1),
      (1,1,-1),
      (-1,1,-1),
           
      (-1,-1,1),
      (1,-1,1),
      (1,1,1),
      (-1,1,1)]
      
edge = [(cube[0], cube[1]),
      (cube[1], cube[2]),
      (cube[2], cube[3]),
      (cube[3], cube[0]), 
      
      (cube[4], cube[5]), 
      (cube[5], cube[6]), 
      (cube[6], cube[7]), 
      (cube[7], cube[4]),     
      
      (cube[0], cube[4]), 
      (cube[1], cube[5]),
      (cube[2], cube[6]), 
      (cube[3], cube[7])]
      
def rotateAbout(point, a, b, c):

  R = numeric.Matrix([[math.cos(a)*math.cos(b), 
                      math.cos(a)*math.sin(b)*math.sin(c)-math.sin(a)*math.cos(c), 
                      math.cos(a)*math.sin(b)*math.cos(c)+math.sin(a)*math.sin(c)],
                     [math.sin(a)*math.cos(b),
                      math.sin(a)*math.sin(b)*math.sin(c)+math.cos(a)*math.cos(c),
                      math.sin(a)*math.sin(b)*math.cos(c)-math.cos(a)*math.sin(c)],
                     [-1*math.sin(b),
                      math.cos(b)*math.sin(c), 
                      math.cos(b)*math.cos(c)]])
  v = numeric.Matrix([[point[0]], 
                      [point[1]], 
                      [point[2]]])
  Q = R @ v
  return Q[0, 0], Q[1, 0], Q[2, 0]
  
def project(point, scale, origin):
  
  P = numeric.Matrix([[1, 0, 0], 
                      [0, 1, 0], 
                      [0, 0, 0]])
  v = numeric.Matrix([[point[0]], 
                      [point[1]], 
                      [point[2]]])
  Q = P @ v                        
  return (Q[0, 0] * scale + origin[0], Q[1, 0] * scale + origin[1])      

def drawHandler(canvas):
  global cube, edge, focalLength, scale, yaw, pitch, roll, running, speed
  
  if yaw >= math.radians(360):
      yaw = math.radians(0) 
  if pitch >= math.radians(360):
      pitch = math.radians(0) 
  if roll >= math.radians(360):
      roll = math.radians(0)       
      
  if running == True:    
      yaw += speed 
      pitch += speed
      roll += speed
      
      
  for line in edge:
      rotatedEdge1 = rotateAbout(line[0], yaw, pitch, roll)
      rotatedEdge2 = rotateAbout(line[1], yaw, pitch, roll)
      
      projectedEdge1 = project(rotatedEdge1, scale, origin)
      projectedEdge2 = project(rotatedEdge2, scale, origin)
      
      canvas.draw_line(projectedEdge1, 
                       projectedEdge2,
                       edgeLineWidth, 
                       edgeLineColour)    

  for point in cube:
      rotatedPoint = rotateAbout(point, yaw, pitch, roll)
      projectedPoint = project(rotatedPoint, scale, origin) 

      canvas.draw_circle(projectedPoint,
                         vertexRadius,
                         vertexLineWidth,
                         vertexLineColour)

def start(key):
  global running
  if key == simplegui.KEY_MAP['space']:
      running = True
      
def stop(key):
  global running
  if key == simplegui.KEY_MAP['space']:
      running = False

frame = simplegui.create_frame("Hold Space To Run!", 500, 500)
frame.set_draw_handler(drawHandler)
frame.set_canvas_background("White")

frame.set_keydown_handler(start)
frame.set_keyup_handler(stop)

frame.start()
