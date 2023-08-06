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
"""cubicweb-jsonschema yams constraints to jsl serializers"""

from logilab.common.registry import Predicate

from . import JSONSchemaMapper


class yams_constraint_type(Predicate):
    """ Predicate that returns 1 when the yams constraint supplied at execution
    time matches the constraint type name supplied at construction time (e.g.
    "SizeConstraint", "StaticVocabularyConstraint", etc.).
    """

    def __init__(self, cstr_type):
        self.cstr_type = cstr_type

    def __call__(self, cls, vreg, _, etype, rtype, cstr, jsl_attrs):
        if cstr.type() == self.cstr_type:
            return 1
        return 0


class JslConstraintSerializer(JSONSchemaMapper):
    __regid__ = 'jsonschema.constraint'
    __abstract__ = True

    def __init__(self, vreg, _, etype, rtype, constraint, jsl_attrs):
        self.vreg = vreg
        self._ = _
        self.etype = vreg.schema[etype]
        self.rtype = vreg.schema[rtype]
        self.constraint = constraint
        self.jsl_attrs = jsl_attrs

    def todict(self):
        raise NotImplementedError


class JslSizeConstraintSerializer(JslConstraintSerializer):
    __select__ = yams_constraint_type('SizeConstraint')

    def todict(self):
        if ('min_length' not in self.jsl_attrs
                and self.constraint.min is not None):
            return {'min_length': self.constraint.min}
        if ('max_length' not in self.jsl_attrs
                and self.constraint.max is not None):
            return {'max_length': self.constraint.max}


class JslIntervalBoundConstraintSerializer(JslConstraintSerializer):
    __select__ = yams_constraint_type('IntervalBoundConstraint')

    def todict(self):
        if ('minimum' not in self.jsl_attrs
                and self.constraint.minvalue is not None):
            return {'minimum': self.constraint.minvalue}
        if ('maximum' not in self.jsl_attrs
                and self.constraint.maxvalue is not None):
            return {'maximum': self.constraint.maxvalue}
