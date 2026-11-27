import pytest

from ...missions import tca, tch, tre
from .. import Network, tarot


def test_network_accepts_missions_and_names():
    network = Network(
        name="test",
        telescopes=[tca, "tch", tre],
        priorities={"TCA": 2},
    )

    assert len(network) == 3
    assert list(network) == [tca, tch, tre]
    assert network.tca is tca
    assert network.tch is tch
    assert network.priority("TCA") == 2
    assert network.priority(tch) == 0
    assert network.by_priority() == [tca, tch, tre]


def test_network_parses_builtin_name():
    assert Network._cli_parse("tarot") is tarot


def test_network_rejects_duplicate_missions():
    with pytest.raises(ValueError, match="can't be used twice"):
        Network(name="duplicate", telescopes=[tre, tre])


def test_network_rejects_priorities_for_unknown_missions():
    with pytest.raises(ValueError, match="not in the network"):
        Network(name="invalid", telescopes=[tre], priorities={"tca": 1})
