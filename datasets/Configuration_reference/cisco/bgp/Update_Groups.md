```markdown
# Update Groups

The BGP Update Groups feature contains an algorithm that dynamically calculates and optimizes update groups of neighbors that share outbound policies and can share the update messages. The BGP Update Groups feature separates update group replication from peer group configuration, improving convergence time and flexibility of neighbor configuration.

## Monitor BGP Update Groups

This task displays information related to the processing of BGP update groups.

## SUMMARY STEPS

1. `show bgp [ ipv4 { unicast | multicast | all | tunnel } | ipv6 { unicast | all } | all { unicast | multicast | all labeled-unicast | tunnel } | vpnv4 unicast | vrf { vrf-name | all } [ ipv4 unicast ipv6 unicast ] | vpvn6 unicast ] update-group [ neighbor ip-address | process-id.index [ summary | performance-statistics ]]`

## DETAILED STEPS

```bash
show bgp [ ipv4 { unicast | multicast | all | tunnel } | ipv6 { unicast | all } | all { unicast | multicast | all labeled-unicast | tunnel } | vpnv4 unicast | vrf { vrf-name | all } [ ipv4 unicast ipv6 unicast ] | vpvn6 unicast ] update-group [ neighbor ip-address | process-id.index [ summary | performance-statistics ]]
```

### Example:

```bash
RP/0/RP0/CPU0:router# show bgp update-group 0.0
```

Displays information about BGP update groups.

- The `ip-address` argument displays the update groups to which that neighbor belongs.
  
- The `process-id.index` argument selects a particular update group to display and is specified as follows: `process ID (dot) index`. Process ID range is from `0` to `254`. Index range is from `0` to `4294967295`.

- The `summary` keyword displays summary information for neighbors in a particular update group.

- If no argument is specified, this command displays information for all update groups (for the specified address family).

- The `performance-statistics` keyword displays performance statistics for an update group.

## Displaying BGP Update Groups: Example

The following is sample output from the `show bgp update-group` command run in EXEC configuration XR EXEC mode:

```bash
show bgp update-group

Update group for IPv4 Unicast, index 0.1:
  Attributes:
    Outbound Route map:rm
    Minimum advertisement interval:30
    Messages formatted:2, replicated:2
  Neighbors in this update group: 10.0.101.92

Update group for IPv4 Unicast, index 0.2:
  Attributes:
    Minimum advertisement interval:30
    Messages formatted:2, replicated:2
  Neighbors in this update group: 10.0.101.91
```
```