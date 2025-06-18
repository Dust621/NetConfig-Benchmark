```markdown
# BGP Cost Community

The BGP cost community is a nontransitive extended community attribute that is passed to internal BGP (iBGP) and confederation peers but not to external BGP (eBGP) peers. The cost community feature allows you to customize the local route preference and influence the best-path selection process by assigning cost values to specific routes. The extended community format defines generic points of insertion (POI) that influence the best-path decision at different points in the best-path algorithm.

**BGP Cost Community Reference**, on page 18 provides additional conceptual details on BGP cost community.

## Configure BGP Cost Community

BGP receives multiple paths to the same destination and it uses the best-path algorithm to decide which is the best path to install in RIB. To enable users to determine an exit point after partial comparison, the cost community is defined to tie-break equal paths during the best-path selection process. Perform this task to configure the BGP cost community.

### SUMMARY STEPS

1. configure  
2. route-policy name  
3. set extcommunity cost { cost-extcommunity-set-name | cost-inline-extcommunity-set } [ additive ]  
4. end-policy  
5. router bgp as-number  
6. Do one of the following:  
   - default-information originate  
   - aggregate-address address/mask-length [ as-set ] [ as-confed-set ] [ summary-only ] [ route-policy route-policy-name ]  
   - redistribute connected [ metric metric-value ] [ route-policy route-policy-name ]  
   - process-id [ match { external | internal }] [ metric metric-value ] [ route-policy route-policy-name ]  
   - redistribute isis process-id [ level { 1 | 1-inter-area | 2 }] [ metric metric-value ] [ route-policy route-policy-name ]  
   - redistribute ospf process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]  

7. Do one of the following:  
   - redistribute ospfv3 process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]  
   - redistribute rip [ metric metric-value ] [ route-policy route-policy-name ]  
   - redistribute static [ metric metric-value ] [ route-policy route-policy-name ]  
   - network { ip-address/prefix-length | ip-address mask } [ route-policy route-policy-name ]  
   - neighbor ip-address remote-as as-number  
   - route-policy route-policy-name { in | out }  

8. Use the commit or end command.  
9. show bgp ip-address  

### DETAILED STEPS

#### Step 1 configure

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2 route-policy name

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# route-policy costA
```

Enters route policy configuration mode and specifies the name of the route policy to be configured.

#### Step 3 set extcommunity cost { cost-extcommunity-set-name | cost-inline-extcommunity-set } [ additive ]

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# set extcommunity cost cost_A
```

Specifies the BGP extended community attribute for cost.

#### Step 4 end-policy

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# end-policy
```

Ends the definition of a route policy and exits route policy configuration mode.

#### Step 5 router bgp as-number

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Enters BGP configuration mode allowing you to configure the BGP routing process.

#### Step 6 Do one of the following:

- default-information originate  
- aggregate-address address/mask-length [ as-set ] [ as-confed-set ] [ summary-only ] [ route-policy route-policy-name ]  
- redistribute connected [ metric metric-value ] [ route-policy route-policy-name ]  
- process-id [ match { external | internal }] [ metric metric-value ] [ route-policy route-policy-name ]  
- redistribute isis process-id [ level { 1 | 1-inter-area | 2 }] [ metric metric-value ] [ route-policy route-policy-name ]  
- redistribute ospf process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]  

Applies the cost community to the attach point (route policy).

#### Step 7 Do one of the following:

- redistribute ospfv3 process-id [ match { external [ 1 | 2 ] | internal | nssa-external [ 1 | 2 ]}] [ metric metric-value ] [ route-policy route-policy-name ]  
- redistribute rip [ metric metric-value ] [ route-policy route-policy-name ]  
- redistribute static [ metric metric-value ] [ route-policy route-policy-name ]  
- network { ip-address/prefix-length | ip-address mask } [ route-policy route-policy-name ]  
- neighbor ip-address remote-as as-number  
- route-policy route-policy-name { in | out }  

#### Step 8 Use the commit or end command.

- **commit** — Saves the configuration changes and remains within the configuration session.  
- **end** — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  

#### Step 9 show bgp ip-address

**Example:**

```bash
RP/0/RP0/CPU0:router# show bgp 172.168.40.24
```

Displays the cost community in the following format:  
`Cost: POI : cost-community-ID : cost-number`

## Configure BGP Community and Extended-Community Advertisements

Perform this task to specify that community/extended-community attributes should be sent to an eBGP neighbor. These attributes are not sent to an eBGP neighbor by default. By contrast, they are always sent to iBGP neighbors. This section provides examples on how to enable sending community attributes. The `send-community-ebgp` keyword can be replaced by the `send-extended-community-ebgp` keyword to enable sending extended-communities.

If the `send-community-ebgp` command is configured for a neighbor group or address family group, all neighbors using the group inherit the configuration. Configuring the command specifically for a neighbor overrides inherited values.

> **Note**  
> BGP community and extended-community filtering cannot be configured for iBGP neighbors. Communities and extended-communities are always sent to iBGP neighbors under VPNv4, MDT, IPv4, and IPv6 address families.

### SUMMARY STEPS

1. configure  
2. router bgp as-number  
3. neighbor ip-address  
4. remote-as as-number  
5. address-family {ipv4 {labeled-unicast | unicast | mdt | mvpn | rt-filter | tunnel} | ipv6 {labeled-unicast | mvpn | unicast}}  
6. Use one of these commands:  
   - send-community-ebgp  
   - send-extended-community-ebgp  
7. Use the commit or end command.  

### DETAILED STEPS

#### Step 1 configure

**Example:**

```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2 router bgp as-number

**Example:**

```bash
RP/0/RP0/CPU0:router(config)# router bgp 120
```

Specifies the autonomous system number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

#### Step 3 neighbor ip-address

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp)# neighbor 172.168.40.24
```

Places the router in neighbor configuration mode for BGP routing and configures the neighbor IP address as a BGP peer.

#### Step 4 remote-as as-number

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# remote-as 2002
```

Creates a neighbor and assigns a remote autonomous system number to it.

#### Step 5 address-family {ipv4 {labeled-unicast | unicast | mdt | mvpn | rt-filter | tunnel} | ipv6 {labeled-unicast | mvpn | unicast}}

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr)# address-family ipv6 unicast
```

Enters neighbor address family configuration mode for the specified address family. Use either `ipv4` or `ipv6` address family keyword with one of the specified address family sub mode identifiers.

**IPv6 address family mode supports these sub modes:**  
- labeled-unicast  
- mvpn  
- unicast  

**IPv4 address family mode supports these sub modes:**  
- labeled-unicast  
- mdt  
- mvpn  
- rt-filter  
- tunnel  
- unicast  

#### Step 6 Use one of these commands:

- send-community-ebgp  
- send-extended-community-ebgp  

**Example:**

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# send-community-ebgp
```

or

```bash
RP/0/RP0/CPU0:router(config-bgp-nbr-af)# send-extended-community-ebgp
```

Specifies that the router send community attributes or extended community attributes (which are disabled by default for eBGP neighbors) to a specified eBGP neighbor.

#### Step 7 Use the commit or end command.

- **commit** — Saves the configuration changes and remains within the configuration session.  
- **end** — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  
```