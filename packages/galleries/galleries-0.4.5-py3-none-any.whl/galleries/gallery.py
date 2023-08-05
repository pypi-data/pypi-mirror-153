import numpy as np
from typing import Any, Dict, Optional, List

from galleries.annotations_filtering.filter import FilterStatement
from galleries.annotations_filtering.utils import does_annotations_meets_filter
from galleries.annotations_parsers.file_name_parser import FileNameSepParser
from galleries.images_providers.local_files_image_providers import LocalFilesImageProvider

from galleries.annotations_parsers.gallery_annots_parsers import GalleryAnnotationsParser
from galleries.igallery import IGallery
from galleries.images_providers.gallery_images_provider import GalleryImagesProvider


class Gallery(IGallery):

	def __init__(
			self,
			name: str = "",
			images_provider: GalleryImagesProvider = LocalFilesImageProvider(),
			annots_parser: GalleryAnnotationsParser = FileNameSepParser()
	):
		self._name = name
		self._images_provider = images_provider
		self._annots_parser = annots_parser

	@property
	def images_provider(self):
		return self._images_provider

	@images_provider.setter
	def images_provider(self, value):
		self._images_provider = value

	@property
	def annotations_parser(self):
		return self._annots_parser

	@annotations_parser.setter
	def annotations_parser(self, value):
		self._annots_parser = value

	def get_name(self) -> str:
		return self._name

	def set_name(self, name: str):
		self._name = name

	def get_indices(self, filters: List[List[FilterStatement]] = None):
		indices = self._images_provider.get_indices()
		filters = filters or []
		for index in indices:
			annotations = self.get_annotations_by_index(index)
			meets_filter = does_annotations_meets_filter(annotations, filters)
			if meets_filter:
				yield index

	def get_image_by_index(self, index: Any) -> np.ndarray:
		return self._images_provider.get_image_by_index(index)

	def get_annotations_by_index(self, img_index):
		return self._annots_parser.get_annotations_by_image_index(img_index)

	def get_annotations_types(self) -> Optional[Dict[str, type]]:
		return self._annots_parser.get_annotations_types()

	def get_discrete_annotations_values(self) -> Dict[str, list]:
		return self._annots_parser.get_discrete_annotations_values()


# register_as_setting(Gallery, "_name")
# register_as_setting(Gallery, "_images_provider")
# register_as_setting(Gallery, "_annots_parser")


