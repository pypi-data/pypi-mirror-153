import numpy as np
from PIL import Image

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image.segmentation import ImageSegmentationInstance
from ..util import GrayscaleFormat


class ToGrayscale(
    RequiresNoFinalisation,
    ProcessorComponent[ImageSegmentationInstance, GrayscaleFormat]
):
    """
    Converts the internal image-segmentation format into the grayscale
    annotation format.
    """
    def process_element(
            self,
            element: ImageSegmentationInstance,
            then: ThenFunction[GrayscaleFormat],
            done: DoneFunction
    ):
        # Create a negative from a negative
        if element.annotations is None:
            return then(GrayscaleFormat(element.data, None))

        # If the number of labels is more than 255, this format can't support it
        if element.annotations.max_index > 255:
            raise Exception("Grayscale format supports a maximum of 255 labels")

        # Convert the index array to RGB bytes, using the same value for the R/G/B channel
        rgb_array = np.zeros((*element.annotations.indices.shape, 3), np.uint8)
        for i in range(3):
            rgb_array[:, :, i] = element.annotations.indices.astype(np.uint8)

        # Create the annotation image
        annotation = Image.frombytes("RGB",
                                     element.annotations.size,
                                     rgb_array.tostring())
        annotation = annotation.convert("L")

        then(
            GrayscaleFormat(
                element.data,
                annotation
            )
        )
