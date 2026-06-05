<template>
  <label class="block">
    <span class="text-xs font-bold uppercase tracking-street">{{ label }}</span>
    <component
      :is="type === 'textarea' ? 'textarea' : 'input'"
      :value="modelValue"
      :type="type === 'textarea' ? undefined : (type || 'text')"
      :rows="type === 'textarea' ? 4 : undefined"
      class="mt-2 w-full border-2 border-ink bg-chalk px-3 py-2 text-sm"
      @input="onInput"
    />
  </label>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  label: string
  type?: 'text' | 'textarea' | 'number' | 'email' | 'url' | 'password'
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLInputElement).value)
}
</script>
