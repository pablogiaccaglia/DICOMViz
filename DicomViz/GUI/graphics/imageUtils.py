from collections import namedtuple
from enum import Enum

import numpy

transformationTuple = namedtuple("transformationTuple", ["function", "partial_params"])

class DEGREES_FROM_TRANSFORMATION(Enum):
    ROTATE_90_CCW = -90
    ROTATE_90_CW = 90
    ROTATE_180 = 180

class FLIP_TRANSFORMATION(Enum):
    FLIP_HORIZONTAL = transformationTuple(function = numpy.fliplr, partial_params = None)
    FLIP_VERTICAL = transformationTuple(function = numpy.flipud, partial_params = None)

class ROTATION_TRANSFORMATION(Enum):
    ROTATE_90_CCW = transformationTuple(function = numpy.rot90, partial_params = (1, (1, 0)))
    ROTATE_90_CW = transformationTuple(function = numpy.rot90, partial_params = (1, (0, 1)))
    ROTATE_180 = transformationTuple(function = numpy.rot90, partial_params = (2, (1, 0)))

class TRANSFORMATION_FROM_DEGREES(Enum):
    _90 = ROTATION_TRANSFORMATION.ROTATE_90_CW
    _neg90 = ROTATION_TRANSFORMATION.ROTATE_90_CCW
    _180 = ROTATION_TRANSFORMATION.ROTATE_180

def getTransformationFromRotationDegrees(degrees: int) -> tuple:

    if degrees <= -180:
        degrees = 360 + degrees

    elif degrees >= 180:
        degrees = degrees - 360

    if degrees == -180:
        degrees = 180

    if degrees == 0:
        return None, 0

    degreesStr = str(degrees)

    if degrees == -90:
        degreesStr = degreesStr.replace("-", "neg")

    enumDegreesName = "_" + degreesStr

    return TRANSFORMATION_FROM_DEGREES[enumDegreesName].value, degrees


def getRotationDegreesFromTransformation(transformation: ROTATION_TRANSFORMATION) -> int:

    return int(DEGREES_FROM_TRANSFORMATION[transformation.name].value)

