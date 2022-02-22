---
name: 'UiComponent'
root: '.'
output: 'src/components/ui'
ignore: []
questions:
  name: 'Please enter name of the component you want.'
---

# `{{ inputs.name | pascal }}/{{ inputs.name | pascal }}.tsx`

```tsx
import React from 'react';
import type { FC } from 'react';

interface IProps {}

export const {{ inputs.name | pascal }}: FC<IProps> = (props) => {
  return <></>;
};

```

# `{{ inputs.name | pascal }}/__tests__/{{ inputs.name | pascal }}.test.tsx`

```tsx
import React from 'react';
import { {{ inputs.name | pascal }} } from '../{{ inputs.name }}';

describe('{{ inputs.name | pascal }}', () => {
  it('__TODO__', () => {
    expect({{ inputs.name | pascal }}()).toBe(true);
  });
});
```

# `{{ inputs.name | pascal }}/{{ inputs.name | pascal }}.stories.tsx`

```tsx
import { Meta, Story } from '@storybook/react'

import { {{ inputs.name | pascal }} } from './{{ inputs.name | pascal }}'

const meta: Meta = {
  title: 'Components/{{ inputs.name | pascal }}',
  component: {{ inputs.name | pascal }}
}

export default meta

// write templates

```

# `{{ inputs.name | pascal }}/index.ts`

```ts
export * from './{{ inputs.name | pascal }}';
```