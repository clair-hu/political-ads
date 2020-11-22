import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from "vue-router";
import App from './App.vue';
import store  from "./store/store.js";
import axios from 'axios'
import VueAxios from 'vue-axios'
import vSelect from "vue-select";

// Components
import HomePage from "./components/HomePage.vue";
import LoginPage from "./components/LoginPage.vue";
import SignUpPage from "./components/SignUpPage.vue";
import DashboardPage from "./components/DashboardPage.vue";
import SpendingPage from "./components/SpendingPage.vue";
import ChallengePage from "./components/ChallengePage.vue";
import 'vue-select/dist/vue-select.css';
import VueEditableGrid from 'vue-editable-grid';
import 'vue-editable-grid/dist/VueEditableGrid.css';
import Grid from 'gridjs-vue';

//Register Third Party components
Vue.component("v-select", vSelect);
Vue.component('vue-editable-grid', VueEditableGrid);

Vue.use(Vuex);
Vue.use(VueRouter);
Vue.use(VueAxios, axios);
Vue.use(Grid);

Vue.config.productionTip = false


function authGuard(to, from, next) {
  if(store.getters.user){
    next()
  }else{
    next('/')
  }
}

function loggedInUserRedirect(to, from, next) {
  //console.log(store.getters.user)
  if(to.path === '/' && store.getters.user){
    next('/dashboard')
  }else{
    next()
  }
}

const routes = [
  { path: '/', component: HomePage, beforeEnter: loggedInUserRedirect},
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignUpPage },
  { path: '/dashboard', component: DashboardPage, beforeEnter: authGuard },
  { path: '/spend', component: SpendingPage, beforeEnter: authGuard},
  { path: '/challenge', component: ChallengePage, beforeEnter: authGuard}
];
const router = new VueRouter({
  routes
});

new Vue({
  router,
  store,
  render: h => h(App),
  created() {
    //dispatch action to get all games
  }
}).$mount('#app')