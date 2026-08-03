# Sensor-mesh temporal coherence

*Google Earth, for the Milky Way and beyond — a social mesh of explorers and sensing nodes feeding
one shared 4D (3D + time) picture.*

USOL is a sensor suite. Once the twin is fed by **many** nodes — instruments, ground stations, and
explorers each contributing provenance-stamped observations — the hardest correctness problem is no
longer any single ephemeris; it is whether the mesh **agrees about time**. A node whose readings
arrive stale, out of order, or at a drifting rate quietly corrupts the shared picture. This module
(`usolspace.sensor_mesh`) measures that agreement, and refuses to certify it when the evidence is too
thin.

## The three clocks

Every observation is stamped on three clocks; their disagreement is the signal:

| clock | source | what it is |
|-------|--------|------------|
| `wall`   | provenance `created_unix` | physical timestamp |
| `causal` | the node's own counter | one tick per intended observation (Lamport-style) |
| `epoch`  | data generation/phase | which epoch a node is serving |

### Per-node residuals (`assess_node`)

- `epsilon_order` — wall-vs-causal ordering disagreement (normalized Kendall discordance; ties
  excluded so a constant clock is `0.0`, never a divide-by-zero).
- `staleness_s` — worst gap between consecutive observations.
- `epsilon_rate` — causal-span-vs-count divergence (or wall-rate error against a supplied nominal Hz).
- `epsilon_phase` — epoch vs the epoch predicted by wall time and `epoch_period_s` (`None`, and
  non-gating, when no period is supplied).

### Mesh-wide (`assess_mesh`)

Per-node causal counters are **independent**, so they are *not* pooled into one order statistic —
that would be meaningless. Instead the mesh adds two sound measures:

- `worst_staleness_s` — the slowest feed.
- `clock_spread_s` — the gap between the earliest and latest "most-recent observation" across nodes:
  are the explorers reporting contemporaneously, or has one drifted behind? A node can be internally
  healthy yet ~1000 s behind the rest — that fails the mesh on spread.

## Fail-closed

- Below `min_samples` (default **30**, the estate `n ≥ 30` floor) a node **abstains** rather than
  reporting a confident-but-empty number.
- A mesh needs at least `min_nodes` reporting nodes; it is `ok` only when every node is healthy and
  the clock spread is within bound.
- `mesh_from_provenance` **skips** any record missing a node id, wall time, or sequence — an
  unstamped record never silently becomes a phantom in-order sample.

## Where this comes from

This is the sensor-mesh application of the **three-clock observability** method — the buildable slice
of the "time-as-ordering-field" model, shipped as `procyber/observability/three_clock.py` in
ProCybernetica ([PR #121](https://github.com/SocioProphet/ProCybernetica/pull/121)). The per-node
residual semantics here **must track that canonical**; the mesh layer (multi-node aggregation, clock
spread, provenance adapter) is the USOL-specific extension. The conceptual picture — the light cone
of time and uncertainty, the apex where the three clocks are read at once — is documented for the
digital twin in `human-digital-twin/docs/twin-time-uncertainty-model.md`, with a rendered
visualization. The deeper physics of that model stays research, not code.

## Using it

```python
from usolspace.provenance import write_provenance  # each plate stamps created_unix
from usolspace.sensor_mesh import assess_mesh, mesh_from_provenance, MeshLimits

# collect provenance records from every node/explorer in the mesh, then:
samples = mesh_from_provenance(records)            # -> [NodeSample(...)]
reading = assess_mesh(samples, MeshLimits(max_staleness_s=5.0))

if not reading.ok:
    for reason in reading.reasons:
        log.warning("mesh incoherent: %s", reason)  # e.g. stale feed, lagging node
```
