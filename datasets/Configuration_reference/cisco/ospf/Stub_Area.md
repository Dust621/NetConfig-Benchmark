# Stub Area

A stub area is an area that does not accept route advertisements or detailed network information external to the area. A stub area typically has only one router that interfaces the area to the rest of the autonomous system.

The stub ABR advertises a single default route to external destinations into the stub area. Routers within a stub area use this route for destinations outside the area and the autonomous system. This relationship conserves LSA database space that would otherwise be used to store external LSAs flooded into the area.

## Not-so-Stubby Area

A Not-so-Stubby Area (NSSA) is similar to the stub area. NSSA does not flood Type 5 external LSAs from the core into the area, but can import autonomous system external routes in a limited fashion within the area.

NSSA allows importing of Type 7 autonomous system external routes within an NSSA area by redistribution. These Type 7 LSAs are translated into Type 5 LSAs by NSSA ABRs, which are flooded throughout the whole routing domain.

Use the `capability type7 translate zero-forward-addr` command to enable the translation of Type-7 LSA with a zero forwarding address into Type-5 LSA on the NSSA ABR router. This command is supported only for OSPFv3. Summarization and filtering are supported during the translation.

Use NSSA to simplify administration if you are a network administrator that must connect a central site using OSPF to a remote site that is using a different routing protocol.

Before NSSA, the connection between the corporate site border router and remote router could not be run as an OSPF stub area because routes for the remote site could not be redistributed into a stub area, and two routing protocols needed to be maintained. A simple protocol like RIP was usually run and handled the redistribution.

With NSSA, you can extend OSPF to cover the remote connection by defining the area between the corporate router and remote router as an NSSA. Area 0 cannot be an NSSA.

## Configure Stub and Not-So-Stubby Area Types

This task explains how to configure the stub area and the NSSA for OSPF.

### SUMMARY STEPS

1. `configure`
2. Do one of the following:
   - `router ospf process-name`
   - `router ospfv3 process-name`
3. `capability type7 translate zero-forward-addr`
4. `router-id { router-id }`
5. `area area-id`
6. Do one of the following:
   - `stub [ no-summary ]`
   - `nssa [ no-redistribution ] [ default-information-originate ] [ no-summary ]`
7. Do one of the following:
   - `stub`
   - `nssa`
8. `default-cost cost`
9. Use the `commit` or `end` command.
10. Repeat this task on all other routers in the stub area or NSSA.

### DETAILED STEPS

#### Step 1

```bash
configure
```

Example:
```bash
RP/0/RP0/CPU0:router# configure
```

Enters mode.

#### Step 2

Do one of the following:
- `router ospf process-name`
- `router ospfv3 process-name`

Example:
```bash
RP/0/RP0/CPU0:router(config)# router ospf 1
```
or
```bash
RP/0/RP0/CPU0:router(config)# router ospfv3 1
```

Enables OSPF routing for the specified routing process and places the router in router configuration mode.

or

Enables OSPFv3 routing for the specified routing process and places the router in router ospfv3 configuration mode.

The `process-name` argument is any alphanumeric string no longer than 40 characters.

> **Note**

#### Step 3

```bash
capability type7 translate zero-forward-addr
```

Example:
```bash
RP/0/RP0/CPU0:router(config)# router ospfv3 1
RP/0/RP0/CPU0:router(config-ospfv3)# capability type7 translate zero-forward-addr
```

Enables the translation of Type-7 LSA with a zero forwarding address into Type-5 LSA on the NSSA ABR router.

You can configure `capability type7 translate zero-forward-addr` command only in router ospfv3 configuration mode. This command is not supported for the OSPF process.

> **Note**

#### Step 4

```bash
router-id { router-id }
```

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# router-id 192.168.4.3
```

Configures a router ID for the OSPF process.

We recommend using a stable IP address as the router ID.

> **Note**

#### Step 5

```bash
area area-id
```

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# area 1
```

Enters area configuration mode and configures a nonbackbone area for the OSPF process.

- The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

#### Step 6

Do one of the following:
- `stub [ no-summary ]`
- `nssa [ no-redistribution ] [ default-information-originate ] [ no-summary ]`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# stub no summary
```
or
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# nssa no-redistribution
```

Defines the nonbackbone area as a stub area.

- Specify the `no-summary` keyword to further reduce the number of LSAs sent into a stub area. This keyword prevents the ABR from sending summary link-state advertisements (Type 3) in the stub area.

or

Defines an area as an NSSA.

#### Step 7

Do one of the following:
- `stub`
- `nssa`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# stub
```
or
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# nssa
```

(Optional) Turns off the options configured for stub and NSSA areas.

- If you configured the stub and NSSA areas using the optional keywords (`no-summary`, `no-redistribution`, `default-information-originate`, and `no-summary`) in Step 5, you must now reissue the `stub` and `nssa` commands without the keywords—rather than using the `no` form of the command.
- For example, the `no nssa default-information-originate` form of the command changes the NSSA area into a normal area that inadvertently brings down the existing adjacencies in that area.

#### Step 8

```bash
default-cost cost
```

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)#default-cost 15
```

(Optional) Specifies a cost for the default summary route sent into a stub area or an NSSA.

- Use this command only on ABRs attached to the NSSA. Do not use it on any other routers in the area.
- The default cost is 1.

#### Step 9

Use the `commit` or `end` command.

- `commit` —Saves the configuration changes and remains within the configuration session.
- `end` —Prompts user to take one of these actions:
  - `Yes` — Saves configuration changes and exits the configuration session.
  - `No` —Exits the configuration session without committing the configuration changes.
  - `Cancel` —Remains in the configuration session, without committing the configuration changes.

#### Step 10

Repeat this task on all other routers in the stub area or NSSA.

---

### Configuring a Stub area: example

The following example shows that area 1 is configured as a stub area:

```bash
router ospfv3 1
router-id 10.0.0.217
area 0
interface TenGigE 0/2/0/1
area 1
stub
interface TenGigE 0/2/0/0
```