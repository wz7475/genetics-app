<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { downloadFile } from '@/api/downloadFile'
import { useFileStore } from '@/store'
import AnnotateButton from '@/components/AnnotateButton.vue'
import TimeDisplay from '@/components/TimeDisplay.vue'

const fileStore = useFileStore()

const colorMap = {
    ready: 'success',
    pending: 'info',
    processing: 'deep-purple',
    expired: 'grey',
}

const polling = ref(null)

const timeKey = ref(0)
const timePolling = ref(null)

const singlePercentage = (subtask) => {
    return (100 * subtask.completed) / subtask.total
}

const totalPercentage = (file) => {
    const { completed, total } = Object.values(file.subtasks).reduce(
        (prev, curr) => ({
            completed: prev.completed + curr.completed,
            total: prev.total + curr.total,
        }),
        { completed: 0, total: 0 }
    )

    return (100 * completed) / total
}

onMounted(async () => {
    await fileStore.reloadFiles()
    polling.value = setInterval(fileStore.reloadFiles, 5000)
    timePolling.value = setInterval(() => timeKey.value++, 1000)
})

onUnmounted(() => {
    clearInterval(polling.value)
    clearInterval(timePolling.value)
})
</script>

<template>
    <v-container class="fill-height justify-center d-flex flex-column">
        <div
            class="w-100 d-flex justify-start align-center"
            style="max-width: 1000px"
        >
            <v-btn
                icon="mdi-arrow-left"
                variant="text"
                to="/"
            ></v-btn>

            <v-img
                max-width="60"
                height="60"
                src="@/assets/logo.svg"
            />
            <h1 class="text-h3 font-weight-bold">Gene annotation</h1>
        </div>
        <v-sheet
            class="pa-6 ga-4 d-flex flex-column w-100"
            style="max-width: 1000px"
            elevation="8"
            rounded
        >
            <div class="d-flex ga-8 align-center">
                <h4 class="text-h5 font-weight-bold ml-4">
                    Previous annotations
                </h4>
                <v-progress-circular
                    v-if="!fileStore.ready"
                    indeterminate
                    class="ma-auto"
                ></v-progress-circular>

                <v-spacer />

                <AnnotateButton />
            </div>
            <v-sheet
                v-for="(file, index) in fileStore.files"
                :key="file.name + timeKey"
                elevation="8"
                rounded
                :color="colorMap[file.status]"
            >
                <div
                    class="d-flex pa-1 px-4 align-center"
                    style="min-height: 56px"
                >
                    <span class="text-h6 mr-2">{{ file.name }}</span>
                    <TimeDisplay :time="file.time" />

                    <v-spacer />

                    <v-tooltip v-if="file.status === 'expired'">
                        <p>Expired</p>
                        <template v-slot:activator="{ props, isActive }">
                            <v-btn
                                v-bind="props"
                                density="compact"
                                size="x-large"
                                variant="text"
                                class="pr-1"
                                :icon="
                                    isActive ? 'mdi-close' : 'mdi-emoticon-sad'
                                "
                                @click="fileStore.removeFile(index)"
                            ></v-btn>
                        </template>
                    </v-tooltip>

                    <v-tooltip v-if="file.status === 'pending'">
                        <p>Pending...</p>
                        <template v-slot:activator="{ props }">
                            <div v-bind="props">
                                <v-progress-circular
                                    class="mr-2"
                                    indeterminate
                                ></v-progress-circular>
                            </div>
                        </template>
                    </v-tooltip>

                    <v-tooltip v-if="file.status === 'processing'">
                        <p>Processing...</p>
                        <p
                            v-for="[algorithm, subtask] in Object.entries(
                                file.subtasks
                            )"
                            :key="algorithm"
                        >
                            - {{ algorithm }}:
                            {{ singlePercentage(subtask).toFixed(1) }}%
                        </p>
                        <template v-slot:activator="{ props }">
                            <div v-bind="props">
                                <span class="mr-4">
                                    {{ totalPercentage(file).toFixed(1) }}%
                                </span>

                                <v-progress-circular
                                    class="mr-2"
                                    :model-value="totalPercentage(file)"
                                ></v-progress-circular>
                            </div>
                        </template>
                    </v-tooltip>

                    <v-tooltip v-if="file.status === 'ready'">
                        <p>Download!</p>
                        <template v-slot:activator="{ props }">
                            <v-btn
                                v-bind="props"
                                density="default"
                                icon="mdi-download"
                                variant="text"
                                @click="downloadFile(file.id)"
                            ></v-btn>
                        </template>
                    </v-tooltip>
                </div>

                <v-progress-linear
                    v-if="file.status === 'processing'"
                    bottom
                    indeterminate
                ></v-progress-linear>
            </v-sheet>
        </v-sheet>
    </v-container>
</template>
