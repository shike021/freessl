import api from '@/utils/api'

const state = {
    user: null,
    token: null,
    isAuthenticated: false
}

const mutations = {
    SET_USER(state, user) {
        state.user = user
        state.isAuthenticated = !!user
    },
    SET_TOKEN(state, token) {
        state.token = token
        if (token) {
            localStorage.setItem('token', token)
        } else {
            localStorage.removeItem('token')
        }
    },
    LOGOUT(state) {
        state.user = null
        state.token = null
        state.isAuthenticated = false
        localStorage.removeItem('token')
    }
}

const actions = {
    async login({ commit }, credentials) {
        try {
            const response = await api.post('/auth/login', credentials)
            commit('SET_TOKEN', response.data.token)
            commit('SET_USER', response.data.user)
            return response.data.user
        } catch (error) {
            commit('LOGOUT')
            throw error
        }
    },

    async register({ commit }, userData) {
        try {
            const response = await api.post('/auth/register', userData)
            return response.data
        } catch (error) {
            throw error
        }
    },

    async logout({ commit }) {
        commit('LOGOUT')
    },

    async loadUser({ commit }) {
        try {
            const token = localStorage.getItem('token')
            if (token) {
                commit('SET_TOKEN', token)
                const response = await api.get('/auth/me')
                commit('SET_USER', response.data)
            }
        } catch (error) {
            commit('LOGOUT')
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