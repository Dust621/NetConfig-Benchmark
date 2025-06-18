# Floating Static Routes

Floating static routes are static routes that are used to back up dynamic routes learned through configured routing protocols. A floating static route is configured with a higher administrative distance than the dynamic routing protocol it is backing up. As a result, the dynamic route learned through the routing protocol is always preferred to the floating static route. If the dynamic route learned through the routing protocol is lost, the floating static route is used in its place.

By default, static routes have smaller administrative distances than dynamic routes, so static routes are preferred to dynamic routes.

## Note

A floating static route is often used to provide a backup path if connectivity fails. In the following example, a route is configured with an administrative distance of 201.

```bash
configure
router static
address-family ipv6 unicast
2001:0DB8::/32 2001:0DB8:3000::1 201
end
```

## Configure Floating Static Route

This task explains how to configure a floating static route.

### SUMMARY STEPS

1. `configure`
2. `router static`
3. `vrf vrf-name`
4. `address-family { ipv4 | ipv6 } { unicast | multicast }`
5. `prefix mask [vrf vrf-name ] { ip-address | interface-type interface-instance } [ distance ] [ description text ] [ tag tag ] [ permanent ]`
6. Use the `commit` or `end` command.

### DETAILED STEPS

**Step 1**  
`configure`  

Example:  
```bash
RP/0/RP0/CPU0:router# configure
```  
Enters configuration mode.

---

**Step 2**  
`router static`  

Example:  
```bash
RP/0/RP0/CPU0:router(config)# router static
```  
Enters static route configuration mode.

---

**Step 3**  
`vrf vrf-name`  

Example:  
```bash
RP/0/RP0/CPU0:router(config-static)# vrf vrf_A
```  
*(Optional)* Enters VRF configuration mode.  
If a VRF is not specified, the static route is configured under the default VRF.

---

**Step 4**  
`address-family { ipv4 | ipv6 } { unicast | multicast }`  

Example:  
```bash
RP/0/RP0/CPU0:router(config-static-vrf)# address-family ipv6 unicast
```  
Enters address family mode.

---

**Step 5**  
`prefix mask [vrf vrf-name ] { ip-address | interface-type interface-instance } [ distance ] [ description text ] [ tag tag ] [ permanent ]`  

Example:  
```bash
RP/0/RP0/CPU0:router(config-static-vrf-afi)# 2001:0DB8::/32 2001:0DB8:3000::1 201
```  
Configures an administrative distance of 201.

---

**Step 6**  
Use the `commit` or `end` command.  

- `commit` — Saves the configuration changes and remains within the configuration session.  
- `end` — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  