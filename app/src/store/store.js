import Vue from 'vue';
import Vuex from "vuex";
import VuexPersist from 'vuex-persist'
const axios = require('axios');
const firebase = require('../firebaseConfig.js')

Vue.use(Vuex);

const vuexPersist = new VuexPersist({
    key: 'my-app',
    storage: window.localStorage
})

export default new Vuex.Store({
    plugins: [vuexPersist.plugin],
    state:{
        user: null
    },
    mutations: {
        ['SET_USER'](state, payload){
            state.user = payload;
        }
    },
    actions: {
        async postNewUser({ commit }, payload) {
            try {
                //post new sign up
                let firebase_user = await firebase.auth.createUserWithEmailAndPassword(payload.email, payload.password)
                await axios.post("http://localhost:5000/register",{
                    'firebase_id': firebase_user.user.uid,
                    'user_name': payload.username,
                    'candidate_id': payload.mimic_candidate.user_id
                });
                let response = await axios.get("http://localhost:5000/user-information", {
                    params: {
                        'firebase_id': firebase_user.user.uid
                    }
                }); 

                commit('SET_USER', response.data.user);
                return Promise.resolve(200);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async postLogin({ commit }, payload) {
            try {
                let authed_user = await firebase.auth.signInWithEmailAndPassword(payload.email, payload.password);
                let response = await axios.get("http://localhost:5000/user-information", {
                    params: {
                        'firebase_id': authed_user.user.uid
                    }
                }); 
                commit('SET_USER', response.data.user)
                return Promise.resolve(200);
            } catch (error) {
                return Promise.reject(error);
            }
        },
        async postLogout({ commit }) {
            await firebase.auth.signOut()
            commit('SET_USER', null)
        },

        async autoSignIn( { commit }, payload) {
            let response = await axios.get("http://localhost:5000/user-information", {
                params: {
                    'firebase_id': payload.user.uid
                }
            }); 
            commit('SET_USER', response.data.user);
        }
    },
    getters: {
        user (state) {
            return state.user;
        },
    }
});