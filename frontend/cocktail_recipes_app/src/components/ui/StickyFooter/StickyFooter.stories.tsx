import { Meta, Story } from '@storybook/react'
import { MemoryRouter } from 'react-router-dom'
import { StickyFooter } from './StickyFooter'


const meta: Meta = {
  title: 'Components/StickyFooter',
  component: StickyFooter,
  decorators: [
    (story) => (
      <MemoryRouter
        initialEntries={[
          "/",
          "/about",
        ]}
      >
        {story()}
      </MemoryRouter>
    )
  ]
}

export default meta

// write templates
const Templates: Story<typeof StickyFooter> = (props) => <StickyFooter {...props} />;

export const Default = Templates.bind({});

