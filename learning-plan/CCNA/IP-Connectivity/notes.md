# IP Connectivity — Starter Notes

## Key topics

- IPv4 routing basics: routing table, next-hop, default route
- Static routes: `ip route` examples and use cases
- Dynamic routing intro: OSPF single-area (area 0) basics, neighbor formation, LSAs
- Route selection: administrative distance, metric considerations
- IPv6 basics for routing: link-local, global unicast, OSPFv3 basics

## Common Cisco commands

- `show ip route`
- `show ip ospf neighbor`
- `show ip protocols`
- Configure static route: `ip route 0.0.0.0 0.0.0.0 192.168.1.1`
- Basic OSPF config (sample):
```
router ospf 1
 network 10.0.0.0 0.255.255.255 area 0
```

## Practical notes

- Start with static routes in small labs to understand next-hop behavior before adding OSPF.
- Use `debug ip routing` and `show ip route` to trace route propagation; be cautious with `debug` on production devices.
- Check MTU mismatches for tunneled/serial links if routes appear but traffic fails.

## Practice tasks

1. Build a 3-router topology and configure static routes to achieve full connectivity; replace static routes with OSPF and verify routing table convergence.
2. Create a small IPv6 network and configure OSPFv3 for IPv6 learning.
3. Demonstrate administrative distance by adding two protocols that provide the same route and observe which is preferred.
