```markdown
# BGP Best-External Path

The best–external path functionality supports advertisement of the best–external path to the iBGP and Route Reflector peers when a locally selected bestpath is from an internal peer. BGP selects one best path and one backup path to every destination. By default, it selects one best path. Additionally, BGP selects another bestpath from among the remaining external paths for a prefix. Only a single path is chosen as the best–external path and is sent to other PEs as the backup path. BGP calculates the best–external path only when the best path is an iBGP path. If the best path is an eBGP path, then best–external path calculation is not required.

## Procedure to Determine the Best–External Path

The procedure to determine the best–external path is as follows:

1. Determine the best path from the entire set of paths available for a prefix.

2. Eliminate the current best path.

3. Eliminate all the internal paths for the prefix.

4. From the remaining paths, eliminate all the paths that have the same next hop as that of the current best path.

5. Rerun the best path algorithm on the remaining set of paths to determine the best–external path.

BGP considers the external and confederations BGP paths for a prefix to calculate the best–external path. BGP advertises the best path and the best–external path as follows:

- **On the primary PE**: Advertises the best path for a prefix to both its internal and external peers.
- **On the backup PE**: Advertises the best path selected for a prefix to the external peers and advertises the best–external path selected for that prefix to the internal peers.

## Configure Best-External Path Advertisement

Perform the following tasks to advertise the best–external path to the iBGP and route-reflector peers:

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. Do one of the following:
   - `address-family { vpnv4 unicast | vpnv6 unicast }`
   - `vrf vrf-name {ipv4 unicast | ipv6 unicast}`
4. `advertise best-external`
5. Use the `commit` or `end` command.

### DETAILED STEPS

#### Step 1: `configure`

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters configuration mode.

#### Step 2: `router bgp as-number`

Example:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 100
```
Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

#### Step 3: Do one of the following

- `address-family { vpnv4 unicast | vpnv6 unicast }`
- `vrf vrf-name {ipv4 unicast | ipv6 unicast}`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family vpnv4 unicast
```
Specifies the address family or VRF address family and enters the address family or VRF address family configuration submode.

#### Step 4: `advertise best-external`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-af)# advertise best-external
```
Advertises the best–external path to the iBGP and route-reflector peers.

#### Step 5: Use the `commit` or `end` command

- `commit`: Saves the configuration changes and remains within the configuration session.
- `end`: Prompts user to take one of these actions:
  - **Yes**: Saves configuration changes and exits the configuration session.
  - **No**: Exits the configuration session without committing the configuration changes.
  - **Cancel**: Remains in the configuration session, without committing the configuration changes.
```