import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Auth/Login.vue'),
        meta: { guest: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/Auth/Register.vue'),
        meta: { guest: true }
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/certificates',
        name: 'Certificates',
        component: () => import('@/views/Certificates/List.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/certificates/create',
        name: 'CreateCertificate',
        component: () => import('@/views/Certificates/Create.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/certificates/:id',
        name: 'CertificateDetail',
        component: () => import('@/views/Certificates/Detail.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/certificates/:id/renew',
        name: 'RenewCertificate',
        component: () => import('@/views/Certificates/Renew.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '*',
        redirect: '/dashboard'
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

// Flag to track if user has been loaded
let userLoaded = false

router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const guest = to.matched.some(record => record.meta.guest)

    // Only load user if not already loaded
    if (!userLoaded) {
        try {
            await store.dispatch('auth/loadUser')
            userLoaded = true
        } catch (error) {
            // Ignore errors on initial load
        }
    }
    
    const isAuthenticated = store.state.auth.isAuthenticated

    if (requiresAuth && !isAuthenticated) {
        next('/login')
    } else if (guest && isAuthenticated) {
        next('/dashboard')
    } else {
        next()
    }
})

export default router