# IGP Link State

## IGP Link-State Database Distribution

A given BGP node may have connections to multiple, independent routing domains. IGP link-state database distribution into BGP-LS is supported for both OSPF and IS-IS protocols in order to distribute this information on to controllers or applications that desire to build paths spanning or including these multiple domains.

To distribute OSPFv2 link-state data using BGP-LS, use the `distribute link-state` command in router configuration mode.

```bash
Router# configure
Router(config)# router ospf 100
Router(config-ospf)# distribute link-state instance-id 32
```