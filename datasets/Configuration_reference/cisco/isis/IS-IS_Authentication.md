```markdown
# IS-IS Authentication

Authentication is available to limit the establishment of adjacencies by using the `hello-password` command, and to limit the exchange of LSPs by using the `lsp-password` command.

IS-IS supports plain-text authentication, which does not provide security against unauthorized users. Plain-text authentication allows you to configure a password to prevent unauthorized networking devices from forming adjacencies with the router. The password is exchanged as plain text and is potentially visible to an agent able to view the IS-IS packets.

When an HMAC-MD5 password is configured, the password is never sent over the network and is instead used to calculate a cryptographic checksum to ensure the integrity of the exchanged data.

IS-IS stores a configured password using simple encryption. However, the plain-text form of the password is used in LSPs, sequence number protocols (SNPs), and hello packets, which would be visible to a process that can view IS-IS packets. The passwords can be entered in plain text (clear) or encrypted form.

To set the domain password, configure the `lsp-password` command for Level 2; to set the area password, configure the `lsp-password` command for Level 1.

The keychain feature allows IS-IS to reference configured keychains. IS-IS key chains enable hello and LSP keychain authentication. Keychains can be configured at the router level (in the case of the `lsp-password` command) and at the interface level (in the case of the `hello-password` command) within IS-IS. These commands reference the global keychain configuration and instruct the IS-IS protocol to obtain security parameters from the global set of configured keychains.

IS-IS is able to use the keychain to implement hitless key rollover for authentication. Key rollover specification is time based, and in the event of clock skew between the peers, the rollover process is impacted. The configurable tolerance specification allows for the accept window to be extended (before and after) by that margin. This accept window facilitates a hitless key rollover for applications (for example, routing and management protocols).

## Configure Authentication for IS-IS

This task explains how to configure authentication for IS-IS. This task is optional.

### SUMMARY STEPS

1. `configure`
2. `router isis instance-id`
3. `lsp-password { hmac-md5 | text } { clear | encrypted } password [ level { 1 | 2 }] [ send-only ] [ snp send-only ]`
4. `interface type interface-path-id`
5. `hello-password { hmac-md5 | text } { clear | encrypted } password [ level { 1 | 2 }] [ send-only ]`
6. Use the `commit` or `end` command.

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
router isis instance-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router isis isp
```

Enables IS-IS routing for the specified routing instance, and places the router in router configuration mode.

- You can change the level of routing to be performed by a particular routing instance by using the `is-type` command.

#### Step 3

```bash
lsp-password { hmac-md5 | text } { clear | encrypted } password [ level { 1 | 2 }] [ send-only ] [ snp send-only ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-isis)# lsp-password hmac-md5 clear password1 level 1
```

Configures the LSP authentication password.

- The `hmac-md5` keyword specifies that the password is used in HMAC-MD5 authentication.
- The `text` keyword specifies that the password uses cleartext password authentication.
- The `clear` keyword specifies that the password is unencrypted when entered.
- The `encrypted` keyword specifies that the password is encrypted using a two-way algorithm when entered.
- The `level 1` keyword sets a password for authentication in the area (in Level 1 LSPs and Level SNPs).
- The `level 2` keywords set a password for authentication in the backbone (the Level 2 area).
- The `send-only` keyword adds authentication to LSP and sequence number protocol data units (SNPs) when they are sent. It does not authenticate received LSPs or SNPs.
- The `snp send-only` keyword adds authentication to SNPs when they are sent. It does not authenticate received SNPs.

**Note:** To disable SNP password checking, the `snp send-only` keywords must be specified in the `lsp-password` command.

#### Step 4

```bash
interface type interface-path-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-isis)# interface GigabitEthernet 0/1/0/3
```

Enters interface configuration mode.

#### Step 5

```bash
hello-password { hmac-md5 | text } { clear | encrypted } password [ level { 1 | 2 }] [ send-only ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-isis-if)# hello-password text clear mypassword
```

Configures the authentication password for an IS-IS interface.

#### Step 6

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## Configure Keychains for IS-IS

This task explains how to configure keychains for IS-IS. This task is optional.

Keychains can be configured at the router level (`lsp-password` command) and at the interface level (`hello-password` command) within IS-IS. These commands reference the global keychain configuration and instruct the IS-IS protocol to obtain security parameters from the global set of configured keychains. The router-level configuration (`lsp-password` command) sets the keychain to be used for all IS-IS LSPs generated by this router, as well as for all Sequence Number Protocol Data Units (SN PDUs). The keychain used for HELLO PDUs is set at the interface level, and may be set differently for each interface configured for IS-IS.

### SUMMARY STEPS

1. `configure`
2. `router isis instance-id`
3. `lsp-password keychain keychain-name [ level { 1 | 2 }] [ send-only ] [ snp send-only ]`
4. `interface type interface-path-id`
5. `hello-password keychain keychain-name [ level { 1 | 2 }] [ send-only ]`
6. Use the `commit` or `end` command.

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
router isis instance-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router isis isp
```

Enables IS-IS routing for the specified routing instance, and places the router in router configuration mode.

- You can change the level of routing to be performed by a particular routing instance by using the `is-type` command.

#### Step 3

```bash
lsp-password keychain keychain-name [ level { 1 | 2 }] [ send-only ] [ snp send-only ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-isis)# lsp-password keychain isis_a level 1
```

Configures the keychain.

#### Step 4

```bash
interface type interface-path-id
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-isis)# interface HundredGigE 0/1/0/3
```

Enters interface configuration mode.

#### Step 5

```bash
hello-password keychain keychain-name [ level { 1 | 2 }] [ send-only ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router(config-isis-if)# hello-password keychain isis_b
```

Configures the authentication password for an IS-IS interface.

#### Step 6

Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```