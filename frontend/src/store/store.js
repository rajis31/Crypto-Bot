import { createStore } from 'vuex';

const store = createStore({
    state:{
        isLoggedIn: false,
        api: "http://127.0.0.1:8081/api",
    },
    getters: {
        getIsLoggedIn(state){
            return state.isLoggedIn;
        },
        getApiUrl(state){
            return state.apiUrl;
        }
    },
    mutations:{
        setIsLoggedIn(state){
            state.isLoggedIn = true;
        }
    }
});


export default store;