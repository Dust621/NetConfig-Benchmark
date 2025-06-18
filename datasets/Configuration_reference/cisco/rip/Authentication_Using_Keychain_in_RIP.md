# Authentication Using Keychain in RIP

Authentication using keychain in Cisco IOS XR Routing Information Protocol (RIP) provides a mechanism to authenticate all RIP protocol traffic on a RIP interface, based on keychain authentication. This mechanism uses the Cisco IOS XR security keychain infrastructure to store and retrieve secret keys and use them to authenticate in-bound and out-going traffic on a per-interface basis.

Keychain management is a common method of authentication to configure shared secrets on all entities that exchange secrets such as keys, before establishing trust with each other. Routing protocols and network management applications on Cisco IOS XR software often use authentication to enhance security while communicating with peers.

The Cisco IOS XR software system security component implements various system security features including keychain management. Refer to these documents for detailed information on keychain management concepts, configuration tasks, examples, and commands used to configure keychain management:

- *Implementing Keychain Management* module in *System Security Configuration Guide for Cisco NCS 5000 Series Routers*
- *Keychain Management Commands* module in *System Security Command Reference for Cisco NCS 5000 Series Routers*

> **Tip**  
> The keychain by itself has no relevance; therefore, it must be used by an application that needs to communicate by using the keys (for authentication) with its peers. The keychain provides a secure mechanism to handle the keys and rollover based on the lifetime. The Cisco IOS XR keychain infrastructure takes care of the hit-less rollover of the secret keys in the keychain.

> **Note**  
> Once you have configured a keychain in the IOS XR keychain database and if the same has been configured on a particular RIP interface, it will be used for authenticating all incoming and outgoing RIP traffic on that interface. Unless an authentication keychain is configured on a RIP interface (on the default VRF or a non-default VRF), all RIP traffic will be assumed to be authentic and authentication mechanisms for in-bound RIP traffic and out-bound RIP traffic will not be employed to secure it.

RIP employs two modes of authentication: keyed message digest mode and clear text mode. Use the following command to configure authentication using the keychain mechanism:

```bash
authentication keychain keychain-name mode {md5 | text}
```

In cases where a keychain has been configured on a RIP interface but the keychain is actually not configured in the keychain database or the keychain is not configured with the MD5 cryptographic algorithm, all incoming RIP packets on the interface will be dropped. Outgoing packets will be sent without any authentication data.

## In-bound RIP Traffic on an Interface

These are the verification criteria for all in-bound RIP packets on a RIP interface when the interface is configured with a keychain:

- **If the keychain configured on the RIP interface does not exist in the keychain database...**  
  The packet is dropped. A RIP component-level debug message is logged to provide the specific details of the authentication failure.

- **If the keychain is not configured with an MD5 cryptographic algorithm...**  
  The packet is dropped. A RIP component-level debug message is logged to provide the specific details of the authentication failure.

- **If the Address Family Identifier of the first (and only the first) entry in the message is not 0xFFFF, then authentication is not in use...**  
  The packet is dropped. A RIP component-level debug message is logged to provide the specific details of the authentication failure.

- **If the MD5 digest in the 'Authentication Data' is found to be invalid...**  
  The packet is dropped. A RIP component-level debug message is logged to provide the specific details of the authentication failure.

Else, the packet is forwarded for the rest of the processing.

## Out-bound RIP Traffic on an Interface

These are the verification criteria for all out-bound RIP packets on a RIP interface when the interface is configured with a keychain:

- **If the keychain configured on the RIP interface exists in the keychain database...**  
  The RIP packet passes authentication check at the remote/peer end, provided the remote router is also configured to authenticate the packets using the same keychain.

- **If the keychain is configured with an MD5 cryptographic algorithm...**  
  The RIP packet passes authentication check at the remote/peer end, provided the remote router is also configured to authenticate the packets using the same keychain.

Else, RIP packets fail authentication check.