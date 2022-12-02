import os
import json
import argparse
import funcy
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
parser.add_argument('annotations', metavar='coco_annotations', type=str,
                    help='Path to COCO annotations file.')
parser.add_argument('--train_ratio', type=float, dest='ratio_train', help='set train dataset ratio')
parser.add_argument('--valid_ratio', type=float,  dest='ratio_valid',help='set valid dataset ratio')
parser.add_argument('--test_ratio', type=float,  dest='ratio_test',help='set test dataset ratio')
parser.add_argument('--trainJson_name', type=str, default='train.json', help='Where to store COCO training annotations')
parser.add_argument('--validJson_name', type=str, default='valild.json', help='Where to store COCO valid annotations')
parser.add_argument('--testJson_name', type=str, default='test.json', help='Where to store COCO test annotations')
parser.add_argument('--annotations', dest='annotations', action='store_true',
                    help='Ignore all images without annotations. Keep only these with at least one annotation')
parser.add_argument('--save_path', type=str, default='.', help='main storing path')
parser.add_argument('--image_path', type=str, default='.', help='images relative path')
parser.add_argument('--os', type=str, default='linux', help='choose your operating system')
parser.add_argument('--no_test', type=bool, default=False, action=argparse.BooleanOptionalAction, help='only split train and validation samples')

args = parser.parse_args()

ratio_train = args.ratio_train
ratio_valid = args.ratio_valid
ratio_test = args.ratio_test


def save_coco(file, info, licenses, images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({ 'info': info, 'licenses': licenses, 'images': images, 
            'annotations': annotations, 'categories': categories}, coco, indent=2, sort_keys=True)

def filter_annotations(annotations, images):
    image_ids = funcy.lmap(lambda i: int(i['id']), images)
    return funcy.lfilter(lambda a: int(a['image_id']) in image_ids, annotations)

def main(args):
    with open(args.annotations, 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)
        info = coco['info']
        licenses = coco['licenses']
        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

        images_with_annotations = funcy.lmap(lambda a: int(a['image_id']), annotations)

        if args.annotations:
            images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)

            
        # x: train, y: valid z: test
        if args.no_test:
            x, y = train_test_split(
            images, test_size=ratio_valid)

        else:
            xy, z = train_test_split(
                images, test_size=ratio_test)

            ratio_remaining = 1 - ratio_valid
            ratio_valid_adjusted = ratio_valid / ratio_remaining


            x, y = train_test_split(
                xy, test_size=ratio_valid_adjusted)
        
        if not os.path.exists(args.save_path):
            os.mkdir(args.save_path)
        
        train_path = os.path.join(args.save_path, 'train')
        train_image_path = os.path.join(train_path, 'images')
        valid_path = os.path.join(args.save_path, 'val')
        valid_image_path = os.path.join(valid_path, 'images')
        test_path = os.path.join(args.save_path, 'test')
        test_image_path = os.path.join(test_path, 'images')

        for pp in [train_path, valid_path, test_path]:
            if not os.path.exists(pp):
                os.mkdir(pp)
            if not os.path.exists(os.path.join(pp, 'images')):
                os.mkdir(os.path.join(pp, 'images'))
        
        copy_cmd = 'cp'
        if args.os == 'window':
            copy_cmd = 'copy'

        for train_image in x:
            fname = train_image['file_name']
            os.system(f'{copy_cmd} "{os.path.join(args.image_path, fname)}" "{os.path.join(train_image_path, fname)}"')
        print(f'Complete {len(x)} train images')
        for valid_image in y:
            fname = valid_image['file_name']
            os.system(f'{copy_cmd} "{os.path.join(args.image_path, fname)}" "{os.path.join(valid_image_path, fname)}"')
        print(f'Complete {len(y)} valid images')

        if not args.no_test:
            for test_image in z:
                fname = test_image['file_name']
                os.system(f'{copy_cmd} "{os.path.join(args.image_path, fname)}" "{os.path.join(test_image_path, fname)}"')
            print(f'Complete {len(z)} test images')

        if not args.no_test:
            print("Saved {} entries in {}, {} in {}, and {} in {}".format(len(x), train_path, len(y), valid_path, len(z), test_path))
        else:
            print("Saved {} entries in {}, and {} in {}".format(len(x), train_path, len(y), valid_path))


if __name__ == "__main__":
    main(args)

