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
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        } else {
            localStorage.removeItem('token')
            delete axios.defaults.headers.common['Authorization']
        }
    },
    LOGOUT(state) {
        state.user = null
        state.token = null
        state.isAuthenticated = false
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
    }
}

const actions = {
    async login({ commit }, credentials) {
        try {
            const response = await axios.post('/auth/login', credentials)
            commit('SET_TOKEN', response.data.token)
            commit('SET_USER', response.data.user)
            return response.data.user
        } catch (error) {
            commit('LOGOUT')
            throw error
        }
    },

    async register({ commit }, userData) {
        const response = await axios.post('/auth/register', userData)
        return response.data
    },

    async logout({ commit }) {
        commit('LOGOUT')
    },

    async loadUser({ commit }) {
        try {
            const token = localStorage.getItem('token')
            if (token) {
                commit('SET_TOKEN', token)
                const response = await axios.get('/auth/me')  // 需要实现此端点
                commit('SET_USER', response.data)
            }
        } catch (error) {
            commit('LOGOUT')
        }
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}
