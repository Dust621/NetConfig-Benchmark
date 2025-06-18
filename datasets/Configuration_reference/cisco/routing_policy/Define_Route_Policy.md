```markdown
# Define Route Policy

This task explains how to define a route policy.

- If you want to modify an existing routing policy using the command-line interface (CLI), you must redefine the policy by completing this task.
- Modifying the RPL scale configuration may take a long time.
- BGP may crash either due to large scale RPL configuration changes, or during consecutive RPL changes. To avoid BGP crash, wait until there are no messages in the BGP In/Out queue before committing further changes.

> **Note**  
> You can programmatically configure the route policy using `openconfig-routing-policy.yang` OpenConfig data model. To get started with using data models, see the [Programmability Configuration Guide](#).

> **Tip**  

## SUMMARY STEPS

1. `configure`  
2. `route-policy name [ parameter1 , parameter2 , . . . , parameterN ]`  
3. `end-policy`  
4. Use the `commit` or `end` command.  

## DETAILED STEPS

### Step 1  
`configure`  

**Example:**  
```bash
RP/0/RP0/CPU0:router# configure
```  
Enters mode.  

### Step 2  
`route-policy name [ parameter1 , parameter2 , . . . , parameterN ]`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config)# route-policy sample1
```  
Enters route-policy configuration mode.  

- After the route-policy has been entered, a group of commands can be entered to define the route-policy.  

### Step 3  
`end-policy`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-rpl)# end-policy
```  
Ends the definition of a route policy and exits route-policy configuration mode.  

### Step 4  
Use the `commit` or `end` command.  

- `commit` — Saves the configuration changes and remains within the configuration session.  
- `end` — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  

## Routing Policy Definition: Example  

In the following example, a BGP route policy named `sample1` is defined using the `route-policy name` command. The policy compares the network layer reachability information (NLRI) to the elements in the prefix set `test`. If it evaluates to `true`, the policy performs the operations in the `then` clause. If it evaluates to `false`, the policy performs the operations in the `else` clause, that is, sets the MED value to `200` and adds the community `2:100` to the route. The final steps of the example commit the configuration to the router, exit configuration mode, and display the contents of route policy `sample1`.  

```bash
configure
route-policy sample1
  if destination in test then
    drop
  else
    set med 200
    set community (2:100) additive
  endif
end-policy
end
show config running route-policy sample1
```

**Output:**  
```bash
Building configuration...
route-policy sample1
  if destination in test then
    drop
  else
    set med 200
    set community (2:100) additive
  endif
end-policy
```
```