# Automation & Programmability — Starter Notes

## Key topics

- Network programmability basics: REST APIs, NETCONF, data models (YANG)
- Data formats: JSON and YAML basics and examples
- Configuration management: Ansible intro (playbook structure, modules for network devices)
- Benefits: repeatability, reduced human error, faster deployments
- Simple examples: REST GET to retrieve interface status, Ansible to push a VLAN config

## Practical commands / examples

- Example JSON snippet (interface status):
```
{"interfaces": [{"name": "Gig0/1", "status": "up"}]}
```
- Example Ansible task (pseudo):
```
- name: configure vlan
  ios_vlan:
    vlan_id: 10
    name: STUDENT
```

## Practical notes

- Start with read-only automation tasks (inventory, show output parsing) before attempting config pushes.
- Use lab devices or emulators (GNS3/packet tracer with API-capable images) for testing automation safely.

## Practice tasks

1. Use `curl` to query a device or controller API for a simple GET (if you have lab images exposing REST).
2. Write a minimal Ansible playbook that pushes one VLAN to a lab switch (use `--check` for dry-run).
3. Parse `show` output with a simple Python script using `textfsm` or `ntc-templates`.
