<script setup>
import { getRelativeTime } from '@/utils'
import { computed } from 'vue'
import { onUnmounted } from 'vue'
import { onMounted } from 'vue'
import { ref } from 'vue'

const props = defineProps(['time'])

const polling = ref(null)
const relativeTime = ref('')

const timeFormatOptions = new Intl.DateTimeFormat(navigator.language, {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
})
const absoluteTime = computed(() => timeFormatOptions.format(props.time))

onMounted(() => {
    polling.value = setInterval(
        () => (relativeTime.value = getRelativeTime(props.time))
    )
})

onUnmounted(() => {
    clearInterval(polling.value)
})
</script>

<template>
    <v-tooltip>
        {{ absoluteTime }}
        <template v-slot:activator="{ props }">
            <span
                v-bind="props"
                class="text-subtitle-1"
            >
                {{ relativeTime }}
            </span>
        </template>
    </v-tooltip>
</template>
