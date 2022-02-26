import { Meta, Story } from '@storybook/react'

import { NavBar } from './NavBar'

const meta: Meta = {
  title: 'Components/NavBar',
  component: NavBar
}

export default meta

// write templates
const Templates: Story<typeof NavBar> = (props) => <NavBar {...props} />;

export const Default = Templates.bind({});
