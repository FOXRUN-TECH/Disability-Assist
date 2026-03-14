# New React Native Component Scaffold Command

Scaffold a React Native component for the caregiver mobile app with accessibility props and privacy checks. [TS][DIG]

This command is for Phase 4+ when the `mobile/` directory exists.

## Usage

```text
/new-component <component-name>
```

Example: `/new-component IntentFeed` creates a caregiver intent feed component.

## What It Creates

### 1. Component File (`mobile/src/components/<Name>.tsx`)

```tsx
/**
 * <Name> component.
 *
 * <Description of what this component does.>
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface <Name>Props {
  /** Accessibility label for screen readers. */
  accessibilityLabel?: string;
}

export function <Name>({ accessibilityLabel }: <Name>Props) {
  return (
    <View
      style={styles.container}
      accessibilityLabel={accessibilityLabel ?? '<Name>'}
      accessibilityRole="summary"
    >
      <Text style={styles.text}>
        {/* Component content */}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    // Layout styles
  },
  text: {
    // Text styles
  },
});
```

### 2. Test File (`mobile/src/components/__tests__/<Name>.test.tsx`)

```tsx
/**
 * Tests for <Name> component.
 */

import React from 'react';
import { render, screen } from '@testing-library/react-native';
import { <Name> } from '../<Name>';

describe('<Name>', () => {
  it('renders with accessibility label', () => {
    render(<<Name> accessibilityLabel="Test label" />);
    expect(screen.getByLabelText('Test label')).toBeTruthy();
  });

  it('renders default accessibility label', () => {
    render(<<Name> />);
    expect(screen.getByLabelText('<Name>')).toBeTruthy();
  });
});
```

### 3. Zod Schema (if component accepts user input)

```tsx
// mobile/src/schemas/<name>.ts
import { z } from 'zod';

export const <Name>InputSchema = z.object({
  // Input validation
});
```

## Accessibility Requirements [DIG]

Every component MUST include:

- `accessibilityLabel` -- descriptive label for screen readers
- `accessibilityHint` -- describes what happens on interaction (if interactive)
- `accessibilityRole` -- semantic role (`button`, `summary`, `alert`, etc.)
- Sufficient color contrast (WCAG 2.1 AA minimum)
- Touch target size >= 44x44 points

## Privacy Requirements [PV]

Components displaying user data MUST:

- Check consent status before rendering user-specific content
- Never display raw transcript (use paraphrase)
- Apply role-based filtering (family vs professional vs guardian)
- Not cache sensitive data in component state beyond the current session

## Checklist

- [ ] TypeScript component with props interface
- [ ] Accessibility props included (`accessibilityLabel`, `accessibilityRole`)
- [ ] StyleSheet (React Native standard)
- [ ] Test file with accessibility assertions
- [ ] Zod schema for any user input
- [ ] Privacy consent check if displaying user data
- [ ] File-scoped quality check on new files

## Related Commands

- `/review` -- Review before committing
- `/commit` -- Commit the new component
- `/privacy-audit` -- Verify privacy compliance
