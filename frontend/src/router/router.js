import { createRouter, createWebHistory } from "vue-router";

// Pages
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: Home,
            meta: { isGuest: true }
        },
        {
            path: "/login",
            name: "login",
            component: Login,
            meta: { isGuest: true }
        },
    ],

});

router.beforeEach((to, from, next) => {
    console.log(to.meta);
    next();
});

export default router;