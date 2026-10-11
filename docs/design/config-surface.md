# Configuration surface

Every knob lives in config: trigger thresholds, injection and index budgets,
weight steps, clustering thresholds, recall fusion parameters, and per-environment
switches. A tunable hardcoded in a module is a defect — config is the only place
an operator changes behavior.

Configuration validates at load: illegal values fail loudly with a named knob
instead of producing silent bad behavior. Store-level opt-ins (model endpoints,
vector index) stay explicit, and defaults keep the zero-key path: no credential
required to capture, inject, recall or run deterministic management.
