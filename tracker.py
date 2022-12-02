import socket
import json
import sys
import pyrealsense2 as rs

pipe = rs.pipeline()

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

try:
    IPs = sys.argv[1:]
except IndexError:
    IPs = ["127.0.0.1"]
print("Realsense T265 sending to" , IPs)
TCP_PORT = 54321
BUFFER_SIZE = 1024

starting_height = 1 # starting height in meters
pos_scale = 100
rot_scale = 1
threshold = 0.0005
  
for IP in IPs:  
    MESSAGE = '{"MHTrack": [{"Type": "CameraSubject"}, {"FieldOfView": "true","AspectRatio": "true","FocalLength": "true","ProjectionMode": "false"}]}'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((IP, TCP_PORT))
    s.send(MESSAGE.encode('utf-8'))
    s.close() 


pipe.start(cfg)

frames = pipe.wait_for_frames()

    # Fetch pose frame
pose = frames.get_pose_frame()
if pose:
    data = pose.get_pose_data()
    zeroX = data.translation.x
    zeroY = data.translation.y 
    zeroZ = data.translation.z


try:
    while True:

        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()

        # Fetch pose frame
        pose = frames.get_pose_frame()
        if pose:
            # Print some of the pose data to the terminal
            data = pose.get_pose_data()
      #      if data.translation.z
         
            data.translation.y += starting_height
            print ("x : ", - data.translation.z, " y: ", data.translation.x , "z: " , data.translation.y, " and delta is ", delta)
            MESSAGE = '{{"MHTrack": [{{"Type":"CameraAnimation"}},{{"Location":[{},{},{}],"Rotation":[{:.4f},{:.4f},{:.4f},{:.4f}],"Scale":[1,1,1]}}]}}'.format((pos_scale*(-data.translation.z-zeroZ)),(pos_scale*(data.translation.x-zeroX)),(pos_scale*(data.translation.y-zeroY)), rot_scale*data.rotation.z, rot_scale*-data.rotation.x, rot_scale*-data.rotation.y,rot_scale*data.rotation.w)
          
            for IP in IPs:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((IP, TCP_PORT))
                s.send(MESSAGE.encode('utf-8'))
                s.close()
    
finally:
    pipe.stop()


    