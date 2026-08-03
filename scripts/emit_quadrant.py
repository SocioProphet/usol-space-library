#!/usr/bin/env python3
"""Emit the quadrant initial-load asset from the canonical USOL nearby-star catalogue.

    python scripts/emit_quadrant.py > quadrant.initial.json

The output is what the client-vue Space Twin ships as its initial data load and what the live USOL
endpoint serves — one canonical source, no hand-typed catalogue in the UI.
"""
import json
import sys

from usolspace.nearby_stars import quadrant_payload

json.dump(quadrant_payload(), sys.stdout, indent=2)
sys.stdout.write("\n")
