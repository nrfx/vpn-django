<script setup>
import {computed, onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const tariffToAdd = ref({
  name: "",
  duration_days: 30,
  price: "",
  device_limit: 1,
});
const clients = ref([]);
const tariffs = ref([]);
const tariffToEdit = ref({});


const loading = ref(false);

const a=ref(12);
const b=ref(5);

const c = computed(() => {
  return a.value + b.value; 
})

async function fetchClients() {
  loading.value = true;
  const r = await axios.get("/api/clients/");
  console.log(r.data)
  clients.value = r.data;
  loading.value = false;
}

async function fetchTariffs() {
  loading.value = true;
  const r = await axios.get("/api/tariffs/");
  console.log(r.data)
  tariffs.value = r.data;
  loading.value = false;
}

async function onLoadClick() {
  await fetchTariffs()
}

async function onTariffAdd() {
  await axios.post("/api/tariffs/", {
    ...tariffToAdd.value,
  });
  await fetchTariffs(); // переподтягиваю список
  tariffToAdd.value = { name: "", duration_days: 30, price: "", device_limit: 1 };
}

function onTariffEditClick(tariff) {
  tariffToEdit.value = {...tariff};
}

async function onUpdateTariff() {
  await axios.put(`/api/tariffs/${tariffToEdit.value.id}/`, {
    ...tariffToEdit.value,
  });
  await fetchTariffs();
}
async function onTariffRemoveClick(tariff) {
  console.log("remove", tariff)
  await axios.delete(`/api/tariffs/${tariff.id}/`);
  await fetchTariffs(); // переподтягиваю список, 
}

onBeforeMount(async() => {
  await fetchTariffs();
})





</script>

<template>
<div class="container-fluid py-3">

<form @submit.prevent.stop="onTariffAdd">
  <div class="row">
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          id="tariffName"
          v-model="tariffToAdd.name"
          required
        />
        <label for="tariffName">Название</label>
      </div>
    </div>
    <div class="col-auto">
      <div class="form-floating">
        <input
          type="number"
          min="1"
          class="form-control"
          id="tariffDays"
          v-model="tariffToAdd.duration_days"
          required
        />
        <label for="tariffDays">Срок (дни)</label>
      </div>
    </div>
    <div class="col-auto">
      <div class="form-floating">
        <input
          type="number"
          min="0"
          step="0.01"
          class="form-control"
          id="tariffPrice"
          v-model="tariffToAdd.price"
          required
        />
        <label for="tariffPrice">Цена</label>
      </div>
    </div>
    <div class="col-auto">
      <div class="form-floating">
        <input
          type="number"
          min="1"
          class="form-control"
          id="tariffLimit"
          v-model="tariffToAdd.device_limit"
          required
        />
        <label for="tariffLimit">Лимит устройств</label>
      </div>
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">Добавить</button>
    </div>
  </div>
</form>

<div v-for="item in tariffs" :key="item.id" class="d-flex align-items-center border rounded p-3 mt-3">
  <div class="flex-grow-1 fs-5">{{ item.name }}</div>
  <div class="me-4 text-muted">
    {{ item.duration_days }} дн. · {{ item.price }} ₽ · {{ item.device_limit }} устр. 
    <button class="btn btn-sm btn-outline-success ms-2" @click="onTariffEditClick(item)" 
      data-bs-toggle="modal" 
      data-bs-target="#editTariffModal">
      <i class="bi bi-pen-fill"></i>
    </button>
    <button class="btn btn-sm btn-outline-danger ms-2" @click="onTariffRemoveClick(item)">
      <i class="bi bi-trash"></i>
    </button>
  </div>
</div>

<div class="modal fade" id="editTariffModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="editTariffModalLabel">Modal title</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" id="editName" v-model="tariffToEdit.name" required />
                  <label for="editName">Название</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <input type="number" min="1" class="form-control" id="editDays" v-model="tariffToEdit.duration_days"
                    required />
                  <label for="editDays">Срок (дни)</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <input type="number" min="0" step="0.01" class="form-control" id="editPrice"
                    v-model="tariffToEdit.price" required />
                  <label for="editPrice">Цена</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <input type="number" min="1" class="form-control" id="editLimit" v-model="tariffToEdit.device_limit"
                    required />
                  <label for="editLimit">Лимит устройств</label>
                </div>
              </div>
            </div>
   
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateTariff">Сохранить</button>
      </div>
    </div>
  </div>
</div>
</div>
</template>

<style scoped>
</style>
