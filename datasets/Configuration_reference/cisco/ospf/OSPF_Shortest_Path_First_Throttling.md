# OSPF Shortest Path First Throttling

OSPF SPF throttling makes it possible to configure SPF scheduling in millisecond intervals and to potentially delay SPF calculations during network instability. SPF is scheduled to calculate the Shortest Path Tree (SPT) when there is a change in topology. One SPF run may include multiple topology change events.

The interval at which the SPF calculations occur is chosen dynamically and based on the frequency of topology changes in the network. The chosen interval is within the boundary of the user-specified value ranges. If network topology is unstable, SPF throttling calculates SPF scheduling intervals to be longer until topology becomes stable.

SPF calculations occur at the interval set by the `timers throttle spf` command. The wait interval indicates the amount of time to wait until the next SPF calculation occurs. Each wait interval after that calculation is twice as long as the previous interval until the interval reaches the maximum wait time specified.

## SPF Timing Example

The SPF timing can be better explained using an example. In this example, the start interval is set at 5 milliseconds (ms), initial wait interval at 1000 ms, and maximum wait time at 90,000 ms.

```bash
timers spf 5 1000 90000
```

**Figure 2: SPF Calculation Intervals Set by the `timers spf` Command**

This figure shows the intervals at which the SPF calculations occur as long as at least one topology change event is received in a given wait interval.

Notice that the wait interval between SPF calculations doubles when at least one topology change event is received during the previous wait interval. After the maximum wait time is reached, the wait interval remains the same until the topology stabilizes and no event is received in that interval.

If the first topology change event is received after the current wait interval, the SPF calculation is delayed by the amount of time specified as the start interval. The subsequent wait intervals continue to follow the dynamic pattern.

If the first topology change event occurs after the maximum wait interval begins, the SPF calculation is again scheduled at the start interval and subsequent wait intervals are reset according to the parameters specified in the `timers throttle spf` command. Notice in **Figure 3: Timer Intervals Reset After Topology Change Event** that a topology change event was received after the start of the maximum wait time interval and that the SPF intervals have been reset.

**Figure 3: Timer Intervals Reset After Topology Change Event**

## Configure OSPF Shortest Path First Throttling

This task explains how to configure SPF scheduling in millisecond intervals and potentially delay SPF calculations during times of network instability. This task is optional.

### SUMMARY STEPS

1. `configure`
2. Do one of the following:
   - `router ospf process-name`
   - `router ospfv3 process-name`
3. `router-id { router-id }`
4. `timers throttle spf spf-start spf-hold spf-max-wait`
5. `area area-id`
6. `interface type interface-path-id`
7. Use the `commit` or `end` command.
8. Do one of the following:
   - `show ospf [ process-name ]`
   - `show ospfv3 [ process-name ]`

### DETAILED STEPS

#### Step 1: `configure`

Example:
```bash
RP/0/RP0/CPU0:router# configure
```
Enters mode.

#### Step 2: Enable OSPF/OSPFv3 Routing

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

- Enables OSPF routing for the specified routing process and places the router in router configuration mode.
- Enables OSPFv3 routing for the specified routing process and places the router in router ospfv3 configuration mode.

> **Note:** The `process-name` argument is any alphanumeric string no longer than 40 characters.

#### Step 3: `router-id { router-id }`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# router-id 192.168.4.3
```
Configures a router ID for the OSPF process.

> **Note:** We recommend using a stable IPv4 address as the router ID.

#### Step 4: `timers throttle spf spf-start spf-hold spf-max-wait`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# timers throttle spf 10 4800 90000
```
Sets SPF throttling timers.

#### Step 5: `area area-id`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf)# area 0
```
Enters area configuration mode and configures a backbone area.

> **Note:** The `area-id` argument can be entered in dotted-decimal or IPv4 address notation, such as `area 1000` or `area 0.0.3.232`. However, you must choose one form or the other for an area. We recommend using the IPv4 address notation.

#### Step 6: `interface type interface-path-id`

Example:
```bash
RP/0/RP0/CPU0:router(config-ospf-ar)# interface TenGigE 0/0/0/0
```
Enters interface configuration mode and associates one or more interfaces to the area.

#### Step 7: Use the `commit` or `end` command

- `commit` — Saves the configuration changes and remains within the configuration session.
- `end` — Prompts user to take one of these actions:
  - **Yes** — Saves configuration changes and exits the configuration session.
  - **No** — Exits the configuration session without committing the configuration changes.
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.

#### Step 8: Verify SPF Throttling Timers

Do one of the following:
- `show ospf [ process-name ]`
- `show ospfv3 [ process-name ]`

Example:
```bash
RP/0/RP0/CPU0:router# show ospf 1
```
or
```bash
RP/0/RP0/CPU0:router# show ospfv3 2
```
(Optional) Displays SPF throttling timers.