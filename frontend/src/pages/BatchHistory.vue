<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
</script>
<template><div class="page"><h1>估算记录</h1>
<table><tr><th>#</th><th>时间</th><th>房间</th><th>扣除合计 m²</th><th>净面积 m²</th><th>升数</th></tr>
<template v-for="h in items" :key="h.id">
<tr><td>#{{ h.id }}</td><td>{{ h.created_at }}</td><td>{{ h.room_id }}</td>
<td>{{ h.result?.openings_m2 ?? '—' }}</td><td>{{ h.result?.net_m2 ?? '—' }}</td><td>{{ h.result?.liters ?? '—' }}</td></tr>
<tr v-if="h.result?.opening_items?.length"><td></td><td colspan="5">
<span v-for="(i, idx) in h.result.opening_items" :key="idx" class="tag">{{ i.kind }} 留边{{ i.trim }} 内口{{ i.inner_w }}×{{ i.inner_h }} 扣{{ i.deduct_m2 }}</span>
</td></tr>
</template></table>
</div></template>
