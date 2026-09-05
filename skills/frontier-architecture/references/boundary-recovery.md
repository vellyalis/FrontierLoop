# Existing-system boundary recovery lane

Use bounded recovery when ownership, state writes, side effects, and dependency direction are already
tangled. This is not authority for an omnibus cleanup.

1. Inventory the real entry points, callers, state readers and writers, side effects, contracts, tests,
   observability, and recovery behavior for one bounded responsibility.
2. Choose one canonical owner and the smallest slice whose callers, contract, verification, and rollback
   can move together.
3. Introduce a seam only when it removes owner ambiguity or reverses a harmful dependency. Route real
   consumers through it and prove success and failure behavior before cutover.
4. Cut over to the canonical owner and remove the superseded runtime path in the same bounded transition,
   or use an explicit migration with a removal condition when active contracts prevent that.
5. Stop when that boundary is responsibility-correct. Report neighboring debt without rewriting it, and
   never retain indefinite dual ownership as a compatibility fallback.
