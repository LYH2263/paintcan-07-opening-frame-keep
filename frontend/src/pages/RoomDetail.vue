<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON } from '../api'
import OpeningEditor from '../components/OpeningEditor.vue'
const route = useRoute()
const room = ref(null)
const load = async () => { room.value = (await getJSON(`/api/rooms/${route.params.id}`)).room }
onMounted(load); watch(() => route.params.id, load)
</script>
<template><div class="page" v-if="room">
  <h1>{{ room.name }}</h1>
  <p>墙面 {{ room.length }}×{{ room.width }}×{{ room.height }} m</p>
  <OpeningEditor :room-id="route.params.id" />
</div></template>
