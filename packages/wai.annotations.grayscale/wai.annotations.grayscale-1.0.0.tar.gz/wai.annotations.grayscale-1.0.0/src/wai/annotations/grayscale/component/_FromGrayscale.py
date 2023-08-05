import numpy as np

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from wai.annotations.domain.image.segmentation.util import UnlabelledInputMixin
from ..util import GrayscaleFormat


class FromGrayscale(
    RequiresNoFinalisation,
    UnlabelledInputMixin,
    ProcessorComponent[GrayscaleFormat, ImageSegmentationInstance]
):
    """
    Converter from the grayscale image-segmentation format
    into the wai.annotations internal format.
    """
    def process_element(
            self,
            element: GrayscaleFormat,
            then: ThenFunction[ImageSegmentationInstance],
            done: DoneFunction
    ):
        # Create the annotation instance
        annotation = ImageSegmentationAnnotation(self.labels, element.annotations.size)

        # Calculate the indices from the grayscale data of the image
        new_indices = element.annotations.convert("L").tobytes()
        new_indices = np.fromstring(new_indices, dtype=np.uint8)
        new_indices.resize(annotation.indices.shape)
        new_indices = new_indices.astype(np.uint16)

        # Set the indices to the calculated values
        annotation.indices = new_indices

        then(
            ImageSegmentationInstance(
                element.image,
                annotation
            )
        )
