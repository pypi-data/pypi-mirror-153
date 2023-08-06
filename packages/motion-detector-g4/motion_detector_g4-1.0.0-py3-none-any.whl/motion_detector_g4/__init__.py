from cv2 import cv2, SimpleBlobDetector
import numpy
import os


class MotionDetector:

    def __init__(self, minArea = 4000, maxArea = 150000, noiseSize = 10, debug = False):
        """
        :param minArea: Min blob size
        :param maxArea: Max blob size
        :param noiseSize: Max size of noise area
        :param debug: Is debug mod
        """

        self.debug = debug

        self.backSub = cv2.createBackgroundSubtractorMOG2(history=1, detectShadows=False)

        self.denoiseKernel = numpy.ones((noiseSize, noiseSize), numpy.uint8)

        self.blobDetector = self._createBlobDetector(minArea, maxArea)

    def _createBlobDetector(self, minArea: int, maxArea: int) -> SimpleBlobDetector:
        """
        Create and config OpenCV Simple Blob Detector

        :param minArea: Min blob size
        :param maxArea: Max blob size
        :rtype: SimpleBlobDetector
        :return: SimpleBlobDetector
        """

        params = cv2.SimpleBlobDetector_Params()

        params.filterByColor = False

        params.minRepeatability = 1
        params.minThreshold = 250
        params.maxThreshold = 255

        # Filter by Area
        params.filterByArea = True
        params.minArea = minArea
        params.maxArea = maxArea

        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False

        return cv2.SimpleBlobDetector_create(params)

    def applyFirstFrame(self, firstFramePath: str) -> None:
        """
        :param firstFramePath:
        :rtype: None
        :return: None
        """

        firstFrame = cv2.imread(firstFramePath)

        self.backSub.apply(firstFrame)

    def checkMotion(self, nextFramePath: str) -> bool:
        """
        :param nextFramePath: Next frame for comparison
        :rtype: bool
        :return: Is motion
        """

        nextFrame = cv2.imread(nextFramePath)

        # 1. Delete background

        frameMask = self.backSub.apply(nextFrame)

        if self.debug:
            cv2.imwrite(self._addExt(nextFramePath, 'mask'), frameMask)

        # 2. Clear noises

        frameClear = cv2.morphologyEx(frameMask, cv2.MORPH_OPEN, self.denoiseKernel)

        if self.debug:
            cv2.imwrite(self._addExt(nextFramePath, 'clear'), frameClear)

        # 3. Search blobs

        blobs = self.blobDetector.detect(frameClear)

        if len(blobs) > 0:
            if self.debug:
                frameWithBlobs = cv2.drawKeypoints(nextFrame, blobs, numpy.array([]), (0, 0, 255),
                                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                frameMaskWithBlobs = cv2.drawKeypoints(frameClear, blobs, numpy.array([]), (0, 0, 255),
                                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                cv2.imwrite(self._addExt(nextFramePath, 'blobs'), frameWithBlobs)
                cv2.imwrite(self._addExt(nextFramePath, 'blobs2'), frameMaskWithBlobs)

            return True

        return False

    @staticmethod
    def _addExt(path: str, ext: str) -> str:
        """
        Add ext to path

        :param path: Path to file
        :param ext: Added ext
        :rtype: str
        :return: Path with added ext
        """

        pathExt = os.path.splitext(path)
        return pathExt[0] + '.' + ext + pathExt[1]