<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const rooms = ref([])
const room_id = ref(1)
const out = ref(null)
const error = ref('')
onMounted(async () => { rooms.value = (await getJSON('/api/rooms')).items })
const run = async () => {
  out.value = null; error.value = ''
  try { out.value = await postJSON('/api/estimate', { room_id: room_id.value, persist: true }) }
  catch (e) { try { error.value = JSON.parse(e.message).detail || e.message } catch { error.value = e.message } }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间 <select v-model.number="room_id"><option v-for="r in rooms" :key="r.id" :value="r.id">{{ r.name }}</option></select></label>
<button @click="run">估算</button>
<p v-if="error" class="error">整单拒绝：{{ error }}（未写记录）</p>
<template v-if="out">
<p>毛面积 {{ out.gross_m2 }} m² · 扣除合计 {{ out.openings_m2 }} m² · 净面积 {{ out.net_m2 }} m² · {{ out.liters }} 升 · {{ out.coats }} 遍</p>
<table><tr><th>洞口</th><th>洞口</th><th>留边</th><th>内口</th><th>扣除 m²</th></tr>
<tr v-for="i in out.opening_items" :key="i.id"><td>{{ i.kind }}</td><td>{{ i.w }}×{{ i.h }}</td><td>{{ i.trim }}</td><td>{{ i.inner_w }}×{{ i.inner_h }}</td><td>{{ i.deduct_m2 }}</td></tr></table>
</template></div></template>
