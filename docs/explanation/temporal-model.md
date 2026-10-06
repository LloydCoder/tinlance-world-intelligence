# Temporal model

World Intelligence distinguishes several clocks.

| Timestamp | Meaning |
| --- | --- |
| `event_time` | When an event occurred |
| `valid_time` | When a state or relationship is valid |
| `observed_at` | When a source observation was made |
| `ingested_at` | When the platform accepted the artifact/record |
| `knowledge_as_of` | What the system knew at a selected historical point |

This supports current-state queries, historical reconstruction, knowledge-as-of analysis, deterministic replay, and change detection without destructive mutation.

A newer observation does not automatically make an older observation false; provenance and contradiction records preserve that distinction.
