# PRD-10 · Hardware Reference Design

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Define a practical pilot hardware platform for 10–20 units using available parts, reasonable assembly effort, and enough performance for cloud-first operation.

## 2. Hardware Strategy

Since v1 is cloud-first, the device does not need to carry full local conversational inference load. It does need:
- reliable audio capture;
- low-latency networking;
- stable local runtime;
- strong enough CPU for orchestration and local fallback commands.

## 3. Reference BOM

| Component | Target Spec | Est. Cost CAD |
|---|---|---:|
| SBC | Raspberry Pi 5, 8 GB | 90 |
| Mic array | 4-mic USB or equivalent | 35–45 |
| Storage | 64 GB high-endurance microSD or SSD | 18–40 |
| PSU | official or equivalent high-quality supply | 15 |
| Speaker + amp | intelligible near-field output | 15–25 |
| Enclosure / fasteners / wiring | pilot-grade | 15–25 |
| Optional display | 7" local screen | 60–80 |

### Practical Cost Target
- no-display unit: approximately CAD 190–240
- display unit: approximately CAD 250–320

Any PRD target materially below this range is unrealistic for the current v1 stack.

## 4. Physical Requirements
- always-on wall power;
- visible but non-intrusive status indicator;
- accessible volume control;
- microphone placement optimized for bedside / room use;
- enclosure safe for home and assisted-home settings.

## 5. Security Requirements
- unique device credentials at setup;
- secure update path;
- minimal open ports;
- remote admin only through approved secure channel.

## 6. Pilot Build Guidance
The design must support:
- repeatable imaging and provisioning;
- spare-parts replacement;
- simple field reset;
- deployment checklist per unit.
