import logging
import statistics
import time
from typing import List

from detector.DetectionStrategy import DetectionStrategy
from detector.Sample import Sample
from states import Config


class DistanceThresholdCounter(DetectionStrategy):

    OBSERVATION_WINDOW = Config.detection_strategy["DistanceThresholdCounter"]["observation_window"]
    DISTANCE_THRESHOLD = Config.detection_strategy["DistanceThresholdCounter"]["distance_threshold"]
    Samples = List[Sample]

    def __init__(self):
        self.logger = logging.getLogger("AverageDistance")
        self.logger.info("* AverageDistance observation_window[{}] distance_threshold[{}]"
                         .format(self.OBSERVATION_WINDOW, self.DISTANCE_THRESHOLD))

    def detect(self, measurements: Samples):
        current_time_in_sec = round(time.time())
        recent_samples = list(filter(
            lambda s: s.timestamp >= current_time_in_sec - self.OBSERVATION_WINDOW, measurements
        ))
        # if len(recent_samples) == 0:
        #     return False
        recent_distance_values = map(lambda s: s.distance, recent_samples)
        recent_distance_square_filter = map(lambda s: 1 if s < self.DISTANCE_THRESHOLD else 0, recent_distance_values)
        average_distance = statistics.mean(recent_distance_square_filter)
        self.logger.info("Observed window[{}] Presence probability [{}]".format(len(recent_samples), average_distance))
        if average_distance >= 0.5:
            return True
        return False
