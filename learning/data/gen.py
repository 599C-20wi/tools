import csv
import os
import shutil
import sys

""" A utility file for generating training and validation data sets. """

LEGEND_PATH = "../raw-data/legend.csv"
IMAGES_PATH = "../raw-data/images"

def safe_create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def gen_data_set(expr):
    expr_paths = []
    other_paths = []

    # Partition the images paths.
    with open(LEGEND_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=str(','))
        next(csv_reader) # Skip first line
        for row in csv_reader:
            if row[2] == expr:
                expr_paths.append(row[1])
            else:
                other_paths.append(row[1])

    # Perform train and validation image splits (90 percent train, 10 percent validation)
    train_expr_imgs = expr_paths[:9*len(expr_paths)/10]
    validation_expr_imgs = expr_paths[9*len(expr_paths)/10:]

    train_other_imgs = other_paths[:9*len(other_paths)/10]
    validation_other_imgs = other_paths[9*len(other_paths)/10:]

    # Create subdirectories for training and validation data.
    path = os.getcwd()
    path = os.path.join(path, expr)

    train_dir = os.path.join(path, 'train')
    safe_create_dir(train_dir)

    validation_dir = os.path.join(path, 'validation')
    safe_create_dir(validation_dir)

    train_expr_dir = os.path.join(train_dir, expr)
    if not os.path.exists(train_expr_dir):
        os.makedirs(train_expr_dir)

        for img_name in train_expr_imgs:
            src_path = os.path.join(IMAGES_PATH, img_name)
            dst_path = os.path.join(train_expr_dir, img_name)
            shutil.copyfile(src_path, dst_path)

    train_other_dir = os.path.join(train_dir, 'other')
    if not os.path.exists(train_other_dir):
        os.makedirs(train_other_dir)

        for img_name in train_other_imgs:
            src_path = os.path.join(IMAGES_PATH, img_name)
            dst_path = os.path.join(train_other_dir, img_name)
            shutil.copyfile(src_path, dst_path)
    
    validation_expr_dir = os.path.join(validation_dir, expr)
    if not os.path.exists(validation_expr_dir):
        os.makedirs(validation_expr_dir)

        for img_name in validation_expr_imgs:
            src_path = os.path.join(IMAGES_PATH, img_name)
            dst_path = os.path.join(validation_expr_dir, img_name)
            shutil.copyfile(src_path, dst_path)

    validation_other_dir = os.path.join(validation_dir, 'other')
    if not os.path.exists(validation_other_dir):
        os.makedirs(validation_other_dir)

        for img_name in validation_other_imgs:
            src_path = os.path.join(IMAGES_PATH, img_name)
            dst_path = os.path.join(validation_other_dir, img_name)
            shutil.copyfile(src_path, dst_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python gen.py <facial expression>")
        sys.exit(1) 
    expr = sys.argv[1]
    gen_data_set(expr)
