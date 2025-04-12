const state = {
    certificates: []
}

const mutations = {
    SET_CERTIFICATES(state, certs) {
        state.certificates = certs
    }
}

const actions = {
    async fetchCertificates({ commit }) {
        try {
            const response = await axios.get('/certs')
            commit('SET_CERTIFICATES', response.data)
        } catch (error) {
            console.error('Failed to fetch certificates:', error)
        }
    },

    async createCertificate({ commit }, data) {
        try {
            const response = await axios.post('/certs', data)
            commit('SET_CERTIFICATES', [...state.certificates, response.data])
            return response.data
        } catch (error) {
            console.error('Failed to create certificate:', error)
            throw error
        }
    },

    async renewCertificate({ commit }, { id, data }) {
        try {
            const response = await axios.post(`/certs/${id}/renew`, data)
            const updatedCerts = state.certificates.map(cert =>
                cert.id === id ? response.data : cert
            )
            commit('SET_CERTIFICATES', updatedCerts)
            return response.data
        } catch (error) {
            console.error('Failed to renew certificate:', error)
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
