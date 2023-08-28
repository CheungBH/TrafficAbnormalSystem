import numpy as np
import abnormal.utils as utils


class WheelchairHandler:
    def __init__(self):
        self.hw_threshold = 0.78

    def process(self, ids, boxes, kps, kps_scores):
        # If Bounding Box is vertical rectangle, ResultVec related position is Ture;
        # If horizontal, ResultVec related position is False;
        ResultVec = np.zeros(len(boxes))
        for index, bbox in enumerate(boxes):
            # print("ratio:", (bbox[2] - bbox[0]) / (bbox[3] - bbox[1]))
            # print("bbox:", bbox)
            # if (bbox[2] - bbox[0]) / (bbox[3] - bbox[1]) > self.hw_threshold:
            #     ResultVec[index] = 1
            # else:
            #     ResultVec[index] = 0

            angle_lknee = utils.get_angle(kps[index][13], kps[index][11], kps[index][15])
            angle_rknee = utils.get_angle(kps[index][14], kps[index][12], kps[index][16])
            angle_lhip = utils.get_angle(kps[index][11], kps[index][5], kps[index][13])
            angle_rhip = utils.get_angle(kps[index][12], kps[index][6], kps[index][14])

            # print('angle left knee = {}'.format(angle_lknee))
            # print('angle right knee = {}'.format(angle_rknee))
            # print('angle left hip = {}'.format(angle_lhip))
            # print('angle right hip = {}'.format(angle_rhip))

            if (angle_lknee < 110 or angle_rknee < 110) and (angle_lknee > 70 or angle_rknee > 70):
                angle_knee = True
            else:
                angle_knee = False

            if (angle_lhip < 120 or angle_rhip < 120) and (angle_lhip > 80 or angle_rhip > 80):
                angle_hip = True
            else:
                angle_hip = False

            if (angle_knee and angle_hip) and ((bbox[2] - bbox[0]) / (bbox[3] - bbox[1]) > self.hw_threshold):
                ResultVec[index] = 1
            else:
                ResultVec[index] = 0

        return ResultVec




