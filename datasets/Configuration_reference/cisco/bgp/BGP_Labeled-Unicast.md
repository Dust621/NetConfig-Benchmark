```markdown
# BGP Labeled-Unicast

When BGP is used to distribute a particular route, it can also be used to distribute a Multiprotocol Label Switching (MPLS) label which is mapped to that route. This feature enables BGP UPDATE message to include MPLS label mapping information about a particular prefix.

## Sample Configuration

```bash
! router bgp 1
  bgp router-id 192.168.70.24
  address-family ipv4 unicast
    redistribute connected route-policy set-lbl-idx
    allocate-label all
  !
  neighbor 172.168.40.24
    remote-as 1
    update-source Loopback0
    address-family ipv4 unicast
      route-policy pass-all in
      route-policy pass-all out
    !
    address-family ipv4 labeled-unicast
      route-policy pass-all in
      route-policy pass-all out
    !
```

The IPv4 unicast address family must be configured in router configuration mode before configuring the IPv4 labeled-unicast address family for a neighbor in neighbor configuration mode.

## Sample Output

```bash
router#sh cef 1.2.2.1
Sat Jun 18 20:07:00.833 UTC
1.2.2.1/32, version 1312, internal 0x5000001 0x0 (ptr 0x8bb7a388) [1], 0x0 (0x8cd0a018), 0xa08 (0x8cbccbd8)
Updated Jun 18 19:56:47.237
Prefix Len 32, traffic index 0, precedence n/a, priority 4
via 2.2.2.2/32, 3 dependencies, recursive [flags 0x6000]
path-idx 0 NHID 0x0 [0x8d37f928 0x0]
recursion-via-/32
next hop 2.2.2.2/32 via 24001/0/21
local label 24053
next hop 12.1.1.1/32 Te0/0/0/12 labels imposed {24006 24004}
next hop 112.1.1.2/32 Te0/0/0/12.1 labels imposed {24006 24004}
```
```