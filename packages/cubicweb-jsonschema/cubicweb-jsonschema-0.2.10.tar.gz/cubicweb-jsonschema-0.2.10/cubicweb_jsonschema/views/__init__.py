# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-jsonschema views/forms/actions/components for web ui"""

from cubicweb.__pkginfo__ import numversion as cw_version
from cubicweb import neg_role
from cubicweb.rtags import RelationTags
from cubicweb.schema import VIRTUAL_RTYPES, WORKFLOW_RTYPES


class JSONSchemaSectionRelationTags(RelationTags):
    """JSON Schema configuration relation tag.

    This relation tag can be used to configure generation of JSON Schema
    documents through uicfg. It accepts the following sections:

    *   'inlined': relation definition would appear as an inlined document of
        the main entity's JSON Schema,
    *   'hidden': relation definition is hidden from JSON Schema, and,
    *   'related': relation definition would not appear in entity's JSON
        Schema but would appear in a rel="related" hypermedia link.
    """
    __regid__ = 'jsonschema'

    _allowed_values = frozenset(('inlined', 'hidden', 'related'))
    ignored_rtypes = VIRTUAL_RTYPES | WORKFLOW_RTYPES

    def _init(self, sschema, rschema, oschema, role):
        if self.get(sschema, rschema, oschema, role) is not None:
            return
        if (rschema.meta
                or sschema.is_metadata(rschema)
                or rschema.type in self.ignored_rtypes):
            section = 'hidden'
        elif rschema.final:
            # TODO Should we handle Password (oschema.type)? Maybe not because
            # we already have a mapper producing no value.
            section = 'inlined'
        else:
            rdef = rschema.rdef(sschema, oschema)
            if rdef.role_cardinality(role) in '1+':
                section = 'inlined'
            elif rdef.composite == neg_role(role):
                section = 'inlined'
            else:
                section = 'related'
        self.tag_relation((sschema, rschema, oschema, role), section)

    def relations_by_section(self, entity, section, permission):
        """return a list of (rtype, role, target types) for the given entity
        matching 'section' and 'permission'.
        """
        eschema = entity.e_schema
        cnx = entity._cw
        if permission == 'update':
            relpermission = 'add'
        else:
            relpermission = permission
        eid = entity.eid if entity.has_eid() else None
        rdefs = eschema.relation_definitions(includefinal=True)
        for rschema, targetschemas, role in rdefs:
            if rschema in self.ignored_rtypes:
                continue
            relperms_kwargs = {
                'subject': {'fromeid': eid},
                'object': {'toeid': eid},
            }[role]
            target_types = set()
            for tschema in targetschemas:
                if tschema.type == 'Password' and relpermission == 'read':
                    continue
                if section not in self.etype_get(eschema, rschema, role,
                                                 tschema):
                    continue
                rdef = rschema.role_rdef(eschema, tschema, role)
                if rschema.final:
                    if not rdef.has_perm(cnx, permission, eid=eid,
                                         creating=eid is None):
                        continue
                else:
                    if not rdef.has_perm(cnx, relpermission, **relperms_kwargs):
                        continue
                target_types.add(tschema.type)
            if target_types:
                yield rschema.type, role, target_types


if cw_version >= (3, 25):
    jsonschema_section = JSONSchemaSectionRelationTags(__module__=__name__)
else:
    jsonschema_section = JSONSchemaSectionRelationTags()
