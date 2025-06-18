# OSPF Authentication Message Digest Management

All OSPF routing protocol exchanges are authenticated and the method used can vary depending on how authentication is configured. When using cryptographic authentication, the OSPF routing protocol uses the Message Digest 5 (MD5) authentication algorithm to authenticate packets transmitted between neighbors in the network.

For each OSPF protocol packet, a key is used to generate and verify a message digest that is appended to the end of the OSPF packet. The message digest is a one-way function of the OSPF protocol packet and the secret key. Each key is identified by the combination of interface used and the key identification. An interface may have multiple keys active at any time.

To manage the rollover of keys and enhance MD5 authentication for OSPF, you can configure a container of keys called a keychain with each key comprising the following attributes: generate/accept time, key identification, and authentication algorithm.

## Configure Authentication Message Digest Management for OSPF

This task explains how to manage authentication of a keychain on the OSPF interface.

### Before you begin

A valid keychain must be configured before this task can be attempted.

### SUMMARY STEPS

1. `configure`
2. `router ospf process-name`
3. `router-id { router-id }`
4. `area area-id`
5. `interface type interface-path-id`
6. `authentication [message-digest keychain | null]`
7. Use the `commit` or `end` command.

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
router ospf process-name
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router ospf 1
```

Enables OSPF routing for the specified routing process and places the router in router configuration mode. The `process-name` argument is any alphanumeric string no longer than 40 characters.

**Note:**

#### Step 3

```bash
router-id { router-id }
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf)# router id 192.168.4.3
```

Configures a router ID for the OSPF process. We recommend using a stable IPv4 address as the router ID.

**Note:**

#### Step 4

```bash
area area-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf)# area 1
```

Enters area configuration mode. The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

#### Step 5

```bash
interface type interface-path-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# interface TenGigE 0/0/0/0
```

Enters interface configuration mode and associates one or more interfaces to the area.

#### Step 6

```bash
authentication [message-digest keychain | null]
```

Configures an MD5 keychain.

**Example:**

The following example shows the configuration for message-digest authentication.

```bash
RP/0/RP0/CPU0:router(config-ospf-ar-if)# authentication message-digest keychain ospf_int1
```

In the above example, the `ospf_intl` keychain must be configured before you attempt this step.

**Note:**

#### Step 7

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

### Examples

The following example shows how to configure the keychain `ospf_intf_1` that contains five key IDs. Each key ID is configured with different send-lifetime values; however, all key IDs specify the same text string for the key.

```bash
key chain ospf_intf_1
 key 1
  send-lifetime 11:30:30 May 1 2007 duration 600
  cryptographic-algorithm MD5
  key-string clear ospf_intf_1
 key 2
  send-lifetime 11:40:30 May 1 2007 duration 600
  cryptographic-algorithm MD5
  key-string clear ospf_intf_1
 key 3
  send-lifetime 11:50:30 May 1 2007 duration 600
  cryptographic-algorithm MD5
  key-string clear ospf_intf_1
 key 4
  send-lifetime 12:00:30 May 1 2007 duration 600
  cryptographic-algorithm MD5
  key-string clear ospf_intf_1
 key 5
  send-lifetime 12:10:30 May 1 2007 duration 600
  cryptographic-algorithm MD5
  key-string clear ospf_intf_1
```

The following example shows that keychain authentication is enabled on the `TenGigE 0/0/0/0` interface:

```bash
show ospf 1 interface TenGigE 0/0/0/0
TenGigE 0/0/0/0 is up, line protocol is up
Internet Address 100.10.10.2/24, Area 0
Process ID 1, Router ID 2.2.2.1, Network Type BROADCAST, Cost: 1
Transmit Delay is 1 sec, State DR, Priority 1
Designated Router (ID) 2.2.2.1, Interface address 100.10.10.2
Backup Designated router (ID) 1.1.1.1, Interface address 100.10.10.1
Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
Hello due in 00:00:02
Index 3/3, flood queue length 0
Next 0(0)/0(0)
Last flood scan length is 2, maximum is 16
Last flood scan time is 0 msec, maximum is 0 msec
Neighbor Count is 1, Adjacent neighbor count is 1
Adjacent with neighbor 1.1.1.1
(Backup Designated Router)
Suppress hello for 0 neighbor(s)
Keychain-based authentication enabled
Key id used is 3
Multi-area interface Count is 0
```

The following example shows output for configured keys that are active:

```bash
show key chain ospf_intf_1
Key-chain: ospf_intf_1/ -
Key 1 -- text "0700325C4836100B0314345D"
 cryptographic-algorithm -- MD5
 Send lifetime:
 11:30:30, 01 May 2007 - (Duration) 600
 Accept lifetime: Not configured
Key 2 -- text "10411A0903281B051802157A"
 cryptographic-algorithm -- MD5
 Send lifetime:
 11:40:30, 01 May 2007 - (Duration) 600
 Accept lifetime: Not configured
Key 3 -- text "06091C314A71001711112D5A"
 cryptographic-algorithm -- MD5
 Send lifetime:
 11:50:30, 01 May 2007 - (Duration) 600
 [Valid now]
 Accept lifetime: Not configured
Key 4 -- text "151D181C0215222A3C350A73"
 cryptographic-algorithm -- MD5
 Send lifetime:
 12:00:30, 01 May 2007 - (Duration) 600
 Accept lifetime: Not configured
Key 5 -- text "151D181C0215222A3C350A73"
 cryptographic-algorithm -- MD5
 Send lifetime:
 12:10:30, 01 May 2007 - (Duration) 600
 Accept lifetime: Not configured
```