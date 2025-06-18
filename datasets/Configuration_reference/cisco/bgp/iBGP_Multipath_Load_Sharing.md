```markdown
# iBGP Multipath Load Sharing

When a Border Gateway Protocol (BGP) speaking router that has no local policy configured receives multiple network layer reachability information (NLRI) from the internal BGP (iBGP) for the same destination, the router will choose one iBGP path as the best path. The best path is then installed in the IP routing table of the router. The iBGP Multipath Load Sharing feature enables the BGP speaking router to select multiple iBGP paths as the best paths to a destination. The best paths or multipaths are then installed in the IP routing table of the router.

[iBGP Multipath Load Sharing Reference, on page 21](#) provides additional details.

## Configure iBGP Multipath Load Sharing

Perform this task to configure the iBGP Multipath Load Sharing:

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family {ipv4|ipv6} {unicast|multicast}`
4. `maximum-paths ibgp number`
5. Use the `commit` or `end` command.

### DETAILED STEPS

**Step 1** `configure`

Example:

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

**Step 2** `router bgp as-number`

Example:

```bash
RP/0/RP0/CPU0:router(config)# router bgp 100
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

**Step 3** `address-family {ipv4|ipv6} {unicast|multicast}`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 multicast
```

Specifies either the IPv4 or IPv6 address family and enters address family configuration submode.

**Step 4** `maximum-paths ibgp number`

Example:

```bash
RP/0/RP0/CPU0:router(config-bgp-af)# maximum-paths ibgp 30
```

Configures the maximum number of iBGP paths for load sharing.

**Step 5** Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

## iBGP Multipath Loadsharing Configuration: Example

The following is a sample configuration where 30 paths are used for loadsharing:

```bash
router bgp 100
 address-family ipv4 multicast
  maximum-paths ibgp 30
 !
 !
 end
```
```