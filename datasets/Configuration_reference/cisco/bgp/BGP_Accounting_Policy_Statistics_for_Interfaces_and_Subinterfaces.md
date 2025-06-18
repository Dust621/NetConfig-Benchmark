```markdown
# BGP Accounting Policy Statistics for Interfaces and Subinterfaces

## Table 6: Feature History Table

| Description | Release | Feature Name |
|-------------|---------|--------------|
| Border Gateway Protocol (BGP) policy accounting measures and classifies IP traffic that is received from different peers. You can identify and account for all traffic by customer and bill accordingly. | Release 7.9.1 | BGP Accounting Policy Statistics for Interfaces and Subinterfaces |

Policy accounting is enabled on an individual input interface basis. Using BGP policy accounting, you can now account for traffic according to the route it traverses.

This feature is supported on routers that have the Cisco NC57 based line cards with external TCAM (eTCAM) and operate in native mode.

This feature introduces the `hw-module fib bgppa stats-mode` command.

IP traffic received from various peers is measured and categorised using Border Gateway Protocol (BGP) policy accounting. All traffic can be tracked down, accounted for, and billed individually for. On an individual input interface basis, policy accounting is enabled. Now that traffic can be accounted for based on the route it takes, BGP policy accounting is available.

This feature introduces the `hw-module fib bgppa stats-mode` command. After configuring the command, you must reload the router for the feature to take effect.

## Restriction

- This feature is applicable for the following address families:
  - IPv4
  - IPv6

- This feature supports input destination-based accounting only.

## Configuration

### For main interface:

```bash
Router# config
Router(config)# hw-module fib bgppa stats-mode main-intf
Router(config)# commit
```

### For sub interface:

```bash
Router# config
Router(config)# hw-module fib bgppa stats-mode sub-intf
Router(config)# commit
```

After configuring the command, you must reload the router for the feature to take effect.

**Note**

## Running Configuration

### For main interface:

```bash
hw-module fib bgppa stats-mode main-intf !
```

### For sub interface:

```bash
hw-module fib bgppa stats-mode sub-intf !
```

## Verification

The `show` output displays that the BGP policy accounting is configured.

```bash
Router#show ipv4 int bundle-ether 54
Bundle-Ether54 is Up, ipv4 protocol is Up
Vrf is default (vrfid 0x60000000)
Internet address is 54.1.1.2/24
MTU is 1514 (1500 is available to IP)
Helper address is not set
Directed broadcast forwarding is disabled
Outgoing access list is not set
Inbound common access list is not set, access list is not set
Proxy ARP is disabled
ICMP redirects are never sent
ICMP unreachables are always sent
ICMP mask replies are never sent
Table Id is 0xe0000000
IP Input BGP policy accounting is configured
```

The following example shows the statistic details.

### For IPv4:

```bash
Router#show cef ipv4 interface bundle-ether 22 bgp-policy-statistics
Bundle-Ether22 is UP
Input BGP policy accounting on dst IP address enabled
buckets      packets      bytes
default      207598474    309736310837
1            4946185      7379708020
2            2471450      3687403400
3            2472189      3688505988
4            2472271      3688628332
5            2468753      3683379476
6            2468877      3683564484
7            2472353      3688750676
8            2472434      3688871528
9            2472517      3688995364
10           2468958      3683685336
11           2469081      3683868852
12           2472599      3689117708
13           2467559      3681598028
14           2467682      3681781544
15           2472680      3689238560
```

### For IPv6:

```bash
Router#show cef ipv6 interface hundredGigE 0/7/0/26 bgp-policy-statistics
HundredGigE0/7/0/26 is UP
Input BGP policy accounting on dst IP address enabled
buckets      packets      bytes
default      275658703    412385419688
1            166908       249694368
2            83455        124848680
3            83455        124848680
4            83455        124848680
5            83456        124850176
6            83456        124850176
7            83456        124850176
8            83456        124850176
9            83457        124851672
10           83457        124851672
11           83457        124851672
12           83458        124853168
13           83458        124853168
14           83458        124853168
15           83459        124854664
```
```