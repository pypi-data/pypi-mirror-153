# Galleries

Galleries is a python package to manage images galleries and is mainly designed for recognition purposes. With this package you can create a gallery specifying where to get the images from and how to get annotations (if exist) from each image.

# Installation

`pip install galleries`

# Usage

Gallery construction
```python
from galleries.annotations_parsers.file_name_parser import FileNameSepParser
from galleries.gallery import Gallery
from galleries.images_providers.local_files_image_providers import LocalFilesImageProvider


images_provider = LocalFilesImageProvider("path/to/images")
annotations_parser = FileNameSepParser(["label", "age"], sep="_")
gallery = Gallery(images_provider, annotations_parser)
```

Traverse images
```python
images = gallery.get_images()  # returns a generator
for image in images:
  # image is a numpy ndarray
  pass
```

Get annotations
```python
annotations = gallery.get_annotations()  # returns a generator
for annotation in annotations:
  # annotation is a dictionary
  pass
```

You can also generate new data for each image and easily save it using a `GalleryDataHandler`, which is an abstract class. `GalleryGenericDataHandler` is an implementation of this class that takes information of how to generate the new data and where to save it.

For instance, this is a code example of how to extract features from a gallery and save it to disk:
```python
from galleries.write_gallery_data import GalleryGenericDataHandler

feature_extractor = ...  # your feature extractor here which has a features(image) method
data_generator = "<folder name>", "<feature extractor name>", feature_extractor.features

# write features if do not exist
gallery_features_writer = GalleryGenericDataHandler(gallery, "directory/to/save/features")
exist_features = gallery_features_writer.exists_data(data_generator)
if not exist_features:
  gallery_features_writer.write_data(data_generator)

# read features
features = gallery_features_writer.read_data(data_generator)
```
