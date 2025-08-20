import { mount } from '@vue/test-utils'
import HelloWorld from '../src/components/HelloWorld.vue'

describe('HelloWorld.vue', () => {
  const defaultMsg = 'Hello World'

  test('renders props.msg when passed', () => {
    const msg = 'Hello Vitest'
    const wrapper = mount(HelloWorld, {
      props: {
        msg
      }
    })
    expect(wrapper.find('h1').text()).toBe(msg)
  })

  test('has correct initial count', () => {
    const wrapper = mount(HelloWorld, {
      props: {
        msg: defaultMsg
      }
    })
    expect(wrapper.find('button').text()).toContain('count is 0')
  })

  test('increments count when button is clicked', async () => {
    const wrapper = mount(HelloWorld, {
      props: {
        msg: defaultMsg
      }
    })
    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.find('button').text()).toContain('count is 1')
  })
})