<template>
  <div class="sticky bottom-0 z-10 -mx-1 border-t-2 border-ink bg-chalk/95 px-1 py-4 backdrop-blur-sm">
    <p v-if="message" class="mb-3 text-sm font-bold text-green-700">{{ message }}</p>
    <p v-if="error" class="mb-3 text-sm font-bold text-red-600">{{ error }}</p>
    <button type="submit" class="btn-primary" :disabled="saving">
      {{ saving ? 'Enregistrement...' : 'Enregistrer les modifications' }}
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string
  error: string
  saving: boolean
}>()
</script>
