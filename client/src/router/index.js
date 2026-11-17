import { createRouter, createWebHistory } from 'vue-router';
import TariffsView from '../views/TariffsView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MainView",
      component: () => import("../views/MainView.vue"),
    },
    {
      path: "/tariffs",
      name: "TariffsView",
      component: () => import("../views/TariffsView.vue"),
    },
    {
      path: "/subscriptions",
      name: "SubscriptionsView",
      component: () => import("../views/SubscriptionsView.vue"),
    },
    {
      path: "/clients",
      name: "ClientsView",
      component: () => import("../views/ClientsView.vue"), 
    }
  ]
})

export default router
