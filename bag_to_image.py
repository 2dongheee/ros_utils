import cv2
import glob
import rosbag
from cv_bridge import CvBridge
from tqdm import tqdm

def cvtBag2Img(date_folder, output_folder):
    bridge = CvBridge()
    bag_files = glob.glob(date_folder+'*.bag')
    
    for i, bag_file in enumerate(bag_files):
        bag = rosbag.Bag(bag_file)
        
        print("Bag file : %s"%(bag_file.split('/')[-1]))

        for idx, topic_name in enumerate(bag.get_type_and_topic_info().topics):
            if 'camera' not in topic_name: continue
            frame_count,file_count = 0, 0
            read_cam_topic = bag.read_messages(topics=[topic_name])
           
            for topic, msg, t in tqdm(read_cam_topic, desc=topic_name):
                frame_count+=1
                if frame_count % 10 == 0:
                    filename=('%d_cam%d'%(i, idx)+'_'+str(file_count).zfill(6))
                    file_count+=1
                    
                    if 'raw' in topic_name:
                        img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
                    else:
                        img = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="passthrough")
                    
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    # undistort_img = undistort(img)
                    # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)	
                    cv2.imwrite(output_folder + filename + '.png', img)
    
        bag.close()
        
if __name__ == "__main__":
    bags_path = '/media/dong/dong_ssd/epitone/eptione_bag/calib/'
    output_path = '/media/dong/Store2/Epitone/calib/images/'
    
    cvtBag2Img(bags_path, output_path)