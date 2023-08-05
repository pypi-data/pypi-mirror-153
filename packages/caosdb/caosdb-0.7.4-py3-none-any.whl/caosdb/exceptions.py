# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2020 Florian Spreckelsen <f.spreckelsen@indiscale.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#
"""The exceptions module defines exceptions for HTTP Errors (4xx and 5xx and
HTTP response codes) and for transaction errors (i.e. missing permissions,
dependencies, non-passing consistency checks etc.).
"""

from lxml import etree


class CaosDBException(Exception):
    """Base class of all CaosDB exceptions."""

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg


class ConfigurationError(CaosDBException):
    """ConfigurationError.

    Indicates a misconfiguration.

    Parameters
    ----------
    msg : str
        A descriptin of the misconfiguration. The constructor adds
        a few lines with explainingg where to find the configuration.

    Attributes
    ----------
    msg : str
        A description of the misconfiguration.
    """

    def __init__(self, msg):
        super().__init__(msg + ConfigurationError._INFO)

    _INFO = ("\n\nPlease check your ~/.pycaosdb.ini and your $PWD/"
             ".pycaosdb.ini. Does at least one of them exist and are they correct?")


class ServerConfigurationException(CaosDBException):
    """The server is configured in a different way than expected.

    This can be for example unexpected flags or settings or missing extensions.
    """


class HTTPClientError(CaosDBException):
    """HTTPClientError represents 4xx HTTP client errors."""

    def __init__(self, msg, status, body):
        self.status = status
        self.body = body
        CaosDBException.__init__(self, msg)


class HTTPServerError(CaosDBException):
    """HTTPServerError represents 5xx HTTP server errors."""

    def __init__(self, body):
        xml = etree.fromstring(body)
        error = xml.xpath('/Response/Error')[0]
        msg = error.get("description")

        if error.text is not None:
            msg = msg + "\n\n" + error.text
        CaosDBException.__init__(self, msg)


class CaosDBConnectionError(CaosDBException):
    """Connection is not configured or the network is down."""

    def __init__(self, msg=None):
        CaosDBException.__init__(self, msg)


class HTTPURITooLongError(HTTPClientError):
    """The URI of the last request was too long."""

    def __init__(self, msg=None):
        HTTPClientError.__init__(self, msg=msg, status=414, body=None)


class LoginFailedError(CaosDBException):
    """Login failed.

    Probably, your username/password pair is wrong.
    """

    def __init__(self, msg=None):
        CaosDBException.__init__(self, msg=msg)


class HTTPForbiddenError(HTTPClientError):
    """You're lacking the required permissions. Corresponds to HTTP status
    403.

    """

    def __init__(self, msg=None):
        HTTPClientError.__init__(self, msg=msg, status=403, body=None)


class HTTPResourceNotFoundError(HTTPClientError):
    """The requested resource doesn't exist; corresponds to HTTP status
    404.

    """

    def __init__(self, msg=None):
        HTTPClientError.__init__(self, msg=msg, status=404, body=None)


class MismatchingEntitiesError(CaosDBException):
    """Mismatching entities were found during container sync."""


# ######################### Bad query errors ###########################


class BadQueryError(CaosDBException):
    """Base class for query errors that are not transaction errors."""


class QueryNotUniqueError(BadQueryError):
    """A unique query or retrieve found more than one entity."""


class EmptyUniqueQueryError(BadQueryError):
    """A unique query or retrieve dound no result."""


# ######################### Transaction errors #########################


class TransactionError(CaosDBException):
    """An error of this type is raised whenever any transaction fails with
    one or more entities between client and CaosDB server. More
    detailed errors are collected as direct and indirect children in
    the 'errors' list (direct children) and the 'all_errors' set (set
    of all direct and indirect children).

    """

    def __init__(self, error=None,
                 msg="An error occured during the transaction.",
                 container=None):
        CaosDBException.__init__(self, msg=msg)
        self.errors = []
        self.all_errors = set()
        self.entities = []
        self.all_entities = set()
        self.container = container
        # special case of faulty container
        if container is not None and container.get_errors() is not None:
            self.code = container.get_errors()[0].code
        else:
            self.code = None
        if error is not None:
            self.add_error(error)

    def has_error(self, error_t, direct_children_only=False):
        """Check whether this transaction error contains an error of type
        error_t. If direct_children_only is True, only direct children
        are checked.

        Parameters
        ----------
        error_t : EntityError
            error type to be checked
        direct_children_only: bool, optional
            If True, only direct children, i.e., all errors in
            self.errors are checked. Else all direct and indirect
            children, i.e., all errors in self.all_errors are
            used. Default is false.

        Returns
        -------
        has_error : bool
            True if at least one of the children is of type error_t,
            False otherwise.

        """

        test_set = self.errors if direct_children_only else self.all_errors
        return any([isinstance(err, error_t) for err in test_set])

    def add_error(self, error):
        """Add an error as a direct child to this TransactionError.

        @param error: An EntityError or a list of EntityErrors.

        @raise TypeError: If and only if the 'error' parameter is not an
        instance of EntityError.

        @return: self.
        """

        if hasattr(error, "__iter__"):
            for err in error:
                self.add_error(err)

            return self
        elif isinstance(error, EntityError):
            self.errors.append(error)
            self.entities.append(error.entity)

            self.all_errors.add(error)
            self.all_errors.update(error.all_errors)
            self.all_entities.add(error.entity)
            self.all_entities.update(error.all_entities)

            return self
        else:
            raise TypeError(
                "Argument is to be an EntityError or a list of EntityErrors.")

    def _repr_reasons(self, indent):
        if self.errors is not None and len(self.errors) > 0:
            ret = "\n" + indent + "    +--| REASONS |--"

            for err in self.errors:
                ret += '\n' + indent + '    |  -> ' + \
                    err.__str__(indent=indent + '    |')
            ret += "\n" + indent + "    +----------------"

            return ret
        else:
            return ''

    def _repr_head(self, indent):
        return indent + str(type(self).__name__) + (
            (': ' + self.msg)
            if hasattr(self, 'msg') and self.msg is not None
            else ''
        )

    def __str__(self, indent=''):
        ret = self._repr_head(indent=indent)
        ret += self._repr_reasons(indent=indent)

        return ret

    def __repr__(self):
        return self.__str__()


class EntityError(TransactionError):
    """This is the most basic entity error. It is constructed using an
    entity that caused the error and the error message attached by the
    server.

    """

    def __init__(self, error=None, entity=None):
        TransactionError.__init__(self)
        self.error = error
        if hasattr(error, "code"):
            self.code = error.code
        else:
            self.code = None
        self.entity = entity

        if error is not None and hasattr(error, "encode"):
            self.msg = error
        elif error is not None and hasattr(error, 'description'):
            self.msg = error.description
        elif error is None:
            self.msg = None
        else:
            self.msg = str(error)

    @property
    def description(self):
        """The description of the error."""
        return self.error.description if self.error is not None else None

    def _repr_head(self, indent):
        if hasattr(self, 'entity') and self.entity is not None:
            return (str(type(self.entity).__name__).upper() + " (id: " +
                    str(self.entity.id) + ((", name: " + "'" + str(self.entity.name) + "'") if
                                           self.entity.name is not None else '') + ") CAUSED " +
                    TransactionError._repr_head(self, indent))
        else:
            return TransactionError._repr_head(self, indent)


class UniqueNamesError(EntityError):
    """A name was supposed to be unique but was not."""


class UnqualifiedParentsError(EntityError):
    """This entity has unqualified parents (see 'errors' attribute for a
    list of errors of the parent entities or 'entities' attribute for
    a list of parent entities with errors).

    """


class UnqualifiedPropertiesError(EntityError):
    """This entity has unqualified properties (see 'errors' attribute for
    a list of errors of the properties or 'entities' attribute for a
    list of properties with errors).

    """


class EntityDoesNotExistError(EntityError):
    """This entity does not exist."""


class EntityHasNoDatatypeError(EntityError):
    """This has to have a data type."""


class ConsistencyError(EntityError):
    """The transaction violates database consistency."""


class AuthorizationError(EntityError):
    """You are not allowed to do what ever you tried to do.

    Maybe you need more privileges or a user account.
    """


class AmbiguousEntityError(EntityError):
    """A retrieval of the entity was not possible because there is more
    than one possible candidate.
    """
