```markdown
# Set Priority for Adding Prefixes to RIB

This optional task describes how to set the priority (order) for which specified prefixes are added to the RIB. The prefixes can be chosen using an access list (ACL), prefix list, or by matching a tag value.

## SUMMARY STEPS

1. `configure`
2. `router isis instance-id`
3. `address-family { ipv4 | ipv6 } [ unicast ]`
4. `metric-style wide [ transition ] [ level { 1 | 2 }]`
5. `spf prefix-priority [ level { 1 | 2 }] { critical | high | medium } { access-list-name | tag tag }`
6. Use the `commit` or `end` command.

## DETAILED STEPS

### Step 1  
`configure`  

**Example:**  
```bash
RP/0/RP0/CPU0:router# configure
```  
Enters mode.

### Step 2  
`router isis instance-id`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config)# router isis isp
```  
Enables IS-IS routing for the specified routing process, and places the router in router configuration mode. In this example, the IS-IS instance is called `isp`.

### Step 3  
`address-family { ipv4 | ipv6 } [ unicast ]`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-isis)# address-family ipv4 unicast
```  
Specifies the IPv4 or IPv6 address family, and enters router address family configuration mode.

### Step 4  
`metric-style wide [ transition ] [ level { 1 | 2 }]`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-isis-af)# metric-style wide level 1
```  
Configures a router to generate and accept only wide-link metrics in the Level 1 area.

### Step 5  
`spf prefix-priority [ level { 1 | 2 }] { critical | high | medium } { access-list-name | tag tag }`  

**Example:**  
```bash
RP/0/RP0/CPU0:router(config-isis-af)# spf prefix-priority high tag 3
```  
Installs all routes tagged with the value `3` first.

### Step 6  
Use the `commit` or `end` command.  

- **`commit`** — Saves the configuration changes and remains within the configuration session.  
- **`end`** — Prompts user to take one of these actions:  
  - **Yes** — Saves configuration changes and exits the configuration session.  
  - **No** — Exits the configuration session without committing the configuration changes.  
  - **Cancel** — Remains in the configuration session, without committing the configuration changes.  
```