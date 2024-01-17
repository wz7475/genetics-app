<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { sendFile } from '@/api/sendFile'
import { getFileStatus } from '@/api/getFileStatus'
import { downloadFile } from '@/api/downloadFile'

const filesReady = ref(false)
const files = ref([])

const colorMap = {
    ready: 'success',
    pending: 'info',
    expired: 'grey',
}

const removeFile = (index) => {
    files.value.splice(index, 1)

    const fileStorage = JSON.parse(localStorage.getItem('files') || '[]')
    fileStorage.splice(index, 1)
    localStorage.setItem('files', JSON.stringify(fileStorage))
}

const reloadFiles = async () => {
    const fileStorage = JSON.parse(localStorage.getItem('files') || '[]')
    files.value = []
    filesReady.value = false

    for (const file of fileStorage) {
        const status = (await getFileStatus(file.id)).status
        files.value.push({
            status,
            time: new Date(file.date),
            name: file.name,
            id: file.id,
        })
    }

    filesReady.value = true
}

const polling = ref(null)

onMounted(async () => {
    await reloadFiles()
    polling.value = setInterval(reloadFiles, 5000)
})

onUnmounted(() => {
    clearInterval(polling.value)
})

const submit = async (event) => {
    await sendFile(event)
    await reloadFiles()
}
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

                <v-spacer />

                <v-btn
                    color="primary"
                    size="x-large"
                    variant="flat"
                    tag="label"
                >
                    <v-icon
                        icon="mdi-dna"
                        size="large"
                        start
                    />

                    Annotate file
                    <input
                        type="file"
                        hidden
                        accept=".tsv"
                        @change="submit"
                    />
                </v-btn>
            </div>
            <v-progress-circular
                v-if="!filesReady"
                indeterminate
                class="ma-auto"
            ></v-progress-circular>
            <v-sheet
                v-for="(file, index) in files"
                :key="file.name"
                elevation="8"
                class="d-flex pa-1 px-4 align-center"
                style="min-height: 56px"
                rounded
                :color="colorMap[file.status]"
            >
                <span class="text-h6">{{ file.name }}</span>
                <span class="pl-2 text-subtitle-1">
                    {{ file.time.toISOString() }}
                </span>
                <v-spacer />

                <v-hover
                    v-if="file.status === 'expired'"
                    v-slot="{ isHovering, props }"
                >
                    <v-btn
                        v-bind="props"
                        density="compact"
                        size="x-large"
                        variant="text"
                        class="pr-1"
                        :icon="isHovering ? 'mdi-close' : 'mdi-emoticon-sad'"
                        @click="removeFile(index)"
                    ></v-btn>
                </v-hover>

                <v-progress-circular
                    v-if="file.status === 'pending'"
                    class="mr-2"
                    indeterminate
                ></v-progress-circular>
                <v-btn
                    v-if="file.status === 'ready'"
                    density="default"
                    icon="mdi-download"
                    variant="text"
                    @click="downloadFile(file.id)"
                ></v-btn>
            </v-sheet>
        </v-sheet>
    </v-container>
</template>
