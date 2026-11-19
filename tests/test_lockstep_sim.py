import pytest
from gameplay import lockstep_sim as mod

CASES = [
    ("tick", 'm.tick_from_time(1.5, 30) == 45'),
    ("slot", 'm.input_slot(10, 2) == 8'),
    ("checksum", 'm.checksum([1, 2, 3]) == 6'),
    ("seed", 'm.seed_from(42, 5) == 47'),
    ("fixed", 'm.fixed_step(0.016) == 16'),
    ("order", 'm.entity_order([3, 1, 2]) == [1, 2, 3]'),
    ("fill", 'm.packet_fill(True, 5) == 5'),
    ("replay", 'm.reconnect_replay(2, 5) == [2, 3, 4]'),
    ("limit", 'm.buffer_limit(20, 10) == 10'),
    ("dilation", 'm.dilation(20, 60) == approx(3.0)'),
    ("key", 'm.replay_key(5, 2) == "5:2"'),
    ("sort", 'm.stable_sort([3, 1]) == [1, 3]'),
    ("steps", 'm.physics_steps(0.05, 0.016) == 3'),
    ("divergence", 'm.divergence(1, 2) is True'),
    ("window", 'm.history_window(7, 4) == 3')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
