```markdown
# Restrictions for Configuring IRB

Before configuring IRB, consider these restrictions:

## BVI Configuration Restrictions

- Only one BVI can be configured in any bridge domain.
- The same BVI cannot be configured in multiple bridge domains.

## Unsupported Features on Layer 2 Bridging (with BVI)

The following areas are not supported on the Layer 2 bridging (with BVI):

- **Access Control Lists (ACLs)**  
  However, Layer 2 ACLs can be configured on each Layer 2 port of the bridge domain.
- Static MAC entry configuration in Bridge.
- MAC ageing configuration at global config mode.
- MAC Learning Disable.
- Port-channel sub-interface as bridge member.
- Physical sub-interface as bridge member.
- VLAN rewrite.
- QOS configuration on BVI interface is not supported.
- VRF on BVI interface is not supported.
```