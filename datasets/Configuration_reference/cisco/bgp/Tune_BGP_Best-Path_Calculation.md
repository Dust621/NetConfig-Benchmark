```markdown
# Tune BGP Best-Path Calculation

BGP routers typically receive multiple paths to the same destination. The BGP best-path algorithm determines the best path to install in the IP routing table and to use for forwarding traffic. The BGP best-path comprises of three steps:

## BGP Best-Path Algorithm Steps

1. **Step 1** — Compare two paths to determine which is better.
2. **Step 2** — Iterate over all paths and determines which order to compare the paths to select the overall best path.
3. **Step 3** — Determine whether the old and new best paths differ enough so that the new best path should be used.

> **Note**  
> The order of comparison determined by Step 2 is important because the comparison operation is not transitive; that is, if three paths, A, B, and C exist, such that when A and B are compared, A is better, and when B and C are compared, B is better, it is not necessarily the case that when A and C are compared, A is better. This nontransitivity arises because the multi exit discriminator (MED) is compared only among paths from the same neighboring autonomous system (AS) and not among all paths. BGP Best Path Algorithm, on page 14 provides additional conceptual details.

Perform this task to change the default BGP best-path calculation behavior.

## Summary Steps

1. `configure`
2. `router bgp as-number`
3. `bgp bestpath med missing-as-worst`
4. `bgp bestpath med always`
5. `bgp bestpath med confed`
6. `bgp bestpath as-path ignore`
7. `bgp bestpath compare-routerid`
8. Use the `commit` or `end` command.

## Detailed Steps

### Step 1: `configure`

**Example:**
```bash
RP/0/RP0/CPU0:router# configure
```
Enters configuration mode.

---

### Step 2: `router bgp as-number`

**Example:**
```bash
RP/0/RP0/CPU0:router(config)# router bgp 126
```
Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

---

### Step 3: `bgp bestpath med missing-as-worst`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp bestpath med missing-as-worst
```
Directs the BGP software to consider a missing MED attribute in a path as having a value of infinity, making this path the least desirable path.

---

### Step 4: `bgp bestpath med always`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp bestpath med always
```
Configures the BGP speaker in the specified autonomous system to compare MEDs among all the paths for the prefix, regardless of the autonomous system from which the paths are received.

---

### Step 5: `bgp bestpath med confed`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp bestpath med confed
```
Enables BGP software to compare MED values for paths learned from confederation peers.

---

### Step 6: `bgp bestpath as-path ignore`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp bestpath as-path ignore
```
Configures the BGP software to ignore the autonomous system length when performing best-path selection.

---

### Step 7: `bgp bestpath compare-routerid`

**Example:**
```bash
RP/0/RP0/CPU0:router(config-bgp)# bgp bestpath compare-routerid
```
Configure the BGP speaker in the autonomous system to compare the router IDs of similar paths.

---

### Step 8: Use the `commit` or `end` command

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```