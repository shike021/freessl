import { shallowMount } from '@vue/test-utils'
import Vuex from 'vuex'
import certs from '@/store/modules/certs'

describe('Certs Store Module', () => {
  let store

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        certs: certs
      }
    })
  })

  it('initial state should be correct', () => {
    expect(store.state.certs.certificates).toEqual([])
  })

  it('SET_CERTIFICATES mutation should update certificates', () => {
    const mockCerts = [
      {
        id: 1,
        domains: 'example.com',
        expiry_date: '2024-12-31T00:00:00'
      }
    ]
    
    store.commit('certs/SET_CERTIFICATES', mockCerts)
    
    expect(store.state.certs.certificates).toEqual(mockCerts)
  })

  it('ADD_CERTIFICATE mutation should add a certificate to the beginning of the list', () => {
    const mockCert1 = {
      id: 1,
      domains: 'example.com',
      expiry_date: '2024-12-31T00:00:00'
    }
    
    const mockCert2 = {
      id: 2,
      domains: 'test.com',
      expiry_date: '2024-12-31T00:00:00'
    }
    
    // 添加第一个证书
    store.commit('certs/ADD_CERTIFICATE', mockCert1)
    expect(store.state.certs.certificates[0]).toEqual(mockCert1)
    
    // 添加第二个证书，应该在列表开头
    store.commit('certs/ADD_CERTIFICATE', mockCert2)
    expect(store.state.certs.certificates[0]).toEqual(mockCert2)
    expect(store.state.certs.certificates[1]).toEqual(mockCert1)
  })

  it('UPDATE_CERTIFICATE mutation should update an existing certificate', () => {
    const mockCert = {
      id: 1,
      domains: 'example.com',
      expiry_date: '2024-12-31T00:00:00'
    }
    
    const updatedCert = {
      id: 1,
      domains: 'example.com',
      expiry_date: '2025-12-31T00:00:00' // 更新过期日期
    }
    
    // 添加证书
    store.commit('certs/ADD_CERTIFICATE', mockCert)
    expect(store.state.certs.certificates[0].expiry_date).toBe('2024-12-31T00:00:00')
    
    // 更新证书
    store.commit('certs/UPDATE_CERTIFICATE', updatedCert)
    expect(store.state.certs.certificates[0].expiry_date).toBe('2025-12-31T00:00:00')
  })

  it('UPDATE_CERTIFICATE mutation should not affect other certificates', () => {
    const mockCert1 = {
      id: 1,
      domains: 'example.com',
      expiry_date: '2024-12-31T00:00:00'
    }
    
    const mockCert2 = {
      id: 2,
      domains: 'test.com',
      expiry_date: '2024-12-31T00:00:00'
    }
    
    const updatedCert1 = {
      id: 1,
      domains: 'example.com',
      expiry_date: '2025-12-31T00:00:00' // 更新过期日期
    }
    
    // 添加两个证书
    store.commit('certs/ADD_CERTIFICATE', mockCert1)
    store.commit('certs/ADD_CERTIFICATE', mockCert2)
    
    // 更新第一个证书
    store.commit('certs/UPDATE_CERTIFICATE', updatedCert1)
    
    // 验证第一个证书已更新
    expect(store.state.certs.certificates.find(c => c.id === 1).expiry_date).toBe('2025-12-31T00:00:00')
    
    // 验证第二个证书未受影响
    expect(store.state.certs.certificates.find(c => c.id === 2).expiry_date).toBe('2024-12-31T00:00:00')
  })
})

