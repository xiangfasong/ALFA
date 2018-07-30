import pickle
import datetime
import argparse
import sys
import numpy as np
import json
import pprint
import os

from map_computation import Computation_mAP, read_imagenames, read_annotations
from ALFA import ALFA


def read_detectors_full_detections(detections_filenames):

    """
    Method to read detections into dict

    ----------
    detections_filenames : list
        Pickles that store detections for mAP computation
        File contains a list of detections for one detector or fusion result, kept in format:

        (image filename: '00000.png', bounding boxes: [[23, 45, 180, 790], ..., [100, 39, 705, 98]],
            labels: [0, ..., 19], class_scores: [[0.0, 0.01, ...., 0.98], ..., [0.9, 0.0, ..., 0.001]])


    Returns
    -------
    detectors_full_detections: dict
        Dictionary, containing detections for n detectors:

        '1': [
        (image filename: '00000.png', bounding boxes: [[23, 45, 180, 790], ..., [100, 39, 705, 98]],
            labels: [0, ..., 19], class_scores: [[0.0, 0.01, ...., 0.98], ..., [0.9, 0.0, ..., 0.001]]),
        ...,
        (image filename: '00500.png', bounding boxes: [[32, 54, 81, 97], ..., [1, 93, 507, 890]],
            labels: [0, ..., 19], class_scores: [[0.0, 0.001, ...., 0.97], ..., [0.95, 0.00001, ..., 0.0001]])
        ],
        ...,
        'n': [
        (image filename: '00000.png', bounding boxes: [[33, 55, 180, 800], ..., [110, 49, 715, 108]],
            labels: [0, ..., 19], class_scores: [[0.01, 0.01, ...., 0.98], ..., [0.8, 0.0002, ..., 0.001]]),
        ...,
        (image filename: '00500.png', bounding boxes: [[13, 35, 170, 780], ..., [90, 29, 695, 88]],
            labels: [0, ..., 19], class_scores: [[0.08, 0.2, ...., 0.06], ..., [0.0, 0.0, ..., 1.0]])
        ]
    """

    detectors_full_detections = {}
    for i in range(len(detections_filenames)):
        with open(detections_filenames[i], 'rb') as f:
            if sys.version_info[0] == 3:
                detectors_full_detections[i] = pickle.load(f, encoding='latin1')
            else:
                detectors_full_detections[i] = pickle.load(f)

    if len(list(detectors_full_detections.keys())) == 0:
        print('Detections even for one detector were not provided!')
        exit(1)
    else:
        check_size_sim = True
        for i in range(1, len(list(detectors_full_detections.keys()))):
            if len(detectors_full_detections[i]) != len(detectors_full_detections[0]):
                check_size_sim = False
                break
        if not check_size_sim:
            print('All detections files should provide detections for the same amount of images with same names!')
            exit(1)
    return detectors_full_detections


def validate_ALFA(dataset_name, dataset_dir, imagenames, annotations, detectors_full_detections, alfa_parameters_dict,
                  map_iou_threshold, weighted_map=False, full_imagenames=None):
    """
    Validate ALFA algorithm

    ----------
    dataset_name : string
        Dataset name, e.g. 'PASCAL VOC'

    dataset_dir : string
        Path to images dir, e.g.'.../PASCAL VOC/VOC2007 test/VOC2007/'

    imagenames : list
            List contains all or a part of dataset filenames

    annotations : dict
        Dict of annotations

    detectors_full_detections: dict
        Dict of full detections for diferent detectors

    alfa_parameters_dict : dict
        Contains list of one element for each parameter:

        tau in the paper, between [0.0, 1.0]
        gamma in the paper, between [0.0, 1.0]
        bounding_box_fusion_method ["MIN", "MAX", "MOST CONFIDENT", "AVERAGE", "WEIGHTED AVERAGE",
        "WEIGHTED AVERAGE FINAL LABEL"]
        class_scores_fusion_method ["MOST CONFIDENT", "AVERAGE", "MULTIPLY"]
        add_empty_detections, if true - low confidence class scores tuple will be added to cluster for each detector, that missed
        epsilon in the paper, between [0.0, 1.0]
        same_labels_only, if true only detections with same class label will be added into same cluster
        confidence_style means how to compute score for object proposal ["LABEL", "ONE MINUS NO OBJECT"]
        use_BC, if true - Bhattacharyya and Jaccard coefficient will be used to compute detections similarity score
        max_1_box_per_detector, if true - only one detection form detector could be added to cluster

    map_iou_threshold : float
        Jaccard coefficient value to compute mAP, between [0, 1]

    weighted_map : boolean
            True - compute weighted mAP by part class samples count to all class samples count in dataset
            False - compute ordinary mAP

    full_imagenames: list
            List contains all of dataset filenames, if compute
            weighted map on a part of dataset
    """

    alfa = ALFA()
    map_computation = Computation_mAP(None)

    total_time = 0
    time_count = 0
    alfa_full_detections = []

    print('Running ALFA on dataset...')

    a = datetime.datetime.now()
    for j in range(len(detectors_full_detections[0])):
        imagename = detectors_full_detections[0][j][0]

        bounding_boxes = {}
        labels = {}
        class_scores = {}

        for key in detectors_full_detections.keys():
            if len(detectors_full_detections[key][j][1]) > 0:
                bb = detectors_full_detections[key][j][1]
                l = np.array(detectors_full_detections[key][j][2])
                cl_sc = np.array(detectors_full_detections[key][j][3])
                scores = np.array([cl_sc[i, 1:][l[i]] for i in range(len(l))])
                indices = np.where(scores > alfa_parameters_dict['select_threshold'])[0]
                if len(indices) > 0:
                    bounding_boxes[key] = bb[indices]
                    labels[key] = l[indices]
                    class_scores[key] = cl_sc[indices]

        if bounding_boxes != {}:
            bounding_boxes, labels, class_scores = alfa.ALFA_result(bounding_boxes, class_scores,
                                                                    alfa_parameters_dict['tau'][0],
                                                                    alfa_parameters_dict['gamma'][0],
                                                                    alfa_parameters_dict['bounding_box_fusion_method'][0],
                                                                    alfa_parameters_dict['class_scores_fusion_method'][0],
                                                                    alfa_parameters_dict['add_empty_detections'][0],
                                                                    alfa_parameters_dict['epsilon'][0],
                                                                    alfa_parameters_dict['same_labels_only'][0],
                                                                    alfa_parameters_dict['confidence_style'][0],
                                                                    alfa_parameters_dict['use_BC'][0],
                                                                    alfa_parameters_dict['max_1_box_per_detector'][0],
                                                                    alfa_parameters_dict['single'])
            time_count += 1
        else:
            bounding_boxes = np.array([])
            labels = np.array([])
            class_scores = np.array([])

        alfa_full_detections.append((imagename, bounding_boxes, labels, class_scores))

    b = datetime.datetime.now()
    total_time += (b - a).seconds

    aps, mAP, pr_curves = map_computation.compute_map(dataset_name, dataset_dir, imagenames,
                                            annotations, alfa_full_detections, map_iou_threshold,
                                                      weighted_map, full_imagenames)

    print('Average ensemble time: ', float(total_time) / float(time_count))

    return aps, mAP, pr_curves


def parse_alfa_parameters_json(alfa_parameters_json):
    with open(alfa_parameters_json, 'r') as f:
        alfa_parameters_dict = json.load(f)
    return alfa_parameters_dict


def check_flag(value):
    if value in ['True', 'False']:
        if value == True:
            return True
        else:
            return False
    else:
        raise argparse.ArgumentTypeError('%s is an invalid flag value, use \"True\" or \"False\"!' % value)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', type=str, help='Only \"PASCAL VOC\" is supported, default=\"PASCAL VOC\"',
                        default='PASCAL VOC')
    parser.add_argument('--dataset_dir', required=True, type=str,
                        help='e.g.=\"(Your path)/PASCAL VOC/VOC2007 test/VOC2007\"')
    parser.add_argument('--imagenames_filename', required=True, type=str,
        help='File where images filenames to compute mAP are stored, e.g.=\"./PASCAL_VOC_files/imagesnames_2007_test.txt\"')
    parser.add_argument('--pickled_annots_filename', type=str,
        help='Pickle where annotations to compute mAP are stored, e.g.=\"./PASCAL_VOC_files/annots_2007_test.pkl\"')
    parser.add_argument('--alfa_parameters_json', required=True, type=str,
                        help='File from directory \"./Cross_validation_ALFA_parameters\", that contains parameters:'
                             'tau in the paper, between [0.0, 1.0], '
                             'gamma in the paper, between [0.0, 1.0],'
                             'bounding_box_fusion_method [\"MIN\", \"MAX\", \"MOST CONFIDENT\", \"AVERAGE\", '
                             'class_scores_fusion_method [\"MOST CONFIDENT\", \"AVERAGE\", \"MULTIPLY\", '
                             'add_empty_detections, if true - low confidence class scores tuple will be added to cluster '
                             'for each detector, '
                             'epsilon in the paper, between [0.0, 1.0], '
                             'same_labels_only, if true - only detections with same class label will be added into same '
                             'cluster, '
                             'confidence_style_list ["LABEL", "ONE MINUS NO OBJECT"], '
                             'use_BC, if true - Bhattacharyya and Jaccard coefficient will be used to compute detections '
                             'max_1_box_per_detector, if true - only one detection form detector could be added to cluster, '
                             'single, if true computes ALFA prediction for mAP-s computation refered in paper, '
                             'select_threshold is the confidence threshold for detections, '
                             'detections_filenames list of pickles that store detections for mAP computation')
    parser.add_argument('--map_iou_threshold', type=float,
                        help='Jaccard coefficient value to compute mAP, default=0.5', default=0.5)
    return parser.parse_args(argv)


def main(args):

    alfa_parameters_dict = parse_alfa_parameters_json(args.alfa_parameters_json)
    pprint.pprint(alfa_parameters_dict)

    detectors_full_detections = read_detectors_full_detections(alfa_parameters_dict['detections_filenames'])

    annotations_dir = os.path.join(args.dataset_dir, 'Annotations/')
    images_dir = os.path.join(args.dataset_dir, 'JPEGImages/')

    imagenames = read_imagenames(args.imagenames_filename, images_dir)
    annotations = read_annotations(args.pickled_annots_filename, annotations_dir, imagenames, args.dataset_name)

    validate_ALFA(args.dataset_name, args.dataset_dir, imagenames,
                    annotations, detectors_full_detections, alfa_parameters_dict, args.map_iou_threshold)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
