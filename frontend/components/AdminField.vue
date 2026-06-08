<template>
  <label class="block">
    <span class="text-xs font-bold uppercase tracking-street">{{ label }}</span>
    <component
      :is="type === 'textarea' ? 'textarea' : 'input'"
      :value="modelValue"
      :placeholder="placeholder"
      :type="type === 'textarea' ? undefined : (type || 'text')"
      :rows="type === 'textarea' ? 4 : undefined"
      class="mt-2 w-full border-2 border-ink bg-chalk px-3 py-2 text-sm placeholder:text-smoke/60"
      @input="onInput"
    />
    <p v-if="hint" class="mt-1 text-xs text-smoke">{{ hint }}</p>
  </label>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  label: string
  type?: 'text' | 'textarea' | 'number' | 'email' | 'url' | 'password'
  placeholder?: string
  hint?: string
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLInputElement).value)
}
</script>
