# ADR-001: Cloud-First Architecture

## Status

Accepted

## Date

2026-03-13

## Context

The system needs to interpret degraded and non-standard speech from users with various communication barriers, including speech, cognitive, sensory, developmental, and age-related conditions. Local-only inference cannot match cloud model quality for this specialized task. The target hardware (Raspberry Pi 5) lacks GPU acceleration for competitive on-device inference, and the specialized nature of the speech patterns requires large, frequently updated models that exceed local compute budgets.

## Decision

Adopt a cloud-first architecture with limited local degraded fallback.

- Cloud STT, LLM, and TTS are the primary inference path for all speech understanding and response generation.
- The local device (RPi5) handles audio capture, wake word detection, VAD (voice activity detection), and action routing.
- A degraded local mode provides a narrow allow-list of pre-approved actions (e.g., "turn on light", "play music") when cloud connectivity is unavailable.
- Full local inference parity is explicitly out of scope. The degraded mode is a safety net, not a feature-equivalent fallback.

## Consequences

### Positive

- Best available model quality for interpreting degraded and non-standard speech patterns
- No GPU hardware cost at the device level, keeping per-unit cost within CAD 190-320 target
- Models are updateable and improvable without device-side deployments
- Enables centralized assistive priors and community pattern learning (with consent)
- Pilot scale allows rapid iteration on model selection and tuning

### Negative

- Internet connectivity is required for full functionality
- End-to-end latency target of 3.5 seconds median adds complexity to the audio pipeline
- Recurring cloud operating costs targeted at CAD 8-15 per user per month
- All audio data transits the network, requiring encrypted transport and strict consent controls
- Cloud provider dependency introduces vendor risk

### Neutral

- Pilot scale of 10-20 units keeps cloud costs manageable during initial phases
- Architecture does not preclude future local model improvements if hardware evolves
- Cloud-first aligns with the consent model, where cloud processing is consent lane 1 (core-cloud), a required lane

## Compliance Impact

- Privacy: Medium -- all audio transits the network; encrypted transport (TLS 1.3+) is mandatory; no raw audio retention without explicit consent
- Security: Medium -- cloud API credentials must be securely managed; device-to-cloud channel must be authenticated
- Consent lanes affected: Lane 1 (core-cloud) is required for system operation
- Risk tiers affected: None directly; risk tiers apply at the action layer, not the inference layer

## References

- [PRD-03: System Architecture](../../PRD-03-System-Architecture.md)
- [PRD-10: Hardware Reference Design](../../PRD-10-Hardware-Reference-Design.md)
- [PRD-11: Privacy, Security and Ethics](../../PRD-11-Privacy-Security-and-Ethics.md)
- [Roadmap](../../roadmap.md)
