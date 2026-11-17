<script setup>
import { onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

function emptySubscription() {
  return { user: "", tariff: "", expires_at: "", is_active: true }
}

const subscriptions = ref([])
const clients = ref([]) // для выпадающего списка юзеров
const tariffs = ref([])// для выпадающего списка тарифов
const subscriptionToAdd = ref(emptySubscription())
const subscriptionToEdit = ref({})
const loading = ref(false)

function formatDate(value) {
  return new Date(value).toLocaleString("ru-RU")
}

async function fetchSubscriptions() {
  loading.value = true
  const r = await axios.get("/api/subscriptions/")
  subscriptions.value = r.data
  loading.value = false
}

async function fetchClients() {
  const r = await axios.get("/api/clients/")
  clients.value = r.data
}

async function fetchTariffs() {
  const r = await axios.get("/api/tariffs/")
  tariffs.value = r.data
}

async function onSubscriptionAdd() {
  await axios.post("/api/subscriptions/", { ...subscriptionToAdd.value })
  subscriptionToAdd.value = emptySubscription()
  await fetchSubscriptions()
}

function onSubscriptionEditClick(subscription) {
  subscriptionToEdit.value = {
    ...subscription,
    expires_at: subscription.expires_at.slice(0, 16),
  }
}

async function onSubscriptionUpdate() {
  const { id, user, tariff, expires_at, is_active } = subscriptionToEdit.value
  await axios.put(`/api/subscriptions/${id}/`, { user, tariff, expires_at, is_active })
  await fetchSubscriptions()
}

async function onSubscriptionRemoveClick(subscription) {
  if (!confirm(`Удалить подписку ${subscription.user_name} ?`)) return
  await axios.delete(`/api/subscriptions/${subscription.id}/`)
  await fetchSubscriptions()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  await Promise.all([fetchSubscriptions(), fetchClients(), fetchTariffs()])
})
</script>

<template>
  <div class="container-fluid py-3">

    <form @submit.prevent.stop="onSubscriptionAdd">
      <div class="row g-2">
        <div class="col">
          <div class="form-floating">
            <select class="form-select" id="subUser" v-model="subscriptionToAdd.user" required>
              <option v-for="client in clients" :key="client.user" :value="client.user">{{ client.username }}</option>
            </select>
            <label for="subUser">Клиент</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" id="subTariff" v-model="subscriptionToAdd.tariff" required>
              <option v-for="tariff in tariffs" :key="tariff.id" :value="tariff.id">{{ tariff.name }}</option>
            </select>
            <label for="subTariff">Тариф</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="datetime-local" class="form-control" id="subExpires"
              v-model="subscriptionToAdd.expires_at" required />
            <label for="subExpires">Истекает</label>
          </div>
        </div>
        <div class="col-auto d-flex align-items-center">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="subActive" v-model="subscriptionToAdd.is_active" />
            <label class="form-check-label" for="subActive">Активна</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary h-100">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="subscription in subscriptions" :key="subscription.id"
      class="d-flex align-items-center border rounded p-3 mt-3">
      <div class="flex-grow-1 fs-5">
        {{ subscription.user_name }} - {{ subscription.tariff_name }}
      </div>
      <div class="me-4 text-muted">
        до {{ formatDate(subscription.expires_at) }}
        <span class="badge ms-2" :class="subscription.is_active ? 'bg-success' : 'bg-secondary'">
          {{ subscription.is_active ? "Активна" : "Неактивна" }}
        </span>
        <button class="btn btn-sm btn-outline-success ms-2" @click="onSubscriptionEditClick(subscription)"
          data-bs-toggle="modal" data-bs-target="#editSubscriptionModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger ms-2" @click="onSubscriptionRemoveClick(subscription)">
          <i class="bi bi-trash"></i>
        </button>
      </div>
    </div>

    <div class="modal fade" id="editSubscriptionModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактирование подписки</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <select class="form-select" id="editSubUser" v-model="subscriptionToEdit.user">
                <option v-for="client in clients" :key="client.user" :value="client.user">{{ client.username }}</option>
              </select>
              <label for="editSubUser">Клиент</label>
            </div>
            <div class="form-floating mb-2">
              <select class="form-select" id="editSubTariff" v-model="subscriptionToEdit.tariff">
                <option v-for="tariff in tariffs" :key="tariff.id" :value="tariff.id">{{ tariff.name }}</option>
              </select>
              <label for="editSubTariff">Тариф</label>
            </div>
            <div class="form-floating mb-2">
              <input type="datetime-local" class="form-control" id="editSubExpires"
                v-model="subscriptionToEdit.expires_at" required />
              <label for="editSubExpires">Истекает</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="editSubActive" v-model="subscriptionToEdit.is_active" />
              <label class="form-check-label" for="editSubActive">Активна</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="onSubscriptionUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
