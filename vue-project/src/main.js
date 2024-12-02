import "./assets/main.css";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue"; // Vue 3에서 createApp 사용
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import { createVuetify } from "vuetify";  // Vuetify 3에서 createVuetify 사용
import BootstrapVue3 from "bootstrap-vue-3";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";
import "vuetify/styles";  // Vuetify 스타일 파일 import

// Vuetify 인스턴스 생성
const vuetify = createVuetify();  // Vuetify 3 인스턴스 생성

// Vue 앱 인스턴스를 생성
const app = createApp(App);

// Pinia store 설정
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

// 앱에 Vuetify, Pinia, router, BootstrapVue3를 사용하도록 설정
app.use(vuetify);  // Vuetify 플러그인 사용
app.use(pinia);
app.use(router);
app.use(BootstrapVue3);

// 앱을 DOM에 마운트
app.mount("#app");
