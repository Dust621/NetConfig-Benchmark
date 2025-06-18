```markdown
# Setting an SPF Interval for Delaying the IS-IS SPF Computations

## Feature History

| Description | Release | Feature Name |
|------------|---------|--------------|
| You can now define a standard algorithm to postpone the IS-IS SPF computations by setting an SPF interval. This reduces the computational load and churn on IGP nodes when multiple temporally close network events trigger multiple SPF computations. This algorithm also reduces the probability and the duration of transient forwarding loops during native IS-IS convergence when the protocol reacts to multiple temporally close events. This feature complies with RFC 8405. This feature introduces the `spf-interval ietf` command. | Release 7.7.1 | Setting SPF interval in IS-IS to postpone the IS-IS SPF computations |

## Overview

You can set an SPF interval in IS-IS to define a standard algorithm to postpone the IS-IS SPF computations. This reduces the computational load and churn on IGP nodes when multiple temporally close network events trigger multiple SPF computations.

This algorithm reduces the probability and the duration of transient forwarding loops during native IS-IS convergence when the protocol reacts to multiple temporally close events.

To do this, you can use the algorithm specified by RFC 8405 to temporarily postpone the IS-IS SPF computation.

This task is optional.

## Setting IETF for Postponing SPF Calculations

### Configuration

1. Enter the Cisco IOS XR configuration mode.

   ```bash
   Router# configure
   ```

2. Enable IS-IS routing for the specified routing instance and place the router in router configuration mode.

   ```bash
   Router(config)# router isis <tag>
   ```

3. Specify the IPv4 or IPv6 address family, and then enter router address family configuration mode.

   ```bash
   Router(config-isis)# address-family {ipv4 | ipv6} unicast
   ```

4. Set the interval type (IETF) for SPF calculations.

   ```bash
   Router(config-isis-af)# spf-interval ietf
   ```

5. Commit the changes.

   ```bash
   Router(config-isis-af)# commit
   ```

### Configuration Example

```bash
Router# configure
Router(config)# router isis isp
Router(config-isis)# address-family ipv4 unicast
Router(config-isis-af)# spf-interval ietf?
initial-wait      Initial delay before running a route calculation [50]
short-wait        Short delay before running a route calculation [200]
long-wait         Long delay before running a route calculation [5000]
learn-interval    Time To Learn interval for running a route calculation [500]
holddown-interval Holddown interval for running a route calculation [10000]
level             Set SPF interval for one level only
Router(config-isis-af)# spf-interval ietf
Router(config-isis-af)# commit
```

### Verification Example

```bash
Router# show run router isis
router isis 1
 net 49.0001.0000.0000.0100.00
 log adjacency changes
 address-family ipv4 unicast
  metric-style wide
  spf-interval ietf
 !
 address-family ipv6 unicast
  metric-style wide
  spf-interval ietf
 !
```

```bash
Router# show isis ipv4 spf-log last 5 detail
IS-IS 1 Level 2 IPv4 Unicast Route Calculation Log
Time Total Trig.
Timestamp               Type (ms) Nodes Count First Trigger LSP    Triggers
------------ ----- ----- ----- ----- -------------------- -----------------------
--- Wed Mar 16 2022 ---
15:31:49.763 FSPF  1    6    3    tb5-r4.00-00          LINKBAD PREFIXBAD
Delay:
101ms (since first trigger)
261177ms (since end of last calculation)
Trigger Link:
tb5-r2.00
Trigger Prefix:
34.1.24.0/24
New LSP Arrivals:
0
SR uloop:
No
Next Wait Interval:
200ms
RIB Batches:
1 (0 critical, 0 high, 0 medium, 1 low)
Timings (ms):
+--Total--+
Real      CPU
SPT Calculation: 1      1
Route Update:    0      0
----- -----
```

## Recommendations

It is recommended to use the default delay values, which are listed in the syntax description. These default parameters are suggested by RFC 8405 and should be appropriate for most networks.

However, you can configure different values if required.

### Example

```bash
Router# configure
Router(config)# router isis isp
Router(config-isis)# address-family ipv4 unicast
Router(config-isis-af)# spf-interval ietf
Router(config-isis-af)# commit
Router(config-isis-af)# spf-interval ietf short-wait 500
Router(config-isis-af)# commit
```
```