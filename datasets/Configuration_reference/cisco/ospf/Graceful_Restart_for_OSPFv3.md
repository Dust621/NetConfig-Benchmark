```markdown
# Graceful Restart for OSPFv3

The OSPFv3 Graceful Shutdown feature preserves the data plane capability in these circumstances:

- Planned OSPFv3 process restart, such as a restart resulting from a software upgrade or downgrade
- Unplanned OSPFv3 process restart, such as a restart resulting from a process crash

In addition, OSPFv3 will unilaterally shutdown and enter the exited state when a critical memory event, indicating the processor is critically low on available memory, is received from the sysmon watch dog process.

This feature supports nonstop data forwarding on established routes while the OSPFv3 routing protocol restarts. Therefore, this feature enhances high availability of IPv6 forwarding.

## Configure OSPFv3 Graceful Restart

This task explains how to configure a graceful restart for an OSPFv3 process. This task is optional.

### SUMMARY STEPS

1. `configure`
2. `router ospfv3 process-name`
3. `graceful-restart`
4. `graceful-restart lifetime`
5. `graceful-restart interval seconds`
6. `graceful-restart helper disable`
7. Use the `commit` or `end` command.
8. `show ospfv3 [ process-name [ area-id ]] database grace`

### DETAILED STEPS

#### Step 1  
`configure`  

**Example:**  
```bash
RP/0/RP0/CPU0:router# configure
```  
Enters mode.

#### Step 2  
`router ospfv3 process-name`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config)# router ospfv3 test
```  
Enters router configuration mode for OSPFv3. The process name is a WORD that uniquely identifies an OSPF routing process. The process name is any alphanumeric string no longer than 40 characters without spaces.

#### Step 3  
`graceful-restart`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-ospfv3)# graceful-restart
```  
Enables graceful restart on the current router.

#### Step 4  
`graceful-restart lifetime`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-ospfv3)# graceful-restart lifetime 120
```  
Specifies a maximum duration for a graceful restart.  

- The default lifetime is 95 seconds.  
- The range is 90 to 3600 seconds.  

#### Step 5  
`graceful-restart interval seconds`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-ospfv3)# graceful-restart interval 120
```  
Specifies the interval (minimal time) between graceful restarts on the current router.  

- The default value for the interval is 90 seconds.  
- The range is 90 to 3600 seconds.  

#### Step 6  
`graceful-restart helper disable`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-ospfv3)# graceful-restart helper disable
```  
Disables the helper capability.  

#### Step 7  
Use the `commit` or `end` command.  

- `commit` — Saves the configuration changes and remains within the configuration session.  
- `end` — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  

#### Step 8  
`show ospfv3 [ process-name [ area-id ]] database grace`  

**Example:**  
```bash
RP/0/RP0/CPU0:router# show ospfv3 1 database grace
```  
Displays the state of the graceful restart link.  

## Display Information About Graceful Restart  

This section describes the tasks you can use to display information about a graceful restart.  

- To see if the feature is enabled and when the last graceful restart ran, use the `show ospf` command. To see details for an OSPFv3 instance, use the `show ospfv3 process-name [ area-id ] database grace` command.  

### Displaying the State of the Graceful Restart Feature  

The following screen output shows the state of the graceful restart capability on the local router:  

```bash
RP/0/RP0/CPU0:router# show ospfv3 1 database grace
Routing Process “ospfv3 1” with ID 2.2.2.2
Initial SPF schedule delay 5000 msecs
Minimum hold time between two consecutive SPFs 10000 msecs
Maximum wait time between two consecutive SPFs 10000 msecs
Initial LSA throttle delay 0 msecs
Minimum hold time for LSA throttle 5000 msecs
Maximum wait time for LSA throttle 5000 msecs
Minimum LSA arrival 1000 msecs
LSA group pacing timer 240 secs
Interface flood pacing timer 33 msecs
Retransmission pacing timer 66 msecs
Maximum number of configured interfaces 255
Number of external LSA 0. Checksum Sum 00000000
Number of areas in this router is 1. 1 normal 0 stub 0 nssa
Graceful Restart enabled, last GR 11:12:26 ago (took 6 secs)
Area BACKBONE(0)
Number of interfaces in this area is 1
SPF algorithm executed 1 times
Number of LSA 6. Checksum Sum 0x0268a7
Number of DCbitless LSA 0
Number of indication LSA 0
Number of DoNotAge LSA 0
Flood list length 0
```  
```