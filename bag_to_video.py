import cv2
import rosbag
import numpy as np
from tqdm import tqdm
import glob

def callback(msg): 
    np_arr = np.fromstring(msg.data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def createBag2video(bag_files_path, output_path):
    fcc = cv2.VideoWriter_fourcc('M','J','P','G')
    bag_files = glob.glob(bag_files_path+'*.bag')

    for i, bag_file in enumerate(bag_files): 
        bag = rosbag.Bag(bag_file)
        
        print("Bag file : %s"%(bag_file.split('/')[-1]))

        for idx, topic_name in enumerate(bag.get_type_and_topic_info().topics):
            if 'camera' not in topic_name: continue
            frame_count = 0
            
            out = cv2.VideoWriter(output_path+'%d_cam%d_%s.mp4'%(i, idx, bag_file.split('.')[-1]), fcc, 30, (1920, 1080))
            read_cam_topic = bag.read_messages(topics=[topic_name])
            
            for topic, msg, t in tqdm(read_cam_topic, desc=topic_name):
                img = callback(msg)
                frame_count+=1
                
                # Correction of Distortion
                #img = undistort(img)
                out.write(img)
                
            out.release()
        bag.close()
        exit(0)
    
if __name__=="__main__":
    bag_files_path = '/media/dong/dong_ssd/epitone/'
    output_path = '/media/dong/Store2/Epitone/'
   
    createBag2video(bag_files_path, output_path)

   

		

