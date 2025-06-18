```markdown
# BGP Additional Paths

The Border Gateway Protocol (BGP) Additional Paths feature modifies the BGP protocol machinery for a BGP speaker to be able to send multiple paths for a prefix. This gives 'path diversity' in the network. The add path enables BGP prefix independent convergence (PIC) at the edge routers.

BGP add path enables add path advertisement in an iBGP network and advertises the following types of paths for a prefix:

- **Backup paths** — to enable fast convergence and connectivity restoration.
- **Group-best paths** — to resolve route oscillation.
- **All paths** — to emulate an iBGP full-mesh.

## Configure BGP Additional Paths

Perform these tasks to configure BGP Additional Paths capability:

### SUMMARY STEPS

1. `configure`
2. `route-policy route-policy-name`
3. `if conditional-expression then action-statement else`
4. `pass endif`
5. `end-policy`
6. `router bgp as-number`
7. `address-family {ipv4 {unicast} | ipv6 {unicast | l2vpn vpls-vpws | vpnv4 unicast | vpnv6 unicast}`
8. `additional-paths receive`
9. `additional-paths send`
10. `additional-paths selection route-policy route-policy-name`
11. Use the `commit` or `end` command.

### DETAILED STEPS

#### Step 1: `configure`

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters configuration mode.

#### Step 2: `route-policy route-policy-name`

Example:
```bash
RP/0/RP0/CPU0:router(config)# route-policy add_path_policy
```
Defines the route policy and enters route-policy configuration mode.

#### Step 3: `if conditional-expression then action-statement else`

Example:
```bash
RP/0/RP0/CPU0:router(config-rpl)# if community matches-any (*) then set path-selection all advertise else
```
Decides the actions and dispositions for the given route.

#### Step 4: `pass endif`

Example:
```bash
RP/0/RP0/CPU0:router(config-rpl-else)# pass
RP/0/RP0/CPU0:router(config-rpl-else)# endif
```
Passes the route for processing and ends the `if` statement.

#### Step 5: `end-policy`

Example:
```bash
RP/0/RP0/CPU0:router(config-rpl)# end-policy
```
Ends the route policy definition and exits route-policy configuration mode.

#### Step 6: `router bgp as-number`

Example:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 100
```
Specifies the autonomous system number and enters BGP configuration mode.

#### Step 7: `address-family {ipv4 {unicast} | ipv6 {unicast | l2vpn vpls-vpws | vpnv4 unicast | vpnv6 unicast}`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 unicast
```
Specifies the address family and enters address family configuration submode.

#### Step 8: `additional-paths receive`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-af)# additional-paths receive
```
Configures receive capability of multiple paths for a prefix to capable peers.

#### Step 9: `additional-paths send`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-af)# additional-paths send
```
Configures send capability of multiple paths for a prefix to capable peers.

#### Step 10: `additional-paths selection route-policy route-policy-name`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-af)# additional-paths selection route-policy add_path_policy
```
Configures additional paths selection capability for a prefix.

#### Step 11: Use the `commit` or `end` command

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the changes.
  - **Cancel** — Remains in the configuration session without committing the changes.
```