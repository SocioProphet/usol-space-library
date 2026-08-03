"""Sensor-mesh temporal-coherence tests — teeth both ways.

A clean, contemporaneous mesh passes; each distinct defect (stale feed, out-of-order feed, rate
drift, sub-floor node, too-few nodes, a node lagging behind the others) must fail with the matching
reason. A gate that only ever passes measures nothing.
"""

from usolspace.sensor_mesh import (
    MeshLimits,
    NodeSample,
    assess_mesh,
    assess_node,
    mesh_from_provenance,
)

DT = 0.1  # 0.1 s between observations => 10 Hz


def node(nid: str, base: float, n: int = 32, cstart: int = 0, cstep: int = 1):
    """A clean, aligned node feed anchored at wall time ``base``."""
    return [
        NodeSample(nid, base + i * DT, cstart + i * cstep, int((base + i * DT) // 1.0))
        for i in range(n)
    ]


def test_clean_mesh_is_coherent():
    samples = node("alpha", 1000.0) + node("beta", 1000.0) + node("gamma", 1000.0)
    m = assess_mesh(samples)
    assert m.ok, m.reasons
    assert m.node_count == 3 and m.healthy_count == 3
    assert m.clock_spread_s == 0.0
    assert all(r.epsilon_order == 0.0 and r.epsilon_rate == 0.0 for r in m.nodes)


def test_a_stale_feed_fails_the_mesh():
    stale = node("beta", 1000.0)
    stale[-1] = NodeSample("beta", stale[-2].wall_ts + 30.0, 31, 1030)  # 30 s hole
    m = assess_mesh(node("alpha", 1000.0) + stale)
    assert not m.ok
    assert m.worst_staleness_s >= 30.0
    assert any("beta" in r for r in m.reasons)
    assert any("staleness" in x for r in m.nodes if r.node_id == "beta" for x in r.reasons)


def test_out_of_order_feed_fails():
    m = assess_mesh(node("alpha", 1000.0) + node("beta", 1000.0, cstart=100, cstep=-1))
    beta = next(r for r in m.nodes if r.node_id == "beta")
    assert not beta.ok and beta.epsilon_order == 1.0
    assert not m.ok


def test_rate_drift_feed_fails():
    m = assess_mesh(node("alpha", 1000.0) + node("beta", 1000.0, cstep=2))
    beta = next(r for r in m.nodes if r.node_id == "beta")
    assert not beta.ok and beta.epsilon_rate > 0.5
    assert not m.ok


def test_sub_floor_node_abstains_and_fails_mesh():
    m = assess_mesh(node("alpha", 1000.0) + node("beta", 1000.0, n=10))
    beta = next(r for r in m.nodes if r.node_id == "beta")
    assert not beta.ok and beta.epsilon_order is None
    assert any("insufficient samples" in x for x in beta.reasons)
    assert not m.ok


def test_too_few_nodes_is_not_a_mesh():
    m = assess_mesh(node("alpha", 1000.0))  # a single node
    assert not m.ok
    assert any("too few nodes" in r for r in m.reasons)


def test_a_node_lagging_behind_the_others_fails_on_clock_spread():
    # both feeds are internally clean, but beta is reporting ~1000 s of stale history.
    m = assess_mesh(node("alpha", 1000.0) + node("beta", 0.0))
    alpha = next(r for r in m.nodes if r.node_id == "alpha")
    beta = next(r for r in m.nodes if r.node_id == "beta")
    assert alpha.ok and beta.ok            # each node is internally healthy
    assert m.clock_spread_s >= 900.0
    assert not m.ok                          # ...but the mesh is not contemporaneous
    assert any("clock_spread" in r for r in m.reasons)


def test_phase_gate_when_epoch_period_supplied():
    limits = MeshLimits(epoch_period_s=1.0)
    good = assess_node(node("alpha", 1000.0), limits)
    assert good.ok and good.epsilon_phase == 0.0
    # hold epoch flat while wall crosses many epoch boundaries
    frozen = [NodeSample("beta", 1000.0 + i * DT, i, 0) for i in range(32)]
    bad = assess_node(frozen, limits)
    assert not bad.ok and bad.epsilon_phase is not None and bad.epsilon_phase > 0.05


def test_mesh_from_provenance_adapts_and_skips_unstamped():
    records = [
        {"created_unix": 1000.0, "params": {"node_id": "alpha", "causal_seq": 0, "epoch": 1000}},
        {"created_unix": 1000.1, "params": {"node_id": "alpha", "causal_seq": 1, "epoch": 1000}},
        {"node_id": "beta", "created_unix": 1000.0, "causal_seq": 0},          # top-level, no epoch -> 0
        {"created_unix": 1000.2, "params": {"node_id": "alpha"}},              # no seq -> skipped
        {"params": {"causal_seq": 5, "epoch": 1}},                            # no node/wall -> skipped
    ]
    samples = mesh_from_provenance(records)
    assert len(samples) == 3
    assert {s.node_id for s in samples} == {"alpha", "beta"}
    beta = next(s for s in samples if s.node_id == "beta")
    assert beta.epoch == 0  # default when absent
