<script setup>
import { onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const roles = [
  { value: 0, label: "Пользователь" },
  { value: 1, label: "Администратор" },
]

function emptyClient() {
  return { username: "", email: "", password: "", balance: 0, role: 0 }
}

const clients = ref([])
const clientToAdd = ref(emptyClient())
const clientToEdit = ref({})
const loading = ref(false)

function roleLabel(value) {
  return roles.find(r => r.value === value)?.label
}

async function fetchClients() {
  loading.value = true
  const r = await axios.get("/api/clients/")
  clients.value = r.data
  loading.value = false
}

async function onClientAdd() {
  await axios.post("/api/clients/", { ...clientToAdd.value })
  clientToAdd.value = emptyClient()
  await fetchClients()
}

function onClientEditClick(client) {
  // пароль пустой: если не заполнить, останется прежним
  clientToEdit.value = { ...client, password: "" }
}

async function onClientUpdate() {
  const { password, ...rest } = clientToEdit.value
  const body = password ? { ...rest, password } : rest
  await axios.put(`/api/clients/${clientToEdit.value.id}/`, body)
  await fetchClients()
}

async function onClientRemoveClick(client) {
  if (!confirm(`Удалить клиента ${client.username} вместе с подписками и платежами?`)) return
  await axios.delete(`/api/clients/${client.id}/`)
  await fetchClients()
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  await fetchClients()
})
</script>

<template>
  <div class="container-fluid py-3">

    <form @submit.prevent.stop="onClientAdd">
      <div class="row g-2">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" id="clientUsername" v-model="clientToAdd.username" required />
            <label for="clientUsername">Логин</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="email" class="form-control" id="clientEmail" v-model="clientToAdd.email" />
            <label for="clientEmail">Email</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="password" class="form-control" id="clientPassword" v-model="clientToAdd.password" required />
            <label for="clientPassword">Пароль</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-floating">
            <input type="number" min="0" step="0.01" class="form-control" id="clientBalance"
              v-model="clientToAdd.balance" required />
            <label for="clientBalance">Баланс</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-floating">
            <select class="form-select" id="clientRole" v-model="clientToAdd.role">
              <option v-for="role in roles" :key="role.value" :value="role.value">{{ role.label }}</option>
            </select>
            <label for="clientRole">Роль</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary h-100">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="client in clients" :key="client.id"
      class="d-flex align-items-center border rounded p-3 mt-3">
      <div class="flex-grow-1">
        <div class="fs-5">{{ client.username }}</div>
        <div class="text-muted small">{{ client.email || "email не указан" }}</div>
      </div>
      <div class="me-4 text-muted">
        {{ client.balance }} ₽ · {{ roleLabel(client.role) }} ·
        подписок: {{ client.active_subscriptions }}
        <button class="btn btn-sm btn-outline-success ms-2" @click="onClientEditClick(client)"
          data-bs-toggle="modal" data-bs-target="#editClientModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger ms-2" @click="onClientRemoveClick(client)">
          <i class="bi bi-trash"></i>
        </button>
      </div>
    </div>

    <div class="modal fade" id="editClientModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактирование клиента</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <input type="text" class="form-control" id="editClientUsername" v-model="clientToEdit.username" required />
              <label for="editClientUsername">Логин</label>
            </div>
            <div class="form-floating mb-2">
              <input type="email" class="form-control" id="editClientEmail" v-model="clientToEdit.email" />
              <label for="editClientEmail">Email</label>
            </div>
            <div class="form-floating mb-2">
              <input type="password" class="form-control" id="editClientPassword" v-model="clientToEdit.password"
                placeholder="Новый пароль" />
              <label for="editClientPassword">Новый пароль (пусто — не менять)</label>
            </div>
            <div class="row g-2">
              <div class="col">
                <div class="form-floating">
                  <input type="number" min="0" step="0.01" class="form-control" id="editClientBalance"
                    v-model="clientToEdit.balance" required />
                  <label for="editClientBalance">Баланс</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select class="form-select" id="editClientRole" v-model="clientToEdit.role">
                    <option v-for="role in roles" :key="role.value" :value="role.value">{{ role.label }}</option>
                  </select>
                  <label for="editClientRole">Роль</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
              @click="onClientUpdate">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
