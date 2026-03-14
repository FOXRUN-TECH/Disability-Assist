"""PostToolUse hook: remind to fix RPi5 default route on SSH network errors.

Detects SSH connection failures and network-related errors in Bash output,
then reminds Claude to check/fix the RPi5 default route and DNS.

Always exits 0 (non-blocking reminder).
"""

from __future__ import annotations

import json
import sys

# Error patterns that suggest RPi5 networking issues
NETWORK_ERROR_PATTERNS = (
    "Network is unreachable",
    "Temporary failure resolving",
    "Could not resolve host",
    "Connection timeout",
    "No route to host",
    "connect: Network is unreachable",
    "Temporary failure in name resolution",
)

# Patterns that suggest dpkg lock issues
DPKG_ERROR_PATTERNS = (
    "dpkg frontend lock",
    "Could not get lock /var/lib/dpkg",
    "dpkg was interrupted",
)


def main() -> None:
    """Check Bash tool output for RPi5 network/dpkg errors and print reminders."""
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, OSError):
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    # Get the command output (tool_result contains stdout/stderr from Bash)
    tool_result = hook_input.get("tool_result", "")
    if not isinstance(tool_result, str):
        tool_result = str(tool_result)

    # Check for network errors
    for pattern in NETWORK_ERROR_PATTERNS:
        if pattern in tool_result:
            print(
                "REMINDER: RPi5 network error detected. The default route is "
                "ephemeral and lost on reboot. Fix with:\n"
                "  1. sudo ip route add default via 192.168.137.1 dev eth0\n"
                '  2. echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf\n'
                "  3. Verify: ping -c 1 8.8.8.8",
                file=sys.stderr,
            )
            break

    # Check for dpkg errors
    for pattern in DPKG_ERROR_PATTERNS:
        if pattern in tool_result:
            print(
                "REMINDER: dpkg lock/interrupt detected on RPi5. Fix with:\n"
                "  sudo DEBIAN_FRONTEND=noninteractive dpkg --configure -a "
                "--force-confold\n"
                "If lock is held by a stale process, check: ps aux | grep dpkg",
                file=sys.stderr,
            )
            break


if __name__ == "__main__":
    main()
    sys.exit(0)
