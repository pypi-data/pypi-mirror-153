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

"""cubicweb-jsonschema predicates"""

from pyramid import predicates


class NoWildcardAcceptPredicate(predicates.AcceptPredicate):
    """Overrides accept predicate to eliminate match on "*/*" value.

    See https://github.com/Pylons/pyramid/issues/1264.
    """

    def __call__(self, context, request):
        request_accepts = [h for h in request.accept if h != '*/*']
        for accept_type in self.values:
            if accept_type in request_accepts:
                return True
        return False


def includeme(config):
    config.add_route_predicate('strict_accept', NoWildcardAcceptPredicate)
    config.scan(__name__)
