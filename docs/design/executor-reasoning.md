# Executor and reasoning

The library core holds no model client. Intelligence lives in the executor package,
which reasons through the host's own CLI by default, or an explicitly configured
operator-owned endpoint; hosts capture, trigger, inject and recall without ever
holding a key.

Every dialect switches its host's own memory off: two memory systems in one run make
the score unattributable. Authentication, transport and response-shape failures are
observable executor failures — an empty reply never advances a watermark, so a
failed projection stops before it can claim settled work.

Manage verdicts use the same discipline. The reasoner chooses only from the menu the
core drafted and replies in a fixed grammar, so a rambling or hijacked judgment can
only fail to decide, never invent an operation.
