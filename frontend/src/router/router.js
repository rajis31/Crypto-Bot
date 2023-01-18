import { createRouter, createWebHistory } from "vue-router";

// Pages
import Home from "../pages/Home.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: Home,
            meta: { isGuest: true }
        },
    ],

});

router.beforeEach((to, from, next) => {
    console.log(to.meta);
    next();
});

export default router;