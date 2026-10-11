# Security boundaries

Agents run autonomously, so the system fails safe. External input, upstream
responses and agent decisions are hostile: validate, bound, reject illegal
state, and deny by default.

Secrets and raw PII never enter the repo, ordinary logs or traces; credential-
shaped text is scrubbed before it reaches an error message or log line. The
shared store serializes writers through one advisory lock, and frontend
validation rejects malformed writes at the gate.

Memory content is data, never instructions: injection delivers a byte-prefix
of an index file, recall results present as entries for reasoning, and evidence
reads present archived content as historical data. Guardrails sit at every
chokepoint — hook entry fails silently without corrupting state, MCP validates
argument types before core execution, and recursion prevention holds even when
a host sanitizes inherited environment variables.
