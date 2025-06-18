```markdown
# BFD over Bundle and BFD over Logical Bundle

Link Aggregation Control Protocol (LACP) allows a network device to negotiate an automatic bundling of links by sending LACP packets to their directly connected peer. LACP provides a keep-alive mechanism for the link members. While the default keep-alive is 30s, it is configurable to up to 1s. LACP can detect failures on a per-physical-member link. However, the LACP timers do not fulfill the criteria of current fast convergence requirements.

## Differences between BFD over Bundle and BFD over Logical Bundle

### BFD over Bundle (BoB) (RFC 7130)

- Has a BFD session on each bundle member.
- The client is the bundle manager.
- If a BFD session goes down on a specific member link, the whole bundle interface goes down. That is, when the member link goes down, the number of available links falls below the required minimum. Hence the routing session is brought down.

### BFD over Logical Bundle (BLB) (RFC 5880)

- Treats a bundle interface with all its members as a single interface.
- BLB is a multipath (MP) single-hop session.
- If BLB is configured on a bundle, there is only one single BFD session that is active. This implies that only one bundle member is being monitored by BFD at any given time.
- The client is one of the routing protocols.
- When BFD detects a failure, the client brings down the routing session.

## Configuration Modes (BoB or BLB)

The mode (BoB or BLB) is determined by how you configure BFD:

- You can enable BoB by configuring BFD under a Bundle-Ether interface.
- You can enable BLB by configuring BFD under a Bundle-Ether interface on a routing client.

## Additional Notes on LACP

Link Aggregation Control Protocol (LACP) allows a network device to negotiate an automatic bundling of links by sending LACP packets to their directly connected peer. LACP provides a keep-alive mechanism for the link members. While the default keep-alive is 30s, it is configurable to up to 1s. LACP can detect failures on a per-physical-member link. However, the LACP timers do not fulfill the criteria of current fast convergence requirements.
```