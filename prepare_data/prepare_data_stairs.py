import os
from sklearn.model_selection import train_test_split
import numpy as np
import shutil

def read_files_xml_img(dataset,imgExt='jpg'):
    labelExt = 'xml'
    # list objects
    currentDir = os.path.join(os.getcwd(),dataset)
    # loop throught all items
    labels = []
    count =  0
    images = list_files(currentDir,fileExt=imgExt)
    for files in list_files(currentDir,fileExt=labelExt):
        # break th name
        label_name = files.replace('.{}'.format(labelExt),'')
        # check consisterncy
        if '{}.{}'.format(label_name, imgExt) in images:
            labels.append(label_name)
            count=+ 1
    
    count = len(list_files(currentDir,fileExt=labelExt)) - count

    print(count,'items were dropped')
    train_val(labels, currentDir)




def clean_dir(path, sub_fold, train_test_fold):
    for train_test in train_test_fold:
        folder = os.path.join(path, '../', sub_fold, train_test)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def train_val_post(labels,row_path):
    X_train, X_test, _, _ = train_test_split(labels, labels, test_size=0.33, random_state=42)
    clean_dir(row_path,'images',['train', 'val'])
    clean_dir(row_path,'labels',['train', 'val'])
    copy_files(X_train, row_path,'train', 'xml', 'jpg',nbOfStart=1)
    copy_files(X_test, row_path, 'val', 'xml', 'jpg',nbOfStart=1)

def train_val(labels,row_path):
    X_train, X_test, _, _ = train_test_split(labels, labels, test_size=0.33, random_state=42)
    copy_files(X_train, row_path,'train', 'xml', 'jpg',nbOfStart=1)
    copy_files(X_test, row_path, 'val', 'xml', 'jpg',nbOfStart=1)

def list_files(path,fileExt=''):
    # get a list of the file of a specific extension
    onlyfiles = [f for f in os.listdir(path) if f[len(f)-len(fileExt):] == fileExt]
    #
    return onlyfiles
    
def copy_files(labels,path,train_test_fold, label_ext,img_ext, nbOfStart=90000):
    # create files
    newName = np.arange(nbOfStart,nbOfStart+len(labels))
    # loop thorught files
    for count, fileName in enumerate(labels):
        # copy labels and Imgs
        for idx, exts in enumerate([label_ext, img_ext]):
            src_path = os.path.join(path,'{}.{}'.format(fileName, exts))
            dst_renamed = os.path.join(path, '../', train_test_fold, '{}.{}'.format(str(newName[count]),exts))
            shutil.copyfile(src_path, dst_renamed)

read_files_xml_img(dataset='row_data/stairs/row')