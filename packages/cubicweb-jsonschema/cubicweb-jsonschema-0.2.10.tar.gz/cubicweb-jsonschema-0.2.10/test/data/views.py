from cubicweb.web.views import uicfg

from cubicweb_jsonschema.views import jsonschema_section



uicfg.indexview_etype_section['Photo'] = 'subobject'
uicfg.indexview_etype_section['Topic'] = 'subobject'

jsonschema_section.tag_attribute(
    ('CWUser', 'lastname'), 'hidden')
jsonschema_section.tag_subject_of(
    ('CWUser', 'use_email', 'EmailAddress'), 'inlined')
jsonschema_section.tag_subject_of(
    ('CWUser', 'use_email', 'EmailAlias'), 'hidden')
jsonschema_section.tag_object_of(
    ('*', 'use_email', 'EmailAlias'), 'hidden')
jsonschema_section.tag_subject_of(
    ('CWUser', 'picture', '*'), 'inlined')
jsonschema_section.tag_object_of(
    ('*', 'picture', 'Photo'), 'hidden')
jsonschema_section.tag_subject_of(
    ('Photo', 'thumbnail', '*'), 'inlined')

# we don't want this to interfere with entity creation/edition tests
jsonschema_section.tag_subject_of(
    ('CWUser', 'use_email', 'EmailAlias'), 'hidden')
