```markdown
# Route Dampening

Route dampening is a BGP feature that minimizes the propagation of flapping routes across an internetwork. A route is considered to be flapping when it is repeatedly available, then unavailable, then available, then unavailable, and so on.

For example, consider a network with three BGP autonomous systems: autonomous system 1, autonomous system 2, and autonomous system 3. Suppose the route to network A in autonomous system 1 flaps (it becomes unavailable). Under circumstances without route dampening, the eBGP neighbor of autonomous system 1 to autonomous system 2 sends a withdraw message to autonomous system 2. The border router in autonomous system 2, in turn, propagates the withdrawal message to autonomous system 3. When the route to network A reappears, autonomous system 1 sends an advertisement message to autonomous system 2, which sends it to autonomous system 3. If the route to network A repeatedly becomes unavailable, then available, many withdrawal and advertisement messages are sent. Route flapping is a problem in an internetwork connected to the Internet, because a route flap in the Internet backbone usually involves many routes.

The route dampening feature minimizes the flapping problem as follows. Suppose again that the route to network A flaps. The router in autonomous system 2 (in which route dampening is enabled) assigns network A a penalty of 1000 and moves it to history state. The router in autonomous system 2 continues to advertise the status of the route to neighbors. The penalties are cumulative. When the route flaps so often that the penalty exceeds a configurable suppression limit, the router stops advertising the route to network A, regardless of how many times it flaps. Thus, the route is dampened.

The penalty placed on network A is decayed until the reuse limit is reached, upon which the route is once again advertised. At half of the reuse limit, the dampening information for the route to network A is removed.

No penalty is applied to a BGP peer reset when route dampening is enabled, even though the reset withdraws the route.

## Configuring BGP Route Dampening

Perform this task to configure and monitor BGP route dampening.

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `address-family { ipv4 | ipv6 } unicast`
4. `bgp dampening [ half-life [ reuse suppress max-suppress-time ] | route-policy route-policy-name ]`
5. Use the `commit` or `end` command.

### DETAILED STEPS

#### Step 1: `configure`

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters mode.

#### Step 2: `router bgp as-number`

Example:
```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```
Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

#### Step 3: `address-family { ipv4 | ipv6 } unicast`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)# address-family ipv4 unicast
```
Specifies either the IPv4 or IPv6 address family and enters address family configuration submode.

To see a list of all the possible keywords and arguments for this command, use the CLI help (`?`).

#### Step 4: `bgp dampening [ half-life [ reuse suppress max-suppress-time ] | route-policy route-policy-name ]`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-af)# bgp dampening 30 1500 10000 120
```
Configures BGP dampening for the specified address family.

#### Step 5: Use the `commit` or `end` command.

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.
```