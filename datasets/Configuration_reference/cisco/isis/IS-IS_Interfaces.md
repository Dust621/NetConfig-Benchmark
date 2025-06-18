```markdown
# IS-IS Interfaces

IS-IS interfaces can be configured as one of the following types:

- **Active** — Advertises connected prefixes and forms adjacencies. This is the default for interfaces.
- **Passive** — Advertises connected prefixes but does not form adjacencies. The `passive` command is used to configure interfaces as passive. Passive interfaces should be used sparingly for important prefixes such as loopback addresses that need to be injected into the IS-IS domain. If many connected prefixes need to be advertised, then the redistribution of connected routes with the appropriate policy should be used instead.
- **Suppressed** — Does not advertise connected prefixes but forms adjacencies. The `suppress` command is used to configure interfaces as suppressed.
- **Shutdown** — Does not advertise connected prefixes and does not form adjacencies. The `shutdown` command is used to disable interfaces without removing the IS-IS configuration.

## Tag IS-IS Interface Routes

This optional task describes how to associate a tag with a connected route of an IS-IS interface.

### SUMMARY STEPS

1. `configure`
2. `router isis instance-id`
3. `address-family { ipv4 | ipv6 } [ unicast ]`
4. `metric-style wide [ transition ] [ level { 1 | 2 }]`
5. `exit`
6. `interface type number`
7. `address-family { ipv4 | ipv6 } [ unicast ]`
8. `tag tag`
9. Use the `commit` or `end` command.
10. `show isis [ ipv4 | ipv6 | afi-all ] [ unicast | safi-all ] route [ detail ]`

### DETAILED STEPS

**Step 1**  
`configure`  

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters mode.

**Step 2**  
`router isis instance-id`  

Example:
```bash
RP/0/RP0/CPU0:router(config)# router isis isp
```
Enables IS-IS routing for the specified routing process, and places the router in router configuration mode. In this example, the IS-IS instance is called `isp`.

**Step 3**  
`address-family { ipv4 | ipv6 } [ unicast ]`  

Example:
```bash
RP/0/RP0/CPU0:router(config-isis)# address-family ipv4 unicast
```
Specifies the IPv4 or IPv6 address family, and enters router address family configuration mode.

**Step 4**  
`metric-style wide [ transition ] [ level { 1 | 2 }]`  

Example:
```bash
RP/0/RP0/CPU0:router(config-isis-af)# metric-style wide level 1
```
Configures a router to generate and accept only wide link metrics in the Level 1 area.

**Step 5**  
`exit`  

Example:
```bash
RP/0/RP0/CPU0:router(config-isis-af)# exit
```
Exits router address family configuration mode, and returns the router to router configuration mode.

**Step 6**  
`interface type number`  

Example:
```bash
RP/0/RP0/CPU0:router(config-isis)# interface HundredGigE 0/1/0/3
```
Enters interface configuration mode.

**Step 7**  
`address-family { ipv4 | ipv6 } [ unicast ]`  

Example:
```bash
RP/0/RP0/CPU0:router(config-isis-if)# address-family ipv4 unicast
```
Specifies the IPv4 or IPv6 address family, and enters address family configuration mode.

**Step 8**  
`tag tag`  

Example:
```bash
RP/0/RP0/CPU0:router(config-isis-if-af)# tag 3
```
Sets the value of the tag to associate with the advertised connected route.

**Step 9**  
Use the `commit` or `end` command.  

- `commit` — Saves the configuration changes and remains within the configuration session.  
- `end` — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  

**Step 10**  
`show isis [ ipv4 | ipv6 | afi-all ] [ unicast | safi-all ] route [ detail ]`  

Example:
```bash
RP/0/RP0/CPU0:router# show isis ipv4 route detail
```
Displays tag information. Verify that all tags are present in the RIB.

## Tagging Routes: Example

The following example shows how to tag routes.

```bash
route-policy isis-tag-55
end-policy
!
route-policy isis-tag-555
if destination in (5.5.5.0/24 eq 24) then
  set tag 555
  pass
else
  drop
endif
end-policy
!
router static
  address-family ipv4 unicast
    0.0.0.0/0 2.6.0.1
    5.5.5.0/24 Null0
!
router isis uut
  net 00.0000.0000.12a5.00
  address-family ipv4 unicast
    metric-style wide
    redistribute static level-1 route-policy isis-tag-555
    spf prefix-priority critical tag 13
    spf prefix-priority high tag 444
    spf prefix-priority medium tag 777
```
```