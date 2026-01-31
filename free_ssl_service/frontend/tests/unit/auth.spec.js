import { shallowMount } from '@vue/test-utils'
import Vuex from 'vuex'
import auth from '@/store/modules/auth'

describe('Auth Store Module', () => {
  let store

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        auth: auth
      }
    })
  })

  it('initial state should be correct', () => {
    expect(store.state.auth.user).toBe(null)
    expect(store.state.auth.token).toBe(null)
    expect(store.state.auth.isAuthenticated).toBe(false)
  })

  it('SET_USER mutation should update user', () => {
    const user = { id: 1, username: 'test', email: 'test@example.com' }
    store.commit('auth/SET_USER', user)
    
    expect(store.state.auth.user).toEqual(user)
    expect(store.state.auth.isAuthenticated).toBe(true)
  })

  it('SET_TOKEN mutation should update token', () => {
    const token = 'test-token-123'
    store.commit('auth/SET_TOKEN', token)
    
    expect(store.state.auth.token).toBe(token)
    expect(localStorage.getItem('token')).toBe(token)
  })

  it('LOGOUT mutation should clear state', () => {
    store.commit('auth/SET_USER', { id: 1, username: 'test' })
    store.commit('auth/SET_TOKEN', 'test-token')
    store.commit('auth/LOGOUT')
    
    expect(store.state.auth.user).toBe(null)
    expect(store.state.auth.token).toBe(null)
    expect(store.state.auth.isAuthenticated).toBe(false)
    expect(localStorage.getItem('token')).toBe(null)
  })
})