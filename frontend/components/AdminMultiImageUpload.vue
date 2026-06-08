<template>
  <div class="block">
    <span class="text-xs font-bold uppercase tracking-street">{{ label }}</span>
    <p v-if="hint" class="mt-1 text-xs text-smoke">{{ hint }}</p>

    <div class="mt-3 flex flex-wrap gap-3">
      <label class="btn-secondary cursor-pointer !py-2 !text-[10px]">
        {{ uploading ? 'Envoi...' : 'Ajouter des photos' }}
        <input
          type="file"
          accept="image/*"
          multiple
          class="hidden"
          :disabled="uploading"
          @change="onFilesSelected"
        >
      </label>
      <button
        v-if="modelValue.length"
        type="button"
        class="border-2 border-ink px-3 py-2 text-[10px] font-bold uppercase"
        @click="clearAll"
      >
        Tout retirer
      </button>
    </div>

    <ul v-if="modelValue.length" class="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <li
        v-for="(url, index) in modelValue"
        :key="`${url}-${index}`"
        class="overflow-hidden border-2 border-ink bg-chalk"
      >
        <div class="relative aspect-[16/10]">
          <img :src="resolveImageUrl(url)" :alt="`${label} ${index + 1}`" class="h-full w-full object-cover">
          <span class="absolute left-2 top-2 bg-ink px-2 py-0.5 text-[10px] font-bold uppercase tracking-street text-chalk">
            {{ index + 1 }}
          </span>
        </div>
        <div class="flex items-center justify-between gap-2 border-t-2 border-ink p-2">
          <div class="flex gap-1">
            <button
              type="button"
              class="border border-ink px-2 py-1 text-[10px] font-bold uppercase disabled:opacity-30"
              :disabled="index === 0"
              @click="moveImage(index, -1)"
            >
              ↑
            </button>
            <button
              type="button"
              class="border border-ink px-2 py-1 text-[10px] font-bold uppercase disabled:opacity-30"
              :disabled="index === modelValue.length - 1"
              @click="moveImage(index, 1)"
            >
              ↓
            </button>
          </div>
          <button
            type="button"
            class="text-[10px] font-bold uppercase text-red-600"
            @click="removeImage(index)"
          >
            Retirer
          </button>
        </div>
      </li>
    </ul>

    <details class="mt-4">
      <summary class="cursor-pointer text-xs font-bold uppercase tracking-street">
        URL externe (optionnel)
      </summary>
      <div class="mt-3 flex flex-wrap gap-2">
        <input
          v-model="externalUrl"
          type="text"
          class="min-w-0 flex-1 border-2 border-ink bg-chalk px-3 py-2 text-sm"
          :placeholder="urlLabel"
        >
        <button
          type="button"
          class="border-2 border-ink px-3 py-2 text-[10px] font-bold uppercase"
          @click="addExternalUrl"
        >
          Ajouter
        </button>
      </div>
    </details>

    <div v-if="$slots['site-preview']" class="mt-8">
      <p class="text-xs font-bold uppercase tracking-street">Aperçu sur le site</p>
      <div class="mt-4 max-w-md pointer-events-none">
        <slot name="site-preview" />
      </div>
    </div>

    <p v-if="error" class="mt-2 text-xs font-bold text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { formatAdminError, normalizeImageUrlForStorage, resolveImageUrl } from '~/composables/useAssetUrl'

const props = withDefaults(defineProps<{
  modelValue: string[]
  label: string
  hint?: string
  folder?: 'settings' | 'news' | 'vehicles' | 'services'
  urlLabel?: string
}>(), {
  folder: 'vehicles',
  urlLabel: 'Coller une URL https://...',
})

const emit = defineEmits<{ 'update:modelValue': [value: string[]] }>()

const uploading = ref(false)
const error = ref('')
const externalUrl = ref('')

function updateImages(urls: string[]) {
  emit('update:modelValue', urls.map(url => normalizeImageUrlForStorage(url)).filter(Boolean))
}

async function onFilesSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const files = input.files ? Array.from(input.files) : []
  input.value = ''
  if (!files.length) return

  uploading.value = true
  error.value = ''

  const uploaded: string[] = []
  try {
    for (const file of files) {
      const result = await adminUpload(file, props.folder)
      uploaded.push(result.url)
    }
    updateImages([...props.modelValue, ...uploaded])
  } catch (err) {
    error.value = formatAdminError(err)
    if (uploaded.length) {
      updateImages([...props.modelValue, ...uploaded])
    }
  } finally {
    uploading.value = false
  }
}

function removeImage(index: number) {
  updateImages(props.modelValue.filter((_, itemIndex) => itemIndex !== index))
}

function moveImage(index: number, direction: -1 | 1) {
  const nextIndex = index + direction
  if (nextIndex < 0 || nextIndex >= props.modelValue.length) return
  const urls = [...props.modelValue]
  const [item] = urls.splice(index, 1)
  urls.splice(nextIndex, 0, item)
  updateImages(urls)
}

function addExternalUrl() {
  const url = externalUrl.value.trim()
  if (!url) return
  updateImages([...props.modelValue, url])
  externalUrl.value = ''
}

function clearAll() {
  updateImages([])
  error.value = ''
}
</script>
