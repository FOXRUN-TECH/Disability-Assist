# Device Setup Command

Ensure RPi5 connectivity, fix networking, and run device provisioning.

## Usage

```text
/device-setup [setup-command]
```

Examples:
- `/device-setup` -- Check connectivity and fix networking only
- `/device-setup provision` -- Fix networking + run provisioning

## What It Does

1. **Load config**: Read RPi5 target from `HOST_SUFFIX_ID` in `.env`
2. **Test connectivity**: SSH to `192.168.137.<suffix>` with configured credentials
3. **Fix networking** (if RPi5 is reachable but has no internet):
   - Check default route: `ip route show default`
   - Add if missing: `sudo ip route add default via 192.168.137.1 dev eth0`
   - Check DNS: `cat /etc/resolv.conf`
   - Fix if needed: set `nameserver 8.8.8.8` + `nameserver 1.1.1.1`
   - Verify: `ping -c 1 8.8.8.8` and `ping -c 1 deb.debian.org`
4. **Fix dpkg** (if packages were interrupted):
   - Check: `sudo fuser /var/lib/dpkg/lock-frontend`
   - Fix: `sudo DEBIAN_FRONTEND=noninteractive dpkg --configure -a --force-confold`
5. **Run setup command** (if specified)

## Networking Context

The RPi5 connects to the development laptop via Ethernet (`192.168.137.0/24`).
Internet access is through Windows ICS (Internet Connection Sharing).
After each RPi5 reboot, the default route and DNS must be re-added (they are ephemeral).

```
[Windows Laptop .1] --ethernet--> [RPi5 .<suffix>] --NAT via .1--> Internet
```

## Troubleshooting

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| SSH timeout | RPi5 off or rebooting | Power cycle, wait 30-60s |
| No internet | Missing default route | `sudo ip route add default via 192.168.137.1 dev eth0` |
| DNS failure | Bad `/etc/resolv.conf` | `echo "nameserver 8.8.8.8" \| sudo tee /etc/resolv.conf` |
| dpkg lock | Interrupted apt/dpkg | `sudo DEBIAN_FRONTEND=noninteractive dpkg --configure -a --force-confold` |
| apt 404 | Stale package cache | `sudo apt-get update` |

## Related Commands

- `/commit` -- Commit and push after changes
