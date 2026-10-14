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
const tariffs = ref([]);
const loading = ref(false);

const list = ref([4,7,3,9,7]);
const a=ref(12);
const b=ref(5);

const c = computed(() => {
  return a.value + b.value; 
})

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

onBeforeMount(async() => {
  await fetchTariffs()
})





</script>

<template>
<div>
  <input type="number" v-model="a"><br>
  <input type="number" v-model="b"><br>

  <b>{{ a }} + {{ b }}</b> <span> = {{ c }}</span>

  <button @click="onLoadClick">Загрузить</button>
  <div v-for="item in tariffs">
    {{ item.name }}
</div>
</div>
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
      <button class="btn btn-primary">
        Добавить
      </button>
    </div>
  </div>
</form>
</template>

<style scoped>
</style>
