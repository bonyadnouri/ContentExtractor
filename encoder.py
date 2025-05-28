from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Any
from enums import FileType
import logging
import subprocess
import aspose.slides as slides

logger = logging.getLogger(__name__)

ENCODER_REGISTRY = {}


def register_encoder(*file_types):
    def decorator(cls):
        for file_type in file_types:
            ENCODER_REGISTRY[file_type] = cls
        return cls
    return decorator

class Encoder(ABC):
    def __init__(self, file: Path, output_dir: Path):
        self.path: Path = file
        self.output_dir: Path = output_dir

    @abstractmethod
    def encode(self) -> List[Any]:
        pass


    
@register_encoder(FileType.PDF)
class PDFEncoder(Encoder):
    def encode(self):
        logger.debug(f"Start PDF encoding: {self.path}")
        # Actual PDF logic here

@register_encoder(FileType.PPTX, FileType.PPT)
class PPTXEncoder(Encoder):
    def encode(self):
        logger.debug(f"Start PowerPoint encoding: {self.path}")
        presentation = slides.Presentation(str(self.path))
        presentation.save(str(self.output_dir), slides.export.SaveFormat.JPG)


def get_encoder(file: Path, output_dir: Path):
    ext = file.suffix.lower()
    try:
        file_type = FileType(ext)
    except ValueError:
        raise ValueError(f"Unsupported file extension: {ext}")

    encoder_cls = ENCODER_REGISTRY.get(file_type)
    if not encoder_cls:
        raise ValueError(f"No encoder registered for file type '{file_type.name}'")

    return encoder_cls(file, output_dir)

def encode(file: Path, output_dir: Path):
    encoder = get_encoder(file, output_dir)
    return encoder.encode()

