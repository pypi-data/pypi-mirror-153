from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class GrayscaleOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing grayscale format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image segmentation files in the grayscale format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import ToGrayscale, GrayscaleWriter
        return ToGrayscale, GrayscaleWriter

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier
