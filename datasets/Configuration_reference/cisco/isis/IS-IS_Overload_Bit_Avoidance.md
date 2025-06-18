```markdown
# IS-IS Overload Bit Avoidance

The IS-IS overload bit avoidance feature allows network administrators to prevent label switched paths (LSPs) from being disabled when a router in that path has its Intermediate System-to-Intermediate System (IS-IS) overload bit set.

When the IS-IS overload bit avoidance feature is activated, all nodes with the overload bit set, including head nodes, mid nodes, and tail nodes, are ignored, which means that they are still available for use with label switched paths (LSPs).

The IS-IS overload bit avoidance feature does not change the default behavior on nodes that have their overload bit set if those nodes are not included in the path calculation (PCALC).

## Note

The IS-IS overload bit avoidance feature is activated using the following command:

```bash
mpls traffic-eng path-selection ignore overload
```

The IS-IS overload bit avoidance feature is deactivated using the no form of this command:

```bash
no mpls traffic-eng path-selection ignore overload
```

When the IS-IS overload bit avoidance feature is deactivated, nodes with the overload bit set cannot be used as nodes of last resort.

## Configure IS-IS Overload Bit Avoidance

This task describes how to activate IS-IS overload bit avoidance.

### Before you begin

The IS-IS overload bit avoidance feature is valid only on networks that support the following features:

- MPLS
- IS-IS

### SUMMARY STEPS

1. `configure`
2. `mpls traffic-eng path-selection ignore overload`

### DETAILED STEPS

#### Step 1

```bash
configure
```

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2

```bash
mpls traffic-eng path-selection ignore overload
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# mpls traffic-eng path-selection ignore overload
```

Activates IS-IS overload bit avoidance.

## Configuring IS-IS Overload Bit Avoidance: Example

The following example shows how to activate IS-IS overload bit avoidance:

```bash
config
mpls traffic-eng path-selection ignore overload
```

The following example shows how to deactivate IS-IS overload bit avoidance:

```bash
config
no mpls traffic-eng path-selection ignore overload
```
```