import api from '@/utils/api'

const state = {
    certificates: []
}

const mutations = {
    SET_CERTIFICATES(state, certs) {
        state.certificates = certs
    },
    ADD_CERTIFICATE(state, cert) {
        state.certificates.unshift(cert)
    },
    UPDATE_CERTIFICATE(state, cert) {
        const index = state.certificates.findIndex(c => c.id === cert.id)
        if (index !== -1) {
            state.certificates.splice(index, 1, cert)
        }
    }
}

const actions = {
    async fetchCertificates({ commit }) {
        try {
            const response = await api.get('/certs')
            commit('SET_CERTIFICATES', response.data)
        } catch (error) {
            console.error('Failed to fetch certificates:', error)
            throw error
        }
    },

    async createCertificate({ commit }, data) {
        try {
            const response = await api.post('/certs', data)
            commit('ADD_CERTIFICATE', response.data)
            return response.data
        } catch (error) {
            console.error('Failed to create certificate:', error)
            throw error
        }
    },

    async renewCertificate({ commit }, certId) {
        try {
            const response = await api.post(`/certs/${certId}/renew`)
            commit('UPDATE_CERTIFICATE', response.data)
            return response.data
        } catch (error) {
            console.error('Failed to renew certificate:', error)
            throw error
        }
    },

    async getCertificate({ commit }, certId) {
        try {
            const response = await api.get(`/certs/${certId}`)
            return response.data
        } catch (error) {
            console.error('Failed to get certificate:', error)
            throw error
        }
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}