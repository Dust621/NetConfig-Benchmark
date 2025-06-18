```markdown
# Verify RIB Configuration Using Routing Table

Perform this task to verify the RIB configuration to ensure that RIB is running on the RP and functioning properly by checking the routing table summary and details.

## SUMMARY STEPS

1. `show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] summary [ detail ] [ standby ]`
2. `show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] [ protocol [ instance ] | ip-address mask ] [ standby ] [ detail ]`

## DETAILED STEPS

### Step 1

```bash
show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] summary [ detail ] [ standby ]
RP/0/RP0/CPU0:router# show route summary
```

Displays route summary information about the specified routing table.

- The default table summarized is the IPv4 unicast routing table.

### Step 2

```bash
show route [ vrf { vrf-name | all }] [ afi-all | ipv4 | ipv6 ] [ unicast | safi-all ] [ protocol [ instance ] | ip-address mask ] [ standby ] [ detail ]
```

Example:

```bash
RP/0/RP0/CPU0:router# show route ipv4 unicast
```

Displays more detailed route information about the specified routing table.

- This command is usually issued with an IP address or other optional filters to limit its display. Otherwise, it displays all routes from the default IPv4 unicast routing table, which can result in an extensive list, depending on the configuration of the network.

## Output of `show route best-local` Command: Example

The following is sample output from the `show route backup` command:

```bash
show route backup
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
O - OSPF, IA - OSPF inter area
N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
U - per-user static route, o - ODR, L - local

S 172.73.51.0/24 is directly connected, 2d20h, HundredGigE 4/0/0/1
Backup O E2 [110/1] via 10.12.12.2, HundredGigE 3/0/0/1
```
```