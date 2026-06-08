<template>
  <div class="block">
    <span class="text-xs font-bold uppercase tracking-street">{{ label }}</span>

    <div class="mt-3 flex flex-wrap gap-3">
      <label class="btn-secondary cursor-pointer !py-2 !text-[10px]">
        {{ uploading ? 'Envoi...' : 'Choisir une photo' }}
        <input
          type="file"
          accept="image/*"
          class="hidden"
          :disabled="uploading"
          @change="onFileSelected"
        >
      </label>
      <button
        v-if="modelValue"
        type="button"
        class="border-2 border-ink px-3 py-2 text-[10px] font-bold uppercase"
        @click="clearImage"
      >
        Retirer
      </button>
    </div>

    <div v-if="displayUrl" class="mt-4">
      <span class="text-xs font-bold uppercase tracking-street">URL de l'image</span>
      <p class="mt-2 break-all border-2 border-ink bg-chalk px-3 py-2 text-xs text-smoke">
        {{ displayUrl }}
      </p>
    </div>

    <details class="mt-4">
      <summary class="cursor-pointer text-xs font-bold uppercase tracking-street">
        URL externe (optionnel)
      </summary>
      <AdminField
        v-model="urlValue"
        class="mt-3"
        :label="urlLabel"
        type="text"
      />
    </details>

    <div v-if="$slots['site-preview']" class="mt-8">
      <p class="text-xs font-bold uppercase tracking-street">Aperçu sur le site</p>
      <div class="mt-4 max-w-md pointer-events-none">
        <slot name="site-preview" />
      </div>
    </div>

    <div v-else-if="previewUrl" class="mt-8">
      <p class="text-xs font-bold uppercase tracking-street">Aperçu</p>
      <div class="mt-4 overflow-hidden border-2 border-ink">
        <img :src="previewUrl" :alt="label" class="max-h-56 w-full object-cover">
      </div>
    </div>

    <p v-if="error" class="mt-2 text-xs font-bold text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { formatAdminError, normalizeImageUrlForStorage, resolveImageUrl } from '~/composables/useAssetUrl'

const props = withDefaults(defineProps<{
  modelValue: string
  label: string
  folder?: 'settings' | 'news' | 'vehicles' | 'services'
  urlLabel?: string
}>(), {
  folder: 'settings',
  urlLabel: 'Coller une URL https://...',
})

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const uploading = ref(false)
const error = ref('')
const localPreviewUrl = ref('')

const urlValue = computed({
  get: () => props.modelValue,
  set: (value: string) => emit('update:modelValue', normalizeImageUrlForStorage(value)),
})

const previewUrl = computed(() => localPreviewUrl.value || resolveImageUrl(props.modelValue) || '')
const displayUrl = computed(() => resolveImageUrl(props.modelValue))

onBeforeUnmount(() => {
  if (localPreviewUrl.value) {
    URL.revokeObjectURL(localPreviewUrl.value)
  }
})

async function onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return

  if (localPreviewUrl.value) {
    URL.revokeObjectURL(localPreviewUrl.value)
  }
  localPreviewUrl.value = URL.createObjectURL(file)

  uploading.value = true
  error.value = ''

  try {
    const result = await adminUpload(file, props.folder)
    emit('update:modelValue', result.url)
  } catch (err) {
    error.value = formatAdminError(err)
    URL.revokeObjectURL(localPreviewUrl.value)
    localPreviewUrl.value = ''
  } finally {
    uploading.value = false
  }
}

function clearImage() {
  if (localPreviewUrl.value) {
    URL.revokeObjectURL(localPreviewUrl.value)
    localPreviewUrl.value = ''
  }
  emit('update:modelValue', '')
  error.value = ''
}
</script>
