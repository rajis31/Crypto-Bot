import { createApp } from 'vue';
import './style.css';
import router from "../src/router/router";
import store from "../src/store/store";
import App from './App.vue';


/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faAlignJustify, faHeart, faFire, faStar } from '@fortawesome/free-solid-svg-icons';
library.add(
            faAlignJustify,
            faHeart,
            faFire,
            faStar
          );


createApp(App)
    .component('font-awesome-icon', FontAwesomeIcon)
    .use(router)
    .use(store)
    .mount('#app');