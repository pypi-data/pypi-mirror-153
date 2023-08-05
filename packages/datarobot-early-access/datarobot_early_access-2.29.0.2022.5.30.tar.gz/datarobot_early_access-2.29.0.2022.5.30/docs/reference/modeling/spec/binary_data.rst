.. _binary_data:

**************************
Working with binary data
**************************


Preparing data for training
===========================

Working with binary files using the DataRobot API requires prior dataset preparation in one of the
supported formats. See `"Prepare the dataset" <https://docs.datarobot.com/en/docs/modeling/special-workflows/visual-ai/vai-model.html#prepare-the-dataset>`_
for more detail. When the dataset is ready, you can start a project following one of the methods
described in working with :ref:`datasets` and :ref:`projects`.


Preparing data for predictions
==============================

For project creation and a lot of the prediction options, DataRobot allows you to upload ZIP
archives with binary files (e.g. images files). Whenever possible it is recommended to use this
option. However, in a few cases the API routes only allow you to upload your dataset in the JSON
or CSV format. In these cases, you can add the binary files as base64 strings to your dataset.


Processing images
=================


Installation
************

To enable support for processing images, install the datarobot library with the ``images`` option:

::

    pip install datarobot[images]


This will install all needed dependencies for image processing.


Processing images
*****************

When working with image files, helper functions may first transform your images before encoding
their binary data as base64 strings.

Specifically, helper functions will perform these steps:
 - Retrieve binary data from the file in the specified location (local path or URL).
 - Resize images to the image size used by DataRobot and save them in a different format
 - Convert binary data to base64-encoded strings.

Working with images locally and located on external servers differs only in the steps related
to binary file retrieval. The following steps for transformation and conversion to base64-encoded
strings are the same.

This examples uses data stored in a folder structure:

::

    /home/user/data/predictions
        ├── images
        ├  ├──animal01.jpg
        ├  ├──animal02.jpg
        ├  ├──animal03.png
        ├── data.csv


As an input for processing, DataRobot needs a collection of image locations. Helper functions
will process the images and return base64-encoded strings in the same order. The first example
uses the contents of **data.csv** as an input. This file holds data needed for model predictions
and also the image storage locations (in the **"image_path"** column).

Contents of data.csv:

::

    weight_in_grams,age_in_months,image_path
    5000,34,/home/user/data/predictions/images/animal01.jpg
    4300,56,/home/user/data/predictions/images/animal02.jpg
    4200,22,/home/user/data/predictions/images/animal03.png


This code snippet will read each image from the "image_path" column and store the base64-string
with image data in the "image_base64" column.

.. code-block:: python

    import os
    import pandas as pd
    from datarobot.helpers.binary_data_utils import get_encoded_image_contents_from_paths

    dataset_dir = '/home/user/data/predictions'
    file_in = os.path.join(dataset_dir, 'data.csv')
    file_out = os.path.join(dataset_dir, 'out.csv')

    df = pd.read_csv(file_in)
    df['image_base64'] = get_encoded_image_contents_from_paths(df['image_path'])
    df.to_csv(file_out, index=False)


The same helper function will work with other iterables:

.. code-block:: python

    import os
    from datarobot.helpers.binary_data_utils import get_encoded_image_contents_from_paths

    images_dir = '/home/user/data/predictions/images'
    images_absolute_paths = [
        os.path.join(images_dir, file) for file in ['animal01.jpg', 'animal02.jpg', 'animal03.png']
    ]

    images_base64 = get_encoded_image_contents_from_paths(images_absolute_paths)


There is also one helper function to work with remote data. This function retrieves binary content
from specified URLs, transforms the images, and returns base64-encoded strings (in the the same way
as it does for images loaded from local paths).

Example:

.. code-block:: python

    import os
    from datarobot.helpers.binary_data_utils import get_encoded_image_contents_from_urls

    image_urls = [
        'https://<YOUR_SERVER_ADDRESS>/animal01.jpg',
        'https://<YOUR_SERVER_ADDRESS>/animal02.jpg',
        'https://<YOUR_SERVER_ADDRESS>/animal03.png'
    ]

    images_base64 = get_encoded_image_contents_from_urls(image_urls)


Examples of helper functions up to this points have used default settings. If needed, the following
functions allow for further customization by passing explicit parameters related to error handling,
image transformations, and request header customization.


Custom image transformations
****************************

By default helper functions will apply transformations, which have proven good results. The default
values align with the preprocessing used for images uploaded in ZIP archives for training.
Therefore, using default values should be the first choice when preparing datasets with images
for predictions. However, you can also specify custom image transformation settings to override
default transformations before converting data into base64 strings. To override the default
behavior, create an instance of the ``ImageOptions`` class and pass it as an additional parameter
to the helper function.

Examples:

.. code-block:: python

    import os
    from datarobot.helpers.image_utils import ImageOptions
    from datarobot.helpers.binary_data_utils import get_encoded_image_contents_from_paths

    images_dir = '/home/user/data/predictions/images'
    images_absolute_paths = [
        os.path.join(images_dir, file) for file in ['animal01.jpg', 'animal02.jpg', 'animal03.png']
    ]

    # Override the default behavior for image quality and subsampling, but the images
    # will still be resized because that's the default behavior. Note: the `keep_quality`
    # parameter for JPEG files by default preserves the quality of the original images,
    # so this behavior must be disabled to manually override the quality setting with an
    # explicit value.
    image_options = ImageOptions(keep_quality=False, image_quality=80, image_subsampling=0)
    images_base64 = get_encoded_image_contents_from_paths(
        paths=images_absolute_paths, image_options=image_options
    )


    # overwrite default behaviour for image resizing, this will keep image aspect
    # ratio and will resize all images using specified size: width=300 and height=300.
    # Note: if image had different aspect ratio originally it will generate image
    # thumbnail, not larger than the original, that will fit in requested image size
    image_options = ImageOptions(image_size=(300, 300))
    images_base64 = get_encoded_image_contents_from_paths(
        paths=images_absolute_paths, image_options=image_options
    )

    # Override the default behavior for image resizing, This will force the image
    # to be resized to size: width=300 and height=300. When the image originally
    # had a different aspect ratio - than resizing it using `force_size` parameter
    # will alter its aspect ratio modifying the image (e.g. stretching)
    image_options = ImageOptions(image_size=(300, 300), force_size=True)
    images_base64 = get_encoded_image_contents_from_paths(
        paths=images_absolute_paths, image_options=image_options
    )

    # overwrite default behaviour and retain original image sizes
    image_options = ImageOptions(should_resize=False)
    images_base64 = get_encoded_image_contents_from_paths(
        paths=images_absolute_paths, image_options=image_options
    )




Custom request headers
**********************

If needed, you can specify custom request headers for downloading binary data.

Example:

.. code-block:: python

    import os
    from datarobot.helpers.binary_data_utils import get_encoded_image_contents_from_urls

    token = 'Nl69vmABaEuchUsj88N0eOoH2kfUbhCCByhoFDf4whJyJINTf7NOhhPrNQKqVVJJ'
    custom_headers = {
        'User-Agent': 'My User Agent',
        'Authorization': 'Bearer {}'.format(token)
    }

    image_urls = [
        'https://<YOUR_SERVER_ADDRESS>/animal01.jpg',
        'https://<YOUR_SERVER_ADDRESS>/animal02.jpg',
        'https://<YOUR_SERVER_ADDRESS>/animal03.png',
    ]

    images_base64 = get_encoded_image_contents_from_urls(image_urls, custom_headers)


Handling errors
***************

When processing multiple images, any error during processing will, by default, stop operations
(i.e., the helper function will raise ``datarobot.errors.ContentRetrievalTerminatedError`` and
terminate further processing). In the case of an error during content retrieval ("connectivity
issue", "file not found" etc), you can override this behavior by passing ``continue_on_error=True``
to the helper function. When specified, processing will continue. In rows where the error was
raised, the value``None`` value will be returned instead of a base64-encoded string. This applies
only to errors during content retrieval, other errors will always terminate execution.

Example:

.. code-block:: python

    import os
    from datarobot.helpers.binary_data_utils import get_encoded_image_contents_from_paths

    images_dir = '/home/user/data/predictions/images'
    images_absolute_paths = [
        os.path.join(images_dir, file) for file in ['animal01.jpg', 'missing.jpg', 'animal03.png']
    ]

    # This execution will print None for missing files and base64 strings for exising files
    images_base64 = get_encoded_image_contents_from_paths(images_absolute_paths, continue_on_error=True)
    for value in images_base64:
        print(value)

    # This execution will raise error during processing of missing file terminating operation
    images_base64 = get_encoded_image_contents_from_paths(images_absolute_paths)


Processing other binary files
=============================

Other binary files can be processed by dedicated functions. These functions work similarly to the
functions used for images, although they do not provide functionality for any transformations.
Processing follows two steps instead of three:

 - Retrieve binary data from the file in the specified location (local path or URL).
 - Convert binary data to base64-encoded strings.

To process documents into base64-encoded strings use these functions:
 
 - To retrieve files from local paths: **get_encoded_file_contents_from_paths** - t
 - To retrieve files from locations specified as URLs: **get_encoded_file_contents_from_urls** - 

Examples:

.. code-block:: python

    import os
    from datarobot.helpers.binary_data_utils import get_encoded_file_contents_from_urls

    document_urls = [
        'https://<YOUR_SERVER_ADDRESS>/document01.pdf',
        'https://<YOUR_SERVER_ADDRESS>/missing.pdf',
        'https://<YOUR_SERVER_ADDRESS>/document03.pdf',
    ]

    # this call will return base64 strings for existing documents and None for missing files
    documents_base64 = get_encoded_file_contents_from_urls(document_urls, continue_on_error=True)
    for value in documents_base64:
        print(value)

    # This execution will raise error during processing of missing file terminating operation
    documents_base64 = get_encoded_file_contents_from_urls(document_urls)