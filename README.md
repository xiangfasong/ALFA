# ALFA: Agglomerative Late Fusion Algorithm for Object Detection

By Evgenii Razinkov, Iuliia Saveleva, Jiří Matas

The paper "ALFA: Agglomerative Late Fusion Algorithm for Object Detection" is accepted 
to ICPR 2018, the link and description to the method will be added here as soon as 
the paper become available.

## Evaluate on Pascal VOC 2007

Results on PASCAL VOC 2007 are not reproducible due to randomness of a cross-validation procedure.
You can evaluate algorithms on PASCAL VOC 2007 and get results, that would be close to the results in paper:

### ALFA

* get ALFA detections running the following command:
```bash
python ./validate_ALFA.py \
--dataset_dir="path/to/VOC2007 test/VOC2007" \
--imagenames_filename="./PASCAL_VOC_files/imagenames_2007_test.txt" \
--pickled_annots_filename="./PASCAL_VOC_files/annots_2007_test.pkl" \
--alfa_parameters_json="./Cross_validation_ALFA_parameters/SSD_DeNet_ALFA_0.05_single_cross_validation_parameters_2007.json"
```

| Algorithm | Detectors  | Single detections | Parameters |
|--------|:---------:|:------:| :------:|
| Fast ALFA | SSD + DeNet | Yes  | SSD_DeNet_ALFA_0.05_single_cross_validation_parameters_2007.json |
| ALFA | SSD + DeNet | Yes |  SSD_DeNet_ALFA_0.015_single_cross_validation_parameters_2007.json |
| Fast ALFA | SSD + DeNet + Faster R-CNN | Yes | SSD_DeNet_Faster_R-CNN_ALFA_0.05_single_cross_validation_parameters_2007.json |
| ALFA | SSD + DeNet + Faster R-CNN | Yes | SSD_DeNet_Faster_R-CNN_ALFA_0.015_single_cross_validation_parameters_2007.json |
| Fast ALFA | SSD + DeNet | No | SSD_DeNet_ALFA_0.05_multiple_cross_validation_parameters_2007.json |
| ALFA | SSD + DeNet | No |  SSD_DeNet_ALFA_0.015_multiple_cross_validation_parameters_2007.json |
| Fast ALFA | SSD + DeNet + Faster R-CNN | No | SSD_DeNet_Faster_R-CNN_ALFA_0.05_multiple_cross_validation_parameters_2007.json |
| ALFA | SSD + DeNet + Faster R-CNN | No | SSD_DeNet_Faster_R-CNN_ALFA_0.015_multiple_cross_validation_parameters_2007.json |


### DBF

### NMS

## Evaluate on Pascal VOC 2012

You can reproduce the results of algorithms on PASCAL VOC 2012.

### ALFA
* get ALFA detections running the following command:
```bash
python ./validate_ALFA.py \
--dataset_dir="path/to/VOC2012 test/VOC2012" \
--imagenames_filename="./PASCAL_VOC_files/imagenames_2012_test.txt" \
--pickled_annots_filename="./PASCAL_VOC_files/annots_2012_test.pkl" \
--alfa_parameters_json="./Cross_validation_ALFA_parameters/SSD_DeNet_ALFA_0.05_single_cross_validation_parameters_2012.json" \
--output_filename="path/to/output_filename.pkl"
```

| Algorithm | Detectors  | Single detections | Parameters |
|--------|:---------:|:------:| :------:|
| Fast ALFA | SSD + DeNet | Yes  | SSD_DeNet_ALFA_0.05_single_cross_validation_parameters_2012.json |
| ALFA | SSD + DeNet | Yes |  SSD_DeNet_ALFA_0.015_single_cross_validation_parameters_2012.json |
| Fast ALFA | SSD + DeNet + Faster R-CNN | Yes | SSD_DeNet_Faster_R-CNN_ALFA_0.05_single_cross_validation_parameters_2012.json |
| ALFA | SSD + DeNet + Faster R-CNN | Yes | SSD_DeNet_Faster_R-CNN_ALFA_0.015_single_cross_validation_parameters_2012.json |
| Fast ALFA | SSD + DeNet | No | SSD_DeNet_ALFA_0.05_multiple_cross_validation_parameters_2012.json |
| ALFA | SSD + DeNet | No |  SSD_DeNet_ALFA_0.015_multiple_cross_validation_parameters_2012.json |
| Fast ALFA | SSD + DeNet + Faster R-CNN | No | SSD_DeNet_Faster_R-CNN_ALFA_0.05_multiple_cross_validation_parameters_2012.json |
| ALFA | SSD + DeNet + Faster R-CNN | No | SSD_DeNet_Faster_R-CNN_ALFA_0.015_multiple_cross_validation_parameters_2012.json |

* convert "path/to/output_filename.pkl" to PASCAL VOC 2012 submission format by running:
```bash
python ./detections_to_PASCAL_VOC_2012_submission.py \
--detections_filename="path/to/output_filename.pkl"
--submission_folder="path/to/submission_folder"
```

* archive "path/to/submission_folder" as .tar.gz

* upload "path/to/submission_folder.tar.gz" to PASCAL VOC 2012 evaluation server

### DBF

### NMS