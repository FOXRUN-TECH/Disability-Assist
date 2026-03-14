# PRD-06 · Adaptive Voice Output

**Project:** Disability-Assist  
**Version:** 2.0-draft  
**Status:** Replacement Draft

## 1. Objective

Provide speech output that is more intelligible and less stressful for the user than generic consumer-assistant voices.

## 2. Adjustable Parameters
- pitch;
- loudness;
- speech rate;
- pause spacing;
- accent / locale where provider supports it;
- perceived gender or voice identity;
- output EQ / frequency shaping;
- text-only mode;
- quiet mode.

## 3. Accessibility Modes

### 3.1 Intelligibility Mode
For hearing loss or comprehension difficulty:
- slower pacing;
- simpler sentence construction;
- configurable EQ emphasis.

### 3.2 Sensory-Safe Mode
For overload-sensitive users:
- no startup tones;
- reduced loudness ceiling;
- terse responses;
- optional TTS suppression.

### 3.3 Familiarity Mode
The system may preserve a stable voice choice to improve comfort, but must not claim therapeutic benefit.

## 4. Rules
- responses must be brief by default;
- avoid robotic over-confirmation;
- never use playful variation in strict-predictability mode;
- no synthetic affect that could mislead users into believing a human is present.

## 5. Testing
- user-adjustable profile saved and restored correctly;
- text-only mode suppresses all speech;
- sensory-safe mode disables non-essential sounds;
- EQ profile changes are audible and reproducible.
