# Verify OSPF Configuration and Operation

This task explains how to verify the configuration and operation of OSPF.

## SUMMARY STEPS

1. `show { ospf | ospfv3 } [ process-name ]`
2. `show { ospf | ospfv3 } [ process-name ] border-routers [ router-id ]`
3. `show { ospf | ospfv3 } [ process-name ] database`
4. `show { ospf | ospfv3 } [ process-name ] [ area-id ] flood-list interface type interface-path-id`
5. `show { ospf | ospfv3 } [ process-name ] [ vrf vrf-name ] [ area-id ] interface [ type interface-path-id ]`
6. `show { ospf | ospfv3 }[ process-name ] [ area-id ] neighbor [ type interface-path-id ] [ neighbor-id ] [ detail ]`
7. `clear { ospf | ospfv3 }[ process-name ] process`
8. `clear { ospf | ospfv3 }[ process-name ] redistribution`
9. `clear { ospf | ospfv3 }[ process-name ] routes`
10. `clear { ospf | ospfv3 }[ process-name ] vrf [vrf-name|all] {process |redistribution|routes|statistics [interface type interface-path-id|message-queue|neighbor]}`
11. `clear { ospf | ospfv3 }[ process-name ] statistics [ neighbor [ type interface-path-id ] [ ip-address ]]`

## DETAILED STEPS

### Step 1

```bash
show { ospf | ospfv3 } [ process-name ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router# show ospf group1
```

(Optional) Displays general information about OSPF routing processes.

---

### Step 2

```bash
show { ospf | ospfv3 } [ process-name ] border-routers [ router-id ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router# show ospf group1 border-routers
```

(Optional) Displays the internal OSPF routing table entries to an ABR and ASBR.

---

### Step 3

```bash
show { ospf | ospfv3 } [ process-name ] database
```

**Example:**
```bash
RP/0/RP0/CPU0:router# show ospf group2 database
```

(Optional) Displays the lists of information related to the OSPF database for a specific router.

- The various forms of this command deliver information about different OSPF LSAs.

---

### Step 4

```bash
show { ospf | ospfv3 } [ process-name ] [ area-id ] flood-list interface type interface-path-id
```

**Example:**
```bash
RP/0/RP0/CPU0:router# show ospf 100 flood-list interface TenGigE 0/3/0/0
```

(Optional) Displays a list of OSPF LSAs waiting to be flooded over an interface.

---

### Step 5

```bash
show { ospf | ospfv3 } [ process-name ] [ vrf vrf-name ] [ area-id ] interface [ type interface-path-id ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router# show ospf 100 interface TenGigE 0/3/0/0
```

(Optional) Displays OSPF interface information.

---

### Step 6

```bash
show { ospf | ospfv3 }[ process-name ] [ area-id ] neighbor [ type interface-path-id ] [ neighbor-id ] [ detail ]
```

**Example:**
```bash
RP/0/RP0/CPU0:router# show ospf 100 neighbor
```

(Optional) Displays OSPF neighbor information on an individual interface basis.

---

### Step 7

```bash
clear { ospf | ospfv3 }[ process-name ] process
```

**Example:**
```bash
RP/0/RP0/CPU0:router# clear ospf 100 process
```

(Optional) Resets an OSPF router process without stopping and restarting it.

---

### Step 8

```bash
clear { ospf | ospfv3 }[ process-name ] redistribution
```

**Example:**
```bash
RP/0/RP0/CPU0:router# clear ospf 100 redistribution
```

Clears OSPF route redistribution.

---

### Step 9

```bash
clear { ospf | ospfv3 }[ process-name ] routes
```

**Example:**
```bash
RP/0/RP0/CPU0:router# clear ospf 100 routes
```

Clears OSPF route table.

---

### Step 10

```bash
clear { ospf | ospfv3 }[ process-name ] vrf [vrf-name|all] {process |redistribution|routes|statistics [interface type interface-path-id|message-queue|neighbor]}
```

**Example:**
```bash
RP/0/RP0/CPU0:router# clear ospf 100 vrf vrf_1 process
```

Clears OSPF route table.

---

### Step 11

```bash
clear { ospf | ospfv3 }[ process-name ] statistics [ neighbor [ type interface-path-id ] [ ip-address ]]
```

**Example:**
```bash
RP/0/RP0/CPU0:router# clear ospf 100 statistics
```

(Optional) Clears the OSPF statistics of neighbor state transitions.