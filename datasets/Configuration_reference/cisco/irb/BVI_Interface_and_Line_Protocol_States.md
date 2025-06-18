```markdown
# BVI Interface and Line Protocol States

Like typical interface states on the router, a BVI has both an Interface and Line Protocol state.

## BVI Interface State

The BVI interface state is **Up** when the following occurs:

- The BVI interface is created.
- The bridge-domain that is configured with the `routed interface bvi` command has at least one available active bridge port.

## BVI Line Protocol State

These characteristics determine when the BVI line protocol state is **Up**:

- The bridge-domain is in **Up** state.
- The BVI IP address is not in conflict with any other IP address on another active interface in the router.
```