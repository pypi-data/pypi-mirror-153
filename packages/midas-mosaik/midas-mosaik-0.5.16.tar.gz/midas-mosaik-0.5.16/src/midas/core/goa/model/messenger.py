"""This module contains the Messenger, which handles
the communication stuff of the grid operator.

"""
from queue import Queue
from sortedcontainers import SortedDict


class Messenger:
    """Handles incoming and outgoing messages."""

    def __init__(self, params, entity_map):
        self.config = params
        self.entity_map = entity_map
        self.inbox = Queue()
        self.outbox = Queue()

        self.setpoints = None
        self.forecasts = None
        self.real_grid_data = None

    def step(self):
        """Perform a simulation step."""

        # Read the inbox
        messages = self._read_inbox()

        # Filter the messages
        self._filter_messages(messages)

    def receive(self, msg):
        """Receive a message.

        The message is a dictionary containing three keys:
        'from': (id of the source, e.g. '<sid>.<eid>'),
        'topic': (context of the message, e.g., the attribute to set),
        'msg': (content of the message, e.g., value to set)

        """
        self.inbox.put(msg)

    def send(self, msg):
        """Send a message.

        The message is a dictionary containing three keys:
        'to': (id of the destination, e.g., '<sid>.<eid>'),
        'topic': (context of the message, e.g., the attribute to set),
        'msg': (content of the message).

        """
        self.outbox.put(msg)

    def _read_inbox(self):
        """Read all messages from the inbox and wrap them into a
        dictionary.

        """
        messages = SortedDict()
        while not self.inbox.empty():
            msg = self.inbox.get()
            # msg_to = self.gridcfg['connections']['ingoing'][msg['from']]
            if msg["from"] not in messages:
                messages[msg["from"]] = {msg["topic"]: list()}
            if msg["topic"] not in messages[msg["from"]]:
                messages[msg["from"]][msg["topic"]] = list()
            messages[msg["from"]][msg["topic"]].append(msg["msg"])
        return messages

    def _filter_messages(self, messages):
        """Filter the messages according to their purpose."""
        self.setpoints = SortedDict()
        self.forecasts = SortedDict()
        self.real_grid_data = SortedDict()

        for dst, attrs in messages.items():
            _, eid = dst.split(".")[:2]
            if eid in self.entity_map:
                # print('In EntityMap', dst, attrs)
                self._handle_entity_map(eid, attrs)
            elif dst in self.config["der_mapping"]:
                self._handle_unit_map(dst, attrs)
                # print('In UnitMapping', dst, attrs)
            else:
                # print('Without category', dst, attrs)
                pass

    def _handle_entity_map(self, eid, attrs):
        """Handle messages with destinations contained in the
        entity map.

        """
        idx = self.entity_map[eid]["idx"]
        etype = self.entity_map[eid]["etype"]
        static = self.entity_map[eid]["static"]

        if etype.lower() in ["load", "sgen"]:
            self.setpoints.setdefault(etype, SortedDict()).setdefault(
                idx, SortedDict()
            )
            self.setpoints[etype][idx].setdefault("attrs", SortedDict())
            self.setpoints[etype][idx].setdefault("static", static)
            for attr, vals in attrs.items():
                self.setpoints[etype][idx]["attrs"].setdefault(attr, 0)
                self.setpoints[etype][idx]["attrs"][attr] += float(sum(vals))

        elif etype.lower() in ["bus"]:
            self.real_grid_data.setdefault(etype, SortedDict())
            self.real_grid_data[etype].setdefault(idx, SortedDict())
            for attr, vals in attrs.items():
                self.real_grid_data[etype][idx][attr] = vals[0]

        else:
            # Handle transformers, lines, switches, etc
            pass

    def _handle_unit_map(self, dst, attrs):
        """Handle messages from unit models with grid as
        destination.

        """
        cfg = self.config["der_mapping"][dst]
        etype = cfg["type"]
        etype_cap = etype.capitalize()
        bidx = cfg["bus"]
        idx = 0
        static = None
        # for idx in range(len(getattr(self.model.gri)))
        for _, eattrs in self.entity_map.items():
            if (
                eattrs["etype"] == etype_cap
                and eattrs["static"]["bus"] == bidx
            ):
                idx = eattrs["idx"]
                static = eattrs["static"]

        self.setpoints.setdefault(etype_cap, SortedDict())
        self.setpoints[etype_cap].setdefault(idx, SortedDict())
        self.setpoints[etype_cap][idx].setdefault("attrs", SortedDict())
        self.setpoints[etype_cap][idx].setdefault("static", static)

        self.forecasts.setdefault(etype_cap, SortedDict())
        self.forecasts[etype_cap].setdefault(idx, SortedDict())
        self.forecasts[etype_cap][idx].setdefault("static", static)
        self.forecasts[etype_cap][idx].setdefault("src", SortedDict())

        for attr, vals in attrs.items():
            if attr in ["p_mw", "q_mvar"]:
                if is_input_from_unitmod(etype, self.config):
                    val = self.setpoints[etype_cap][idx]["attrs"].get(attr, 0)
                    val += float(sum(vals))
                    self.setpoints[etype_cap][idx]["attrs"][attr] = val
            elif attr == "schedule":
                # Should only be one schedule for each unit model!
                self.forecasts[etype_cap][idx]["src"][dst] = vals[0]


def is_input_from_unitmod(etype, flags):
    """Check whether the given etype should be considered as input."""
    if etype == "load" and not flags["grid_load_sensor"]:
        return True
    if etype == "sgen" and not flags["grid_sgen_sensor"]:
        return True
    return False
