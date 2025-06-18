# BGP Prefix Origin Validation using RPKI

A BGP route associates an address prefix with a set of autonomous systems (AS) that identify the interdomain path the prefix has traversed in the form of BGP announcements. This set is represented as the AS_PATH attribute in BGP and starts with the AS that originated the prefix.

To help reduce well-known threats against BGP including prefix mis-announcing and monkey-in-the-middle attacks, one of the security requirements is the ability to validate the origination AS of BGP routes. The AS number claiming to originate an address prefix (as derived from the AS_PATH attribute of the BGP route) needs to be verified and authorized by the prefix holder.

The Resource Public Key Infrastructure (RPKI) is an approach to build a formally verifiable database of IP addresses and AS numbers as resources. The RPKI is a globally distributed database containing, among other things, information mapping BGP (internet) prefixes to their authorized origin-AS numbers. Routers running BGP can connect to the RPKI to validate the origin-AS of BGP paths.

## Configure RPKI Cache-server

Perform this task to configure Resource Public Key Infrastructure (RPKI) cache-server parameters.

Configure the RPKI cache-server parameters in `rpki-server` configuration mode. Use the `rpki server` command in router BGP configuration mode to enter into the `rpki-server` configuration mode.

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `rpki cache {host-name | ip-address}`
4. Use one of these commands:
   - `transport ssh port port_number`
   - `transport tcp port port_number`
5. (Optional) `username user_name`
6. (Optional) `password`
7. `preference preference_value`
8. `purge-time time`
9. Use one of these commands:
   - `refresh-time time`
   - `refresh-time off`
10. Use one of these commands:
    - `response-time time`
    - `response-time off`
11. `shutdown`
12. Use the `commit` or `end` command.

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
RP/0/RP0/CPU0:router(config)#router bgp 100
```
Specifies the BGP AS number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

**Step 3** `rpki cache {host-name | ip-address}`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)#rpki server 10.2.3.4
```
Enters `rpki-server` configuration mode and enables configuration of RPKI cache parameters.

**Step 4** Use one of these commands:
- `transport ssh port port_number`
- `transport tcp port port_number`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#transport ssh port 22
```
Or
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#transport tcp port 2
```
Specifies a transport method for the RPKI cache:
- `ssh`—Select `ssh` to connect to the RPKI cache using SSH.
- `tcp`—Select `tcp` to connect to the RPKI cache using TCP (unencrypted).
- `port port_number`—Specify the port number for the RPKI cache transport over TCP and SSH protocols. The port number ranges from 1 to 65535.
  - SSH supports custom ports in addition to the default port number 22.

**Note:** You can set the transport to either TCP or SSH. Change of transport causes the cache session to flap.

**Step 5** (Optional) `username user_name`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#username ssh_rpki_cache
```
Specifies a (SSH) username for the RPKI cache-server.

**Step 6** (Optional) `password`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#password ssh_rpki_pass
```
Specifies a (SSH) password for the RPKI cache-server.

**Note:** The "username" and "password" configurations only apply if the SSH method of transport is active.

**Step 7** `preference preference_value`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#preference 1
```
Specifies a preference value for the RPKI cache. Range for the preference value is 1 to 10. Setting a lower preference value is better.

**Step 8** `purge-time time`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#purge-time 30
```
Configures the time BGP waits to keep routes from a cache after the cache session drops. Set purge time in seconds. Range for the purge time is 30 to 360 seconds.

**Step 9** Use one of these commands:
- `refresh-time time`
- `refresh-time off`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#refresh-time 20
```
Or
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#refresh-time off
```
Configures the time BGP waits in between sending periodic serial queries to the cache. Set refresh-time in seconds. Range for the refresh time is 15 to 3600 seconds.

Configure the `off` option to specify not to send serial-queries periodically.

**Step 10** Use one of these commands:
- `response-time time`
- `response-time off`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#response-time 30
```
Or
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#response-time off
```
Configures the time BGP waits for a response after sending a serial or reset query. Set response-time in seconds. Range for the response time is 15 to 3600 seconds.

Configure the `off` option to wait indefinitely for a response.

**Step 11** `shutdown`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp-rpki-server)#shutdown
```
Configures shut down of the RPKI cache.

**Step 12** Use the `commit` or `end` command.

- `commit` —Saves the configuration changes and remains within the configuration session.
- `end` —Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` —Exits the configuration session without committing the configuration changes.
  - `Cancel` —Remains in the configuration session, without committing the configuration changes.

## Configure RPKI Prefix Validation

Perform this task to control the behavior of RPKI prefix validation processing.

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. Use one of these commands:
   - `rpki origin-as validation disable`
   - `rpki origin-as validation time {off | prefix_validation_time}`
4. `origin-as validity signal ibgp`
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
RP/0/RP0/CPU0:router(config)#router bgp 100
```
Specifies the BGP AS number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

**Step 3** Use one of these commands:
- `rpki origin-as validation disable`
- `rpki origin-as validation time {off | prefix_validation_time}`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)#rpki origin-as validation disable
```
Or
```bash
RP/0/RP0/CPU0:router(config-bgp)#rpki origin-as validation time 50
```
Or
```bash
RP/0/RP0/CPU0:router(config-bgp)#rpki origin-as validation time off
```
Sets the BGP origin-AS validation parameters:
- `disable`—Use `disable` option to disable RPKI origin-AS validation.
- `time`—Use `time` option to either set prefix validation time (in seconds) or to set `off` the automatic prefix validation after an RPKI update.
  - Range for prefix validation time is 5 to 60 seconds.

Configuring the `disable` option disables prefix validation for all eBGP paths and all eBGP paths are marked as "valid" by default.

**Note:** The `rpki origin-as validation` options can also be configured in neighbor and neighbor address family submodes. The neighbor must be an eBGP neighbor. If configured at the neighbor or neighbor address family level, prefix validation disable or time options will be valid only for that specific neighbor or neighbor address family.

**Step 4** `origin-as validity signal ibgp`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)#rpki origin-as validity signal ibgp
```
Enables the iBGP signaling of validity state through an extended-community.

This can also be configured in global address family submode.

**Step 5** Use the `commit` or `end` command.

- `commit` —Saves the configuration changes and remains within the configuration session.
- `end` —Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` —Exits the configuration session without committing the configuration changes.
  - `Cancel` —Remains in the configuration session, without committing the configuration changes.

## Configure BGP Prefix Validation

Starting from Release 6.5.1, RPKI is disabled by default. From Release 6.5.1, use the following task to configure RPKI Prefix Validation.

```bash
Router(config)# router bgp 100 /* The bgp origin-as validation time and bgp origin-as validity signal ibgp commands are optional. */
Router(config-bgp)# bgp origin-as validation time 50
Router(config-bgp)# bgp origin-as validation time off
Router(config-bgp)# bgp origin-as validation signal ibgp
Router(config-bgp)# address-family ipv4 unicast
Router(config-bgp-af)# bgp origin-as validation enable
```

Use the following commands to verify the origin-as validation configuration:

```bash
Router# show bgp origin-as validity
```
Output:
```
Thu Mar 14 04:18:09.656 PDT
BGP router identifier 10.1.1.1, local AS number 1
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000
RD version: 514
BGP main routing table version 514
BGP NSR Initial initsync version 2 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs
Status codes: s suppressed, d damped, h history, * valid, > best
i - internal, r RIB-failure, S stale, N Nexthop-discard
Origin codes: i - IGP, e - EGP, ? - incomplete
Origin-AS validation codes: V valid, I invalid, N not-found, D disabled
Network          Next Hop          Metric LocPrf Weight Path
*> 209.165.200.223/27 0.0.0.0            0         32768 ?
*> 209.165.200.225/27 0.0.0.0            0         32768 ?
*> 19.1.2.0/24        0.0.0.0            0         32768 ?
*> 19.1.3.0/24        0.0.0.0            0         32768 ?
*> 10.1.2.0/24        0.0.0.0            0         32768 ?
*> 10.1.3.0/24        0.0.0.0            0         32768 ?
*> 10.1.4.0/24        0.0.0.0            0         32768 ?
*> 198.51.100.1/24    0.0.0.0            0         32768 ?
*> 203.0.113.235/24   0.0.0.0            0         32768 ?
V*> 209.165.201.0/27  10.1.2.1           0 4002 i
N*> 198.51.100.2/24   10.1.2.1           0 4002 i
I*> 198.51.100.1/24   10.1.2.1           0 4002 i
*> 192.0.2.1.0/24     0.0.0.0            0         32768 ?
```

```bash
Router# show bgp process Mon Jul 9 16:47:39.428 PDT
```
Output:
```
BGP Process Information:
...
Use origin-AS validity in bestpath decisions
Allow (origin-AS) INVALID paths
Signal origin-AS validity state to neighbors

Address family: IPv4 Unicast
...
Origin-AS validation is enabled for this address-family
Use origin-AS validity in bestpath decisions for this address-family
Allow (origin-AS) INVALID paths for this address-family
Signal origin-AS validity state to neighbors with this address-family
```

## Configure RPKI Bestpath Computation

Perform this task to configure RPKI bestpath computation options.

### SUMMARY STEPS

1. `configure`
2. `router bgp as-number`
3. `rpki bestpath use origin-as validity`
4. `rpki bestpath origin-as allow invalid`
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
RP/0/RP0/CPU0:router(config)#router bgp 100
```
Specifies the BGP AS number and enters the BGP configuration mode, allowing you to configure the BGP routing process.

**Step 3** `rpki bestpath use origin-as validity`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)#rpki bestpath use origin-as validity
```
Enables the validity states of BGP paths to affect the path's preference in the BGP bestpath process. This configuration can also be done in router BGP address family submode.

**Step 4** `rpki bestpath origin-as allow invalid`

Example:
```bash
RP/0/RP0/CPU0:router(config-bgp)#rpki bestpath origin-as allow invalid
```
Allows all "invalid" paths to be considered for BGP bestpath computation.

This configuration can also be done at global address family, neighbor, and neighbor address family submodes. Configuring `rpki bestpath origin-as allow invalid` in router BGP and address family submodes allow all "invalid" paths to be considered for BGP bestpath computation. By default, all such paths are not bestpath candidates. Configuring `pki bestpath origin-as allow invalid` in neighbor and neighbor address family submodes allow all "invalid" paths from that specific neighbor or neighbor address family to be considered as bestpath candidates. The neighbor must be an eBGP neighbor.

**Note:** This configuration takes effect only when the `rpki bestpath use origin-as validity` configuration is enabled.

**Step 5** Use the `commit` or `end` command.

- `commit` —Saves the configuration changes and remains within the configuration session.
- `end` —Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` —Exits the configuration session without committing the configuration changes.
  - `Cancel` —Remains in the configuration session, without committing the configuration changes.