---
name: 'FunctionalComponent'
root: '.'
output: 'src/components/functional'
ignore: []
questions:
  name: 'Please enter the name of the component you want.'
---

# `{{ inputs.name | pascal }}/{{ inputs.name | pascal }}.tsx`

```tsx
import React from 'react';

export const {{ inputs.name | pascal }}: React.FC = () => {
  return (
    <></>
  )
}
```

# `{{ inputs.name | pascal }}/index.ts`

```ts
export * from './{{ inputs.name }}';
```

# `{{ inputs.name | pascal }}/__test__/{{ inputs.name | pascal }}.test.tsx`

```tsx
import { {{ inputs.name | pascal }} } from '../{{ inputs.name | pascal }}';
import { fixture } from '@/utils/testHelpers';

describe('{{ inputs.name | pascal }}', () => {
  let element: Element;
  let restoreFixture: () => void;
  beforeEach(() => {
    ({ element, restoreFixture } = fixture(<{{ inputs.name | pascal }} />));
  })
  it('TODO', () => {})
})

```