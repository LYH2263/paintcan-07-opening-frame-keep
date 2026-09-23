<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON, patchJSON } from '../api'
const route = useRoute()
const detail = ref(null)
const est = ref(null)
const trims = ref({})
const error = ref('')
const load = async () => {
  error.value = ''
  detail.value = await getJSON(`/api/rooms/${route.params.id}`)
  trims.value = Object.fromEntries(detail.value.openings.map(o => [o.id, o.trim ?? 0]))
  est.value = await postJSON('/api/estimate', { room_id: +route.params.id, persist: false }).catch(e => { error.value = message(e); return null })
}
const message = e => {
  try { return JSON.parse(e.message).detail || e.message } catch { return e.message }
}
const saveTrim = async o => {
  error.value = ''
  try {
    await patchJSON(`/api/openings/${o.id}/trim`, { trim: +trims.value[o.id] })
    await load()  // 当场再测才用新留边
  } catch (e) { error.value = message(e) }
}
onMounted(load); watch(() => route.params.id, load)
</script>
<template><div class="page" v-if="detail"><h1>{{ detail.room.name }}</h1>
<p>毛面积 {{ est?.gross_m2 }} m² · 扣除合计 {{ est?.openings_m2 }} m² · 净面积 {{ est?.net_m2 }} m² · 需漆 <span class="hero-num">{{ est?.liters }} L</span></p>
<p v-if="error" class="error">拒绝：{{ error }}（未估算、未记录）</p>
<table><tr><th>洞口</th><th>宽×高</th><th>留边宽 (m)</th><th>内口</th><th>扣除 m²</th><th></th></tr>
<tr v-for="o in detail.openings" :key="o.id">
  <td>{{ o.kind }}</td><td>{{ o.w }}×{{ o.h }}</td>
  <td><input v-model.number="trims[o.id]" type="number" min="0" step="0.01" /></td>
  <td v-if="est">{{ (est.opening_items.find(i => i.id === o.id) || {}).inner_w }}×{{ (est.opening_items.find(i => i.id === o.id) || {}).inner_h }}</td><td v-else>—</td>
  <td>{{ (est?.opening_items.find(i => i.id === o.id) || {}).deduct_m2 ?? '—' }}</td>
  <td><button @click="saveTrim(o)">保存留边</button></td>
</tr></table>
</div></template>
