import { createStore } from 'vuex'
import auth from './modules/auth'
import certs from './modules/certs'

export default createStore({
    modules: {
        auth,
        certs
    }
})
