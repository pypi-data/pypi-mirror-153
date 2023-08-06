from yams.buildobjs import (
    EntityType,
    Boolean,
    Bytes,
    ComputedRelation,
    Date,
    Float,
    Int,
    RelationDefinition,
    String,
    RichString,
)
from cubicweb.schema import (
    ERQLExpression,
    RRQLExpression,
)


class Photo(EntityType):
    data = Bytes(required=True)
    media_type = String(vocabulary=[u'png', u'jpeg'],
                        required=True, default=u'png')
    exposure_time = Float()
    flash = Boolean(required=True, default=False)
    maker_note = Bytes()


class Thumbnail(EntityType):
    data = Bytes(required=True)


class thumbnail(RelationDefinition):
    subject = 'Photo'
    object = 'Thumbnail'
    cardinality = '?1'
    composite = 'subject'
    inlined = True


class picture(RelationDefinition):
    subject = 'CWUser'
    object = 'Photo'
    cardinality = '*?'
    composite = 'subject'


class EmailAlias(EntityType):
    pass


class use_email(RelationDefinition):
    subject = 'CWUser'
    object = 'EmailAlias'
    cardinality = '*1'
    composite = 'subject'


class Book(EntityType):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': ('managers', 'users'),
        'update': (ERQLExpression('X owned_by U'), ),
        'delete': ('managers', 'users', 'guests'),
    }
    title = String(required=True)
    publication_date = Date()


class Author(EntityType):
    name = String(required=True)


class author(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': (RRQLExpression('U has_update_permission S'), ),
        'delete': (RRQLExpression('U has_update_permission S'), ),
    }
    subject = 'Book'
    object = 'Author'
    cardinality = '?*'


class publications(ComputedRelation):
    rule = 'O author S'


class Topic(EntityType):
    name = String(
        required=True,
        __permissions__={
            'read': ('managers', 'users', 'guests'),
            'add': ('managers', 'users'),
            'update': ('managers', ERQLExpression('NOT EXISTS(O topics X)'), ),
        },
    )


class topics(RelationDefinition):
    subject = 'Book'
    object = 'Topic'
