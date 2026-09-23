<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON, patchJSON } from '../api'
const detail = ref(null)
const est = ref(null)
const trims = ref({})
const error = ref('')
const message = e => { try { return JSON.parse(e.message).detail || e.message } catch { return e.message } }
const load = async () => {
  detail.value = await getJSON('/api/rooms/2')
  trims.value = Object.fromEntries(detail.value.openings.map(o => [o.id, o.trim ?? 0]))
  est.value = await postJSON('/api/estimate', { room_id: 2, persist: false }).catch(e => { error.value = message(e); return null })
}
const saveTrim = async o => {
  error.value = ''
  try { await patchJSON(`/api/openings/${o.id}/trim`, { trim: +trims.value[o.id] }); await load() }
  catch (e) { error.value = message(e) }
}
const itemOf = id => est.value?.opening_items.find(i => i.id === id) || {}
onMounted(load)
</script>
<template><div class="page"><h1>洞口示意（种子房间）</h1>
<p v-if="est">墙面 {{ est.gross_m2 }} m² · 扣除合计 {{ est.openings_m2 }} m² · 净面积 {{ est.net_m2 }} m²</p>
<p v-if="error" class="error">拒绝：{{ error }}</p>
<table v-if="detail"><tr><th>洞口</th><th>洞口宽×高</th><th>留边宽 (m)</th><th>内口宽×高</th><th>扣除 m²</th><th></th></tr>
<tr v-for="o in detail.openings" :key="o.id">
  <td>{{ o.kind }}</td><td>{{ o.w }}×{{ o.h }}</td>
  <td><input v-model.number="trims[o.id]" type="number" min="0" step="0.01" /></td>
  <td>{{ itemOf(o.id).inner_w ?? '—' }}×{{ itemOf(o.id).inner_h ?? '—' }}</td>
  <td>{{ itemOf(o.id).deduct_m2 ?? '—' }}</td>
  <td><button @click="saveTrim(o)">保存留边</button></td>
</tr></table>
</div></template>
