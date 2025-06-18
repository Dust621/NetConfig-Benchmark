# Restrictions for Implementing Static Routes

These restrictions apply while implementing Static Routes:

## Static Routing to an Indirect Next Hop

- Static routing to an indirect next hop (any prefix learnt through the RIB and may be more specific over the AIB) that is part of a local subnet requires configuring static routes in the global table indicating the egress interfaces as next hop.  

- To avoid forward drop, configure static routes in the global table indicating the next-hop IP address to be the next hop.  

## Route Learning from AIB  

- Generally, a route is learnt from the AIB in the global table and is installed in the FIB.  

- However, this behavior will not be replicated to leaked prefixes. This could lead to inconsistencies in forwarding behavior.  