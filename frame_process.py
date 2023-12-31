from src.human_detection import HumanDetector
import cv2
import numpy as np
import config.config as config
from utils.generate_json import JsonGenerator
from utils.filter_result import ResultFilterer
from utils.visualize import Visualizer
from abnormal.handler import AbnormalHandler


detector_cfg, detector_weight, estimator_weight, estimator_model_cfg, estimator_data_cfg = config.detector_cfg, \
                                config.detector_weight, config.pose_weight, config.pose_model_cfg, config.pose_data_cfg
write_json = config.write_json
filter_criterion = config.filter_criterion

class PoseAnalyzer:
    def __init__(self):
        pass
    def BBoxAnalyer(self, Id, BBox):
        NumObj = len(Id)

        # If Bounding Box is vertical rectangle, ResultVec related position is Ture;
        # If horizontal, ResultVec related position is False;
        ResultVec = np.zeros(NumObj)
        for index, bbox in enumerate(BBox):
            print("ratio:", (bbox[2]-bbox[0])/(bbox[3]-bbox[1]))
            print("bbox:", bbox)
            if (bbox[2]-bbox[0])/(bbox[3]-bbox[1]) > 0.7128:
                ResultVec[index] = True
            else:
                ResultVec[index] = False
        return ResultVec

class FrameProcessor:
    def __init__(self):
        self.HP = HumanDetector(detector_cfg, detector_weight, estimator_weight, estimator_model_cfg, estimator_data_cfg)
        self.write_json = write_json
        if write_json:
            if not config.json_path:
                try:
                    json_path = config.input_src[:-len(config.input_src.split(".")[-1]) - 1] + ".json"
                except:
                    json_path = "result.json"
            else:
                json_path = ""
            self.Json = JsonGenerator(json_path)
        self.filter = ResultFilterer(filter_criterion)
        self.visualizer = Visualizer(self.HP.estimator.kps)
        self.abnormal = AbnormalHandler()
        # self.poseanalyzer = PoseAnalyzer()

    def process(self, frame, cnt=0):
        ids, boxes, kps, kps_scores = self.HP.process(frame, print_time=True)
        # self.HP.visualize(frame)
        ids, boxes, kps, kps_scores = self.filter.filter(ids, boxes, kps, kps_scores, cnt)

        self.abnormal.process(ids, boxes, kps, kps_scores)
        self.abnormal.visualize(frame)
        # alarmVector = self.poseanalyzer.BBoxAnalyer(ids,boxes)
        # if True in alarmVector:
        #     check_alarm = True
        # else:
        #     check_alarm = False
        # self.visualizer.visualize(frame, ids, boxes, kps, kps_scores, check_alarm)
        self.visualizer.visualize(frame, ids, boxes, kps, kps_scores)

        if self.write_json:
            self.Json.update(ids, boxes, kps, kps_scores, cnt)


    def release(self):
        if self.write_json:
            self.Json.release()


if __name__ == '__main__':
    # pose_weight = "/home/hkuit164/Downloads/pytorch_model_samples/mob3/pytorch/3_best_acc.pth"
    # det_cfg = "/home/hkuit164/Downloads/nanodet_weights/coco/pytorch/nanodet-coco.yml"
    # det_weight = "/home/hkuit164/Downloads/nanodet_weights/coco/pytorch/model_last.pth"
    img_path = "/media/hkuit164/Elements/data/posetrack18/images/test/000691_mpii_test/000025.jpg"

    FP = FrameProcessor()
    img = cv2.imread(img_path)
    FP.process(img)
    cv2.imshow("result", cv2.resize(img, (1080, 720)))
    cv2.waitKey(0)

