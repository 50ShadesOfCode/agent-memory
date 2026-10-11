# Batch write boundaries

Store handles a batch under one writer lock. Invalid input rejects its own item with
an index and field error; accepted siblings share one projection. Single-record
writes use the same validation and persistence boundary.

Projection after a Store write covers only files the write touched. Full passes
stay on explicit sync and rebuild, which remain the discovery path for changes
made outside Store.

An operational failure during writing or projection aborts the batch. Store restores
touched canonical memory files to their pre-batch contents and projects the restored
truth before propagating the error, provided storage remains available for recovery.
Repeated changes to one file preserve its earliest snapshot. Missing predecessors
retain their existing error category and also abort the batch.

Archived evidence remains append-only, including evidence appended by an aborted
batch. Recovery covers canonical files and their projections; interrupted processes
and persistent storage failures require a separate durable recovery design. Projection
continues to discover changes made outside Store.
