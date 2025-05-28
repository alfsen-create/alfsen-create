# Cognitive Catalyst Demo

This repository demonstrates a minimal "Living ETG" process where a node
modifies its own behavior in response to poor performance. The concept comes
from the idea of a **CognitiveCatalyst**—a meta-agent embedded inside each node
that observes outcomes and can adapt the node's routine on the fly.

## Files

- `demo/demo_catalyst_adapt.py` – Python example showing a self-modifying output
  node in a small grid world.
- `PROJECT_ATLAS_TRIALS.md` – Archived research proposal unrelated to the demo.

## Running the Demo

The repository bundles tiny stub implementations of `ETGGraph`, `Node`, and
`GridEnvironment` so the example runs with no external dependencies or network
access. Simply execute:

```bash
python demo/demo_catalyst_adapt.py
```

If you only want to verify that the script is syntactically correct, run:

```bash
python -m py_compile demo/demo_catalyst_adapt.py
```

## How It Works

The output node initially uses a simple `routine_move_right` action policy. A
`CognitiveCatalyst` inside the node tracks recent rewards. If the average reward
over the last five steps is below `0.2`, the catalyst swaps the node's routine to
`routine_random` and logs the change. When this happens, a message will print to
highlight the adaptation.

This repository serves as a lightweight starting point for experimenting with
self-modifying agents and evolving task graphs.

## Running Without Network Access

All required modules live in this repository. Once cloned, the demo can run in
a restricted environment with no internet connection. If you plan to install
additional packages, do so before locking down network access.

