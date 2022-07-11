import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import shutil

dirs = ['train', 'val']
classes = ['downstair','upstair']

def getImagesInDir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def move_files(file_Ext='jpg', sub_fold='images'):
    for train_val in dirs:
        train_val_src = train_val
        if file_Ext == 'txt':
            train_val_src = os.path.join(train_val, 'yolo')
            sub_fold = 'labels'
        src_path = os.path.join(cwd,train_val_src)
        dst_path = os.path.join(cwd,'train_data',sub_fold,train_val)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        # copy files
        for fileName in list_files(src_path,fileExt=file_Ext):
            src_file = os.path.join(src_path,fileName)
            dst_file = os.path.join(dst_path,fileName)
            shutil.copyfile(src_file, dst_file)


def convert_annotation(dir_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes:#or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def list_files(path,fileExt=''):
    # get a list of the file of a specific extension
    onlyfiles = [f for f in os.listdir(path) if f[len(f)-len(fileExt):] == fileExt]
    #
    return onlyfiles
cwd = getcwd()

for dir_path in dirs:
    full_dir_path = cwd + '/' + dir_path
    output_path = full_dir_path +'/yolo/'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image_paths = getImagesInDir(full_dir_path)
    list_file = open(full_dir_path + '.txt', 'w')

    for image_path in image_paths:
        list_file.write(image_path + '\n')
        convert_annotation(full_dir_path, output_path, image_path)
    list_file.close()

    print("Finished processing: " + dir_path)
move_files(file_Ext='jpg')
move_files(file_Ext='txt')
print('Finished train_data file')