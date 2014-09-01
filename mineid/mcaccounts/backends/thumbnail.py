import logging

from sorl.thumbnail.compat import text_type
from sorl.thumbnail.base import ThumbnailBackend as BaseThumbnailBackend
from sorl.thumbnail.conf import settings, defaults as default_settings
from sorl.thumbnail.images import ImageFile as BaseImageFile, DummyImageFile
from sorl.thumbnail import default

from cStringIO import OutputType


logger = logging.getLogger(__name__)


class ImageFile(BaseImageFile):
    """
    This is a custom version of BaseImageFile that accepts
    StringIO objects (aka "In memory files")
    """
    def __init__(self, file_, storage=None):
        self.file = file_

        super(ImageFile, self).__init__(file_, storage=storage)

    def read(self):
        if hasattr(self.file, 'file') and \
                isinstance(self.file.file, OutputType):
            return self.file.read()
        return super(ImageFile, self).read()


class ThumbnailBackend(BaseThumbnailBackend):
    """
    This is a custom thumbnail backend that sets a custom ImageFile class
    """
    def get_thumbnail(self, file_, geometry_string, **options):
 
        """
        Returns thumbnail as an ImageFile instance for file with geometry and
        options given. First it will try to get it from the key value store,
        secondly it will create it.
        """
        logger.debug(text_type('Getting thumbnail for file [%s] at [%s]'), file_,
                     geometry_string)
        if file_:
            source = ImageFile(file_)
        elif settings.THUMBNAIL_DUMMY:
            return DummyImageFile(geometry_string)
        else:
            return None

        #preserve image filetype
        if settings.THUMBNAIL_PRESERVE_FORMAT:
            options.setdefault('format', self._get_format(file_))

        for key, value in self.default_options.items():
            options.setdefault(key, value)


        # For the future I think it is better to add options only if they
        # differ from the default settings as below. This will ensure the same
        # filenames being generated for new options at default.
        for key, attr in self.extra_options:
            value = getattr(settings, attr)
            if value != getattr(default_settings, attr):
                options.setdefault(key, value)
        name = self._get_thumbnail_filename(source, geometry_string, options)
        thumbnail = ImageFile(name, default.storage)
        cached = default.kvstore.get(thumbnail)
        if cached:
            return cached
        else:
            # We have to check exists() because the Storage backend does not
            # overwrite in some implementations.
            # so we make the assumption that if the thumbnail is not cached, it doesn't exist
            try:
                source_image = default.engine.get_image(source)
            except IOError:
                if settings.THUMBNAIL_DUMMY:
                    return DummyImageFile(geometry_string)
                else:
                    # if S3Storage says file doesn't exist remotely, don't try to
                    # create it and exit early.
                    # Will return working empty image type; 404'd image
                    logger.warn(text_type('Remote file [%s] at [%s] does not exist'), file_, geometry_string)
                    return thumbnail

            # We might as well set the size since we have the image in memory
            image_info = default.engine.get_image_info(source_image)
            options['image_info'] = image_info
            size = default.engine.get_image_size(source_image)
            source.set_size(size)
            try:
                self._create_thumbnail(source_image, geometry_string, options,
                                       thumbnail)
                self._create_alternative_resolutions(source_image, geometry_string,
                                                     options, thumbnail.name)
            finally:
                default.engine.cleanup(source_image)

        # If the thumbnail exists we don't create it, the other option is
        # to delete and write but this could lead to race conditions so I
        # will just leave that out for now.
        default.kvstore.get_or_set(source)
        default.kvstore.set(thumbnail, source)
        return thumbnail
