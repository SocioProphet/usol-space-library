"""Sensor-mesh temporal coherence for the galactic digital twin.

USOL is a *sensor suite*: a social mesh of explorers and sensing nodes, each contributing
provenance-stamped observations to one shared 4D (3D + time) picture — Google Earth for the Milky
Way and beyond. For that picture to be trustworthy, the mesh has to agree about *time*: a node whose
readings arrive stale, out of order, or at a drifting rate quietly corrupts the twin.

This module measures that agreement. It is the sensor-mesh application of the **three-clock
observability** method — every observation is stamped on three clocks and their disagreement is
quantified:

    wall    physical timestamp (USOL provenance ``created_unix``)
    causal  the node's own sample counter (Lamport-style, one per intended observation)
    epoch   a coarse generation/phase counter (e.g. the data epoch a node is serving)

Per node it computes four unit-free residuals (``epsilon_order`` / ``staleness_s`` /
``epsilon_rate`` / ``epsilon_phase``); across the mesh it adds a global wall-vs-causal coherence and
a healthy-node count. Everything is **fail-closed**: below the sample floor (``min_samples``, default
30) a node abstains rather than reporting a confident-but-empty number, and a mesh with too few nodes
or any unhealthy node is not ``ok``.

Provenance of the method: the per-node three-clock residual computation is the canonical instrument
shipped as ``procyber/observability/three_clock.py`` in ProCybernetica (PR #121, the Domain-22
buildable slice of the "time-as-ordering-field" model). It is re-expressed here stdlib-only to keep
``usolspace`` dependency-light; the residual semantics MUST track that canonical — see
``docs/architecture/sensor-mesh-observability.md``. The deeper physics of that model stays research,
not code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence


@dataclass(frozen=True)
class NodeSample:
    """One observation from a mesh node/explorer, stamped on all three clocks."""

    node_id: str
    wall_ts: float          # physical time (e.g. provenance created_unix), seconds
    causal_seq: int         # the node's per-observation counter
    epoch: int              # coarse generation/phase


@dataclass(frozen=True)
class MeshLimits:
    """Thresholds + floors. Every bound is inclusive."""

    min_samples: int = 30           # per-node sample floor (estate n>=30 rule)
    min_nodes: int = 2              # a "mesh" needs at least this many reporting nodes
    max_epsilon_order: float = 0.05
    max_staleness_s: float = 5.0
    max_epsilon_rate: float = 0.10
    max_epsilon_phase: float = 0.05
    epoch_period_s: Optional[float] = None    # None => phase not computed / not gating
    nominal_rate_hz: Optional[float] = None   # None => rate is causal-span-vs-count divergence


@dataclass(frozen=True)
class NodeReading:
    """Per-node three-clock reading plus the fail-closed verdict."""

    node_id: str
    n: int
    epsilon_order: Optional[float]
    staleness_s: Optional[float]
    epsilon_rate: Optional[float]
    epsilon_phase: Optional[float]
    ok: bool
    reasons: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class MeshReading:
    """Mesh-wide coherence across all reporting nodes."""

    node_count: int
    healthy_count: int
    worst_staleness_s: Optional[float]   # slowest feed: max per-node staleness
    clock_spread_s: Optional[float]      # how far apart nodes' most-recent observations are
    ok: bool
    reasons: List[str]
    nodes: List[NodeReading]


def _sign(x: float) -> int:
    return (x > 0) - (x < 0)


def _epsilon_order(pairs: Sequence[tuple]) -> float:
    """Normalized Kendall discordance between wall order and causal order, in [0, 1].

    ``pairs`` is a sequence of (wall_ts, causal_seq). A pair of observations is discordant when the
    sign of their wall difference disagrees with the sign of their causal difference. Observations
    tied on either clock carry no ordering information and are excluded from the denominator, so a
    fully-tied clock yields 0.0 rather than a divide-by-zero.
    """
    n = len(pairs)
    discordant = 0
    comparable = 0
    for i in range(n):
        wi, ci = pairs[i]
        for j in range(i + 1, n):
            sw = _sign(wi - pairs[j][0])
            sc = _sign(ci - pairs[j][1])
            if sw == 0 or sc == 0:
                continue
            comparable += 1
            if sw != sc:
                discordant += 1
    return discordant / comparable if comparable else 0.0


def assess_node(samples: Sequence[NodeSample], limits: MeshLimits = MeshLimits()) -> NodeReading:
    """Measure one node's three-clock disagreement (fail-closed below the sample floor)."""
    node_id = samples[0].node_id if samples else "?"
    n = len(samples)

    if n < limits.min_samples:
        return NodeReading(node_id, n, None, None, None, None, False,
                           [f"insufficient samples (n={n} < min_samples={limits.min_samples})"])

    by_wall = sorted(samples, key=lambda s: s.wall_ts)
    wall_span = by_wall[-1].wall_ts - by_wall[0].wall_ts
    if wall_span <= 0:
        return NodeReading(node_id, n, None, None, None, None, False,
                           ["non-positive wall span (all samples share a wall timestamp)"])

    epsilon_order = _epsilon_order([(s.wall_ts, s.causal_seq) for s in samples])
    staleness_s = max(by_wall[i + 1].wall_ts - by_wall[i].wall_ts for i in range(len(by_wall) - 1))

    if limits.nominal_rate_hz is not None and limits.nominal_rate_hz > 0:
        wall_rate = (n - 1) / wall_span
        epsilon_rate = abs(wall_rate - limits.nominal_rate_hz) / limits.nominal_rate_hz
    else:
        causal_span = by_wall[-1].causal_seq - by_wall[0].causal_seq
        epsilon_rate = abs(causal_span - (n - 1)) / (n - 1)

    epsilon_phase: Optional[float] = None
    if limits.epoch_period_s is not None and limits.epoch_period_s > 0:
        first = by_wall[0]
        mismatched = sum(
            1 for s in by_wall
            if s.epoch != first.epoch + int((s.wall_ts - first.wall_ts) // limits.epoch_period_s)
        )
        epsilon_phase = mismatched / n

    reasons: List[str] = []
    if epsilon_order > limits.max_epsilon_order:
        reasons.append(f"epsilon_order {epsilon_order:.4f} > {limits.max_epsilon_order}")
    if staleness_s > limits.max_staleness_s:
        reasons.append(f"staleness_s {staleness_s:.4f} > {limits.max_staleness_s}")
    if epsilon_rate > limits.max_epsilon_rate:
        reasons.append(f"epsilon_rate {epsilon_rate:.4f} > {limits.max_epsilon_rate}")
    if epsilon_phase is not None and epsilon_phase > limits.max_epsilon_phase:
        reasons.append(f"epsilon_phase {epsilon_phase:.4f} > {limits.max_epsilon_phase}")

    return NodeReading(node_id, n, epsilon_order, staleness_s, epsilon_rate, epsilon_phase,
                       not reasons, reasons)


def assess_mesh(samples: Sequence[NodeSample], limits: MeshLimits = MeshLimits()) -> MeshReading:
    """Measure temporal coherence across the whole sensing mesh (fail-closed).

    Groups ``samples`` by ``node_id`` and assesses each node with the per-node three-clock method,
    then adds two sound mesh-wide measures (per-node causal counters are independent, so they are NOT
    pooled into one order statistic — that would be meaningless):

      * ``worst_staleness_s`` — the slowest feed (max per-node staleness).
      * ``clock_spread_s`` — the gap between the earliest and latest "most-recent observation" across
        nodes: are the explorers reporting contemporaneously, or has one drifted behind?

    The mesh is ``ok`` only when it has at least ``min_nodes`` reporting nodes, every node is healthy,
    and the clock spread is within ``max_staleness_s``.
    """
    by_node: Dict[str, List[NodeSample]] = {}
    for s in samples:
        by_node.setdefault(s.node_id, []).append(s)

    nodes = [assess_node(v, limits) for _, v in sorted(by_node.items())]
    node_count = len(nodes)
    healthy_count = sum(1 for r in nodes if r.ok)

    reasons: List[str] = []
    if node_count < limits.min_nodes:
        reasons.append(f"too few nodes ({node_count} < min_nodes={limits.min_nodes})")

    worst_staleness = max((r.staleness_s for r in nodes if r.staleness_s is not None), default=None)

    # clock spread: how far apart the nodes' most-recent observations are.
    clock_spread_s: Optional[float] = None
    if by_node:
        latest = [max(s.wall_ts for s in v) for v in by_node.values()]
        clock_spread_s = max(latest) - min(latest)
        if clock_spread_s > limits.max_staleness_s:
            reasons.append(f"clock_spread_s {clock_spread_s:.4f} > {limits.max_staleness_s} (nodes not contemporaneous)")

    unhealthy = [r.node_id for r in nodes if not r.ok]
    if unhealthy:
        reasons.append(f"unhealthy nodes: {', '.join(unhealthy)}")

    return MeshReading(node_count, healthy_count, worst_staleness, clock_spread_s,
                       not reasons, reasons, nodes)


def mesh_from_provenance(
    records: Sequence[dict],
    *,
    node_key: str = "node_id",
    wall_key: str = "created_unix",
    seq_key: str = "causal_seq",
    epoch_key: str = "epoch",
) -> List[NodeSample]:
    """Adapt USOL provenance records into NodeSamples.

    Each record is a provenance dict (see ``provenance.write_provenance`` — ``created_unix`` is the
    wall clock). ``node_id``/``causal_seq``/``epoch`` may live at the top level or under a nested
    ``params`` block (where USOL keeps per-plate parameters); the nested value wins if present.
    Records missing a node id, wall time, or sequence are skipped (fail-closed: an unstamped record
    never silently becomes a phantom in-order sample).
    """
    out: List[NodeSample] = []
    for rec in records:
        params = rec.get("params") or {}
        node = params.get(node_key, rec.get(node_key))
        wall = params.get(wall_key, rec.get(wall_key))
        seq = params.get(seq_key, rec.get(seq_key))
        epoch = params.get(epoch_key, rec.get(epoch_key, 0))
        if node is None or wall is None or seq is None:
            continue
        out.append(NodeSample(str(node), float(wall), int(seq), int(epoch)))
    return out
