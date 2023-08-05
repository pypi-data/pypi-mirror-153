# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
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

import copy
from lxml import etree


def _translate_to_state_acis(acis):
    result = set()
    for aci in acis:
        aci = copy.copy(aci)
        if aci.role:
            aci.role = "?STATE?" + aci.role + "?"
        result.add(aci)
    return result


class Transition:
    """Transition

    Represents allowed transitions from one state to another.

    Properties
    ----------
    name : str
        The name of the transition
    description: str
        The description of the transition
    from_state : str
        A state name
    to_state : str
        A state name
    """

    def __init__(self, name, from_state, to_state, description=None):
        self._name = name
        self._from_state = from_state
        self._to_state = to_state
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def from_state(self):
        return self._from_state

    @property
    def to_state(self):
        return self._to_state

    def __repr__(self):
        return f'Transition(name="{self.name}", from_state="{self.from_state}", to_state="{self.to_state}", description="{self.description}")'

    def __eq__(self, other):
        return (isinstance(other, Transition)
                and other.name == self.name
                and other.to_state == self.to_state
                and other.from_state == self.from_state)

    def __hash__(self):
        return 23472 + hash(self.name) + hash(self.from_state) + hash(self.to_state)

    @staticmethod
    def from_xml(xml):
        to_state = [to.get("name") for to in xml
                    if to.tag.lower() == "tostate"]
        from_state = [from_.get("name") for from_ in xml
                      if from_.tag.lower() == "fromstate"]
        result = Transition(name=xml.get("name"),
                            description=xml.get("description"),
                            from_state=from_state[0] if from_state else None,
                            to_state=to_state[0] if to_state else None)
        return result


class State:
    """State

    Represents the state of an entity and take care of the serialization and
    deserialization of xml for the entity state.

    An entity state is always a State of a StateModel.

    Properties
    ----------
    name : str
        Name of the State
    model : str
        Name of the StateModel
    description : str
        Description of the State (read-only)
    id : str
        Id of the undelying State record (read-only)
    transitions : set of Transition
        All transitions which are available from this state (read-only)
    """

    def __init__(self, model, name):
        self.name = name
        self.model = model
        self._id = None
        self._description = None
        self._transitions = None

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def transitions(self):
        return self._transitions

    def __eq__(self, other):
        return (isinstance(other, State)
                and self.name == other.name
                and self.model == other.model)

    def __hash__(self):
        return hash(self.name) + hash(self.model)

    def __repr__(self):
        return f"State('{self.model}', '{self.name}')"

    def to_xml(self):
        """Serialize this State to xml.

        Returns
        -------
        xml : etree.Element
        """
        xml = etree.Element("State")
        if self.name is not None:
            xml.set("name", self.name)
        if self.model is not None:
            xml.set("model", self.model)
        return xml

    @staticmethod
    def from_xml(xml):
        """Create a new State instance from an xml Element.

        Parameters
        ----------
        xml : etree.Element

        Returns
        -------
        state : State
        """
        name = xml.get("name")
        model = xml.get("model")
        result = State(name=name, model=model)
        result._id = xml.get("id")
        result._description = xml.get("description")
        transitions = [Transition.from_xml(t) for t in xml if t.tag.lower() ==
                       "transition"]
        if transitions:
            result._transitions = set(transitions)

        return result

    @staticmethod
    def create_state_acl(acl):
        from .models import ACL
        state_acl = ACL()
        state_acl._grants = _translate_to_state_acis(acl._grants)
        state_acl._denials = _translate_to_state_acis(acl._denials)
        state_acl._priority_grants = _translate_to_state_acis(acl._priority_grants)
        state_acl._priority_denials = _translate_to_state_acis(acl._priority_denials)
        return state_acl
