// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'Home',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/HomeView.vue'
                    ),
            },
        ],
    },
    {
        path: '/history',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'History',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/HistoryView.vue'
                    ),
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
