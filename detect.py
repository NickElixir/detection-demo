import os.path
import argparse
import time
import tensorflow as tf
import numpy as np
from models.yolo_v3 import yolo_v3
from utils.utils import process_image, get_anchors, get_classes, convert_box_coordinates, non_max_suppression, draw_boxes

def detect(path_to_input_image, save_as = None,
    path_to_trained_model = os.path.dirname(os.path.abspath(__file__)) + "/model_weights/coco_pretrained_weights.ckpt",
    tensorboard_save_path = os.path.dirname(os.path.abspath(__file__)) + '/tensorboard/tensorboard_detect/',
    class_path = os.path.dirname(os.path.abspath(__file__)) + '/utils/coco_classes.txt',
    anchors_path = os.path.dirname(os.path.abspath(__file__)) + '/utils/anchors.txt',
    input_height = 416,
    input_width = 416):

    h = input_height
    w = input_width
    anchors = get_anchors(anchors_path)
    classes = get_classes(class_path)
    save_as = save_as
    if save_as is None:
        filename_w_ext = os.path.basename(path_to_input_image)
        filename, file_extension = os.path.splitext(filename_w_ext)
        save_as = filename + '_yolo_v3' + file_extension

    image, original_im = process_image(path_to_input_image, h, w)

    tf.reset_default_graph()

    # build graph
    with tf.variable_scope('x_input'):
        X = tf.placeholder(dtype=tf.float32, shape=[None, h, w, 3])
    
    yolo_outputs = yolo_v3(inputs=X, num_classes=len(classes), anchors=anchors, h=h, w=w, training=False) # output

    with tf.variable_scope('obj_detections'):
        raw_outputs = tf.concat(yolo_outputs, axis=1)

    # pass image through model
    with tf.Session() as sess:

        writer = tf.summary.FileWriter(tensorboard_save_path, sess.graph)
        writer.close()

        saver = tf.train.Saver()
        print('restoring model weights...')
        saver.restore(sess, save_path = path_to_trained_model)
        print('feeding image found at filepath: ', path_to_input_image)
        start = time.time()
        ro = sess.run(raw_outputs, feed_dict={X:[np.array(image, dtype=np.float32)]})
        end = time.time()
        total_time = end-start
        print("total inference time was: "+ str(round(total_time,2)) + " seconds (that's " + str(round(60.0/total_time,2)) + " fps!)")
    
    # convert box coordinates, apply nms, and draw boxes
    boxes = convert_box_coordinates(ro)
    filtered_boxes = non_max_suppression(boxes, confidence_threshold = 0.5,iou_threshold = 0.4)
    draw_boxes(save_as, class_path, filtered_boxes, original_im, image)
    
    print('image with detections saved as: ', save_as)

if __name__ == "__main__":
    print(tf.__version__)
    detect('/Users/NikolaiLucenko/Documents/Python/DLS/detection-demo/yolo_v3/tensorflow_yolo_v3_original/example.jpg')