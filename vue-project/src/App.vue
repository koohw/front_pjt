<template>
  <header>
    <AppNavbar />
  </header>
  <RouterView />
  <Footer />
</template>

<script setup>
import { RouterView, RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import AppNavbar from "./components/Common/AppNavbar.vue";
import Footer from "./components/Common/Footer.vue";

const store = useCounterStore();

const logOut = function () {
  store.logOut();
};
</script>

<style scoped></style>
