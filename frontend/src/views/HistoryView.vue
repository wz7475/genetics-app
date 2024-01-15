<script setup>
import { ref } from 'vue'

const files = ref([
    { status: 'expired', time: new Date(), name: 'Mój pliczek 1' },
    { status: 'ready', time: new Date(), name: 'Mój pliczek 2' },
    { status: 'expired', time: new Date(), name: 'Mój pliczek 3' },
    { status: 'pending', time: new Date(), name: 'Mój pliczek 4' },
    { status: 'expired', time: new Date(), name: 'Mój pliczek 5' },
])

const colorMap = {
    ready: 'success',
    pending: 'info',
    expired: 'grey',
}

const submit = () => {}
</script>

<template>
    <v-container class="fill-height justify-center text-center d-flex">
        <v-sheet
            class="pa-6 flex-grow-1 ga-4 d-flex flex-column"
            style="max-width: 1000px"
            elevation="8"
            rounded
        >
            <div class="d-flex ga-8 align-center justify-space-between">
                <h4 class="text-h5 font-weight-bold">Previous annotations</h4>

                <v-btn
                    color="primary"
                    size="x-large"
                    variant="flat"
                    @click="submit"
                >
                    <v-icon
                        icon="mdi-dna"
                        size="large"
                        start
                    />

                    Annotate file
                </v-btn>
            </div>
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
                        @click="files.splice(index, 1)"
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
                ></v-btn>
            </v-sheet>
        </v-sheet>
    </v-container>
</template>
