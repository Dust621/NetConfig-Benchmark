```markdown
# Modify Routing Policy Using Text Editor

This task explains how to modify an existing routing policy using a text editor.

## SUMMARY STEPS

1. `edit { route-policy | prefix-set | as-path-set | community-set | extcommunity-set { rt | soo } | policy-global | rd-set } name [ nano | emacs | vim | inline { add | prepend | remove } set-element ]`
2. `show rpl route-policy [ name [ detail ] | states | brief ]`
3. `show rpl prefix-set [ name | states | brief ]`

## DETAILED STEPS

### Step 1

```
edit { route-policy | prefix-set | as-path-set | community-set | extcommunity-set { rt | soo } | policy-global | rd-set } name [ nano | emacs | vim | inline { add | prepend | remove } set-element ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# edit route-policy sample1
```

Identifies the route policy, prefix set, AS path set, community set, or extended community set name to be modified.

- A copy of the route policy, prefix set, AS path set, community set, or extended community set is copied to a temporary file and the editor is launched.
- After editing with Nano, save the editor buffer and exit the editor by using the `Ctrl-X` keystroke.
- After editing with Emacs, save the editor buffer by using the `Ctrl-X` and `Ctrl-S` keystrokes. To save and exit the editor, use the `Ctrl-X` and `Ctrl-C` keystrokes.
- After editing with Vim, to write to a current file and exit, use the `:wq` or `:x` or `ZZ` keystrokes. To quit and confirm, use the `:q` keystrokes. To quit and discard changes, use the `:q!` keystrokes.

### Step 2

```
show rpl route-policy [ name [ detail ] | states | brief ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show rpl route-policy sample2
```

(Optional) Displays the configuration of a specific named route policy.

- Use the `detail` keyword to display all policies and sets that a policy uses.
- Use the `states` keyword to display all unused, inactive, and active states.
- Use the `brief` keyword to list the names of all extended community sets without their configurations.

### Step 3

```
show rpl prefix-set [ name | states | brief ]
```

**Example:**

```bash
RP/0/RP0/CPU0:router# show rpl prefix-set prefixset1
```

(Optional) Displays the contents of a named prefix set.

- To display the contents of a named AS path set, community set, or extended community set, replace the `prefix-set` keyword with `as-path-set`, `community-set`, or `extcommunity-set`, respectively.

## Simple Inbound Policy: Example

The following policy discards any route whose network layer reachability information (NLRI) specifies a prefix longer than `/24`, and any route whose NLRI specifies a destination in the address space reserved by RFC 1918. For all remaining routes, it sets the MED and local preference, and adds a community to the list in the route.

For routes whose community lists include any values in the range from `101:202` to `106:202` that have a 16-bit tag portion containing the value `202`, the policy prepends autonomous system number `2` twice, and adds the community `2:666` to the list in the route. Of these routes, if the MED is either `666` or `225`, then the policy sets the origin of the route to incomplete, and otherwise sets the origin to IGP.

For routes whose community lists do not include any of the values in the range from `101:202` to `106:202`, the policy adds the community `2:999` to the list in the route.

```bash
prefix-set too-specific
  0.0.0.0/0 ge 25 le 32
end-set

prefix-set rfc1918
  10.0.0.0/8 le 32,
  172.16.0.0/12 le 32,
  192.168.0.0/16 le 32
end-set

route-policy inbound-tx
  if destination in too-specific or destination in rfc1918 then
    drop
  endif
  set med 1000
  set local-preference 90
  set community (2:1001) additive
  if community matches-any ([101..106]:202) then
    prepend as-path 2.30 2
    set community (2:666) additive
    if med is 666 or med is 225 then
      set origin incomplete
    else
      set origin igp
    endif
  else
    set community (2:999) additive
  endif
end-policy

router bgp 2
  neighbor 10.0.1.2
    address-family ipv4 unicast
      route-policy inbound-tx in
```

The following policy example shows how to build two inbound policies, `in-100` and `in-101`, for two different peers. In building the specific policies for those peers, the policy reuses some common blocks of policy that may be common to multiple peers. It builds a few basic building blocks, the policies `common-inbound`, `filter-bogons`, and `set-lpref-prepend`.

The `filter-bogons` building block is a simple policy that filters all undesirable routes, such as those from the RFC 1918 address space. The policy `set-lpref-prepend` is a utility policy that can set the local preference and prepend the AS path according to parameterized values that are passed in. The `common-inbound` policy uses these `filter-bogons` building blocks to build a common block of inbound policy. The `common-inbound` policy is used as a building block in the construction of `in-100` and `in-101` along with the `set-lpref-prepend` building block.

```bash
prefix-set bogon
  10.0.0.0/8 ge 8 le 32,
  0.0.0.0,
  0.0.0.0/0 ge 27 le 32,
  192.168.0.0/16 ge 16 le 32
end-set

route-policy in-100
  apply common-inbound
  if community matches-any ([100..120]:135) then
    apply set-lpref-prepend (100,100,2)
    set community (2:1234) additive
  else
    set local-preference 110
  endif
  if community matches-any ([100..666]:[100..999]) then
    set med 444
    set local-preference 200
    set community (no-export) additive
  endif
end-policy

route-policy in-101
  apply common-inbound
  if community matches-any ([101..200]:201) then
    apply set-lpref-prepend(100,101,2)
    set community (2:1234) additive
  else
    set local-preference 125
  endif
end-policy

route-policy filter-bogons
  if destination in bogon then
    drop
  else
    pass
  endif
end-policy

route-policy common-inbound
  apply filter-bogons
  set origin igp
  set community (2:333)
end-policy

route-policy set-lpref-prepend($lpref,$as,$prependcnt)
  set local-preference $lpref
  prepend as-path $as $prependcnt
end-policy
```