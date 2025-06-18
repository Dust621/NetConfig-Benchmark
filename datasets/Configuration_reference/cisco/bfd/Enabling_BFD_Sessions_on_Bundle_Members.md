# Enabling BFD Sessions on Bundle Members

To enable BFD sessions on bundle member links, complete these steps:

## SUMMARY STEPS

1. `configure`
2. `interface Bundle-Ether bundle-id`
3. `bfd address-family ipv4 fast-detect`
4. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1

**Purpose**: Enters mode.  

**Command or Action**:  

```bash
RP/0/RP0/CPU0:router# configure
```

---

### Step 2

**Purpose**: Enters interface configuration mode for the specified bundle ID.  

**Command or Action**:  

```bash
RP/0/RP0/CPU0:router(config)# interface Bundle-Ether 1
```

---

### Step 3

**Purpose**: Enables IPv4 BFD sessions on bundle member links.  

**Command or Action**:  

```bash
RP/0/RP0/CPU0:router(config-if)# bfd address-family ipv4 fast-detect
```

---

### Step 4

**Purpose**: Saves or exits the configuration session.  

**Command or Action**:  

- `commit` — Saves the configuration changes and remains within the configuration session.  
- `end` — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  