```markdown
# Restrictions for Implementing Routing Policy

These restrictions apply when working with Routing Policy Language implementation:

## Configuration Requirements

- Border Gateway Protocol (BGP), integrated Intermediate System-to-Intermediate System (IS-IS), or Open Shortest Path First (OSPF) must be configured in your network.

## Policy Definition Limits

- An individual policy definition of up to 1000 statements are supported. The total number of statements within a policy can be extended to 4000 statements using hierarchical policy constructs. However, this limit is restricted with the use of apply statements.

## Policy Modification Restrictions

When a policy that is attached directly or indirectly to an attach point needs to be modified, a single commit operation cannot be performed when:

- Removing a set or policy referred by another policy that is attached to any attach point directly or indirectly.
- Modifying the policy to remove the reference to the same set or policy that is getting removed.

The commit must be performed in two steps:

1. Modify the policy to remove the reference to the policy or set and then commit.
2. Remove the policy or set and commit.

## Network Limitations

- Per-vrf label mode is not supported for Carrier Supporting Carrier (CSC) network with internal and external BGP multipath setup.

## IPv6 Next Hop Restrictions

- You cannot change the next hop address to an IPv6 address through RPL policy for a route that starts from an IPv4 peer.
```