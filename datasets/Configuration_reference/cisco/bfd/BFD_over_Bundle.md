# BFD over Bundle

BFD over Bundle feature enables BFD sessions to monitor the status of individual bundle member links. BFD notifies the bundle manager immediately when one of the member links goes down, and reduces the bandwidth used by the bundle.

## Restrictions

The following are the restrictions in using BFD over Bundle feature:

- It is only supported in IETF mode.
- It is not supported on routing protocols, such as OSPF, ISIS, and BGP.
- When BFD timer is configured to 3.3 ms, which is the most aggressive timer, 256 sessions can be brought up.
- If BFD timer is configured to greater than 100 ms, 300 BFD sessions can be brought up simultaneously.
- BFD echo mode and encryption is not supported.
- BFD dampening is not supported.

## Configure BFD over Bundle

Configuring BFD over bundle involves the following steps:

- Enable and Disable IPv6 checksum calculations for BFD on a router.
- Specify the mode, BFD packet transmission intervals, and failure detection times on a bundle.

Repeat the same configuration steps in the destination router.

### Note

```bash
/* Enable and Disable IPv6 checksum calculations for BFD on a router. */
Router(config-if)# bfd
Router(config-bfd-if)# ipv6 checksum disable
Router(config-bfd-if)# dampening disable
Router(config-bfd-if)# commit

/* Specify the mode, BFD packet transmission intervals, and failure detection times on a bundle */
Router(config)# interface Bundle-Ether 3739
Router(config-if)# bfd mode ietf
Router(config-if)# bfd address-family ipv4 multiplier 3
Router(config-if)# bfd address-family ipv4 destination 10.23.1.2
Router(config-if)# bfd address-family ipv4 fast-detect
Router(config-if)# bfd address-family ipv4 minimum-interval 100
Router(config-if)# bfd address-family ipv6 multiplier 3
Router(config-if)# bfd address-family ipv6 destination 2001:DB8:1::2
Router(config-if)# bfd address-family ipv6 fast-detect
Router(config-if)# bfd address-family ipv6 minimum-interval 100
Router(config-if)# ipv4 address 10.23.1.1 255.255.255.252
Router(config-if)# ipv6 address 2001:DB8:1::2/120
Router(config-if)# load-interval 30
Router(config-if)# commit

Router(config)# interface TenGigE 0/0/0/0
Router(config-if)# bundle id 3739 mode active
```

## Running Configuration

```bash
bfd
ipv6 checksum disable
dampening disable
!
interface Bundle-Ether3739
bfd mode ietf
bfd address-family ipv4 multiplier 3
bfd address-family ipv4 destination 10.23.1.2
bfd address-family ipv4 fast-detect
bfd address-family ipv4 minimum-interval 100
bfd address-family ipv6 multiplier 3
bfd address-family ipv6 destination 2001:DB8:1::2
bfd address-family ipv6 fast-detect
bfd address-family ipv6 minimum-interval 100
ipv4 address 10.23.1.1 255.255.255.252
ipv6 address 2001:DB8:1::2/120
load-interval 30
!
interface TenGigE 0/0/0/0
bundle id 3739 mode active
```

## Verification

The following show command outputs displays the status of BFD sessions on bundle members:

```bash
/* Verify the details of the IPv4 BFD session in the source router. */
Router# show bfd session
Interface        Dest Addr       Local det time(int*mult)      State       Echo        Async       H/W        NPU
---------        ---------       ---------                    ------      -----       -----       ---        ---
Te0/0/0/0        10.23.1.2       0s(0s*0)                    300ms(100ms*3) UP        Yes         0/RP0/CPU0
BE3739           10.23.1.2       n/a                         n/a          UP          No          n/a

/* Verify the details of the IPv4 BFD session in the destination router. */
Router# show bfd session
Interface        Dest Addr       Local det time(int*mult)      State       Echo        Async       H/W        NPU
----------       -----------     ---------                    -------     -----       -----       ---        ---
Te0/6/0/0        10.23.1.1       0s(0s*0)                    300ms(100ms*3) UP        No          n/a
BE3739           10.23.1.1       n/a                         n/a          UP          No          n/a

/* Verify the details of the IPv6 BFD session in the source router. */
Router# show bfd ipv6 session
Interface        Dest Addr       Local det time(int*mult)      State       H/W        NPU        Echo        Async
----------       -----------     ---------                    -------     ---        ---        ----        ----
Te0/0/0/0        10:23:1::2      Yes                         0/RP0/0s (0s*0) 00ms(100ms*3) UP        ------      ----
BE3739           10:23:1::2      No                          n/a          n/a        n/a        UP

/* Verify the details of the IPv6 BFD session in the destination router. */
Router# show bfd ipv6 session
Interface        Dest Addr       Local det time(int*mult)      State       H/W        NPU        Echo        Async
----------       -----------     ---------                    -------     ---        ---        ----        ----
Te0/6/0/0        10:23:1::1      No                          n/a         0s(0s*0)   300ms(100ms*3) UP
BE3739           10:23:1::1      No                          n/a         n/a        n/a        UP
```