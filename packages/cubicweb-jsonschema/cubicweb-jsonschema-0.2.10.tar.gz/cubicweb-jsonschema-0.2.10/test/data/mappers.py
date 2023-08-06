from base64 import b64encode, b64decode

from cubicweb import _, Binary

from cubicweb_jsonschema.mappers import (
    BytesMapper,
    CompoundMapper,
    StringMapper,
    yams_match,
)


class EMailMapper(StringMapper):
    __select__ = yams_match(etype='EmailAddress',
                            rtype='address', role='subject')
    format = 'email'


class ThumbnailDataMapper(BytesMapper):
    __select__ = yams_match(etype='Thumbnail',
                            rtype='data', role='subject',
                            target_types='Bytes')

    @staticmethod
    def _type(value):
        return Binary(b64decode(value))

    @staticmethod
    def _value(value):
        return b64encode(value.getvalue()).decode('ascii')


class exif_data(CompoundMapper):
    etype = 'Photo'
    relations = ('exposure_time', 'flash', 'maker_note')
    title = _('EXIF data')
