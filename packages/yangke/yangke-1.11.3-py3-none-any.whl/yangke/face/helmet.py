import dlib
import glob
import os


#
# def get_dataset(dataset, args):
#     if dataset.lower() == 'voc':
#         train_dataset = VOCLike(root='D:\VOCdevkit', splits=[(2028, 'trainval')])
#         val_dataset = VOCLike(root='D:\VOCdevkit', splits=[(2028, 'test')])
#         val_metric = VOC07MApMetric(iou_thresh=0.5, class_names=val_dataset.classes)
#     elif dataset.lower() == 'coco':
#         train_dataset = gdata.COCODetection(splits='instances_train2017', use_crowd=False)
#         val_dataset = gdata.COCODetection(splits='instances_val2017', skip_empty=False)
#         val_metric = COCODetectionMetric(
#             val_dataset, args.save_prefix + '_eval', cleanup=True,
#             data_shape=(args.data_shape, args.data_shape))
#     else:
#         raise NotImplementedError('Dataset: {} not implemented.'.format(dataset))
#     if args.num_samples < 0:
#         args.num_samples = len(train_dataset)
#     if args.mixup:
#         from gluoncv.data import MixupDetection
#         train_dataset = MixupDetection(train_dataset)
#     return train_dataset, val_dataset, val_metric
def train_helmet():
    options = dlib.simple_object_detector_training_options()
    options.add_left_right_image_flips = True
    options.C = 5  # 需要优化
    options.num_threads = 1  # CPU核数
    options.be_verbose = True

    train_xml_path = r"D:\Users\pycharm\face\helmet\VOC2028\dlib\test.xml"
    test_xml_path = r"D:\Users\pycharm\face\helmet\VOC2028\dlib\test.xml"

    dlib.train_simple_object_detector(train_xml_path, 'detector.svm', options)

    print("")
    print("Training accuracy:{}".format(
        dlib.test_simple_object_detector(train_xml_path, 'detector.svm')
    ))
    print("Testing accuracy:{}".format(
        dlib.test_simple_object_detector(test_xml_path, 'detector.svm')
    ))

    detector = dlib.simple_object_detector('detector.svm')
    win_det = dlib.image_window()
    win_det.set_image(detector)

    print("showing detections on the images in the faces folder...")
    win = dlib.image_window()
    image_folder = r"D:\Users\pycharm\face\helmet\VOC2028\JPEGImages"
    for f in glob.glob(os.path.join(image_folder, "*.jpg")):
        print('Processing file: {}'.format(f))
        img = dlib.load_rgb_image(f)
        dets = detector(img)
        print("Number of heads detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            print("Detection {}: Left:{} Top:{} Right:{} Bottom:{}".format(
                k, d.left(), d.top(), d.right(), d.bottom()
            ))

            win.clear_overlay()
            win.set_image(img)
            win.add_overlay(dets)
            dlib.hit_enter_to_continue()

    detector.save('helmet_detect_20200413.svm')


train_helmet()
