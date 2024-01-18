<script setup>
import { sendFile } from '@/api/sendFile'
import { getAlgorithms } from '@/api/getAlgorithms'
import { ref, computed, onMounted } from 'vue'

const props = defineProps(['submitCallback'])

const fileInput = ref(null)
const fileSelected = ref(false)

const algorithms = ref([])
const selectedAlgs = ref([])

const canSubmit = computed(
    () => fileSelected.value && selectedAlgs.value.length > 0
)

const onChange = async () => {
    fileSelected.value = true
}

const submit = async () => {
    if (fileInput.value.files?.[0]) {
        const file = fileInput.value.files[0]

        await sendFile(file, selectedAlgs.value)

        if (fileInput.value) fileInput.value.value = null

        fileSelected.value = false

        if (props.submitCallback) props.submitCallback()
    }
}

onMounted(async () => {
    algorithms.value = await getAlgorithms()
})
</script>

<template>
    <v-dialog
        width="500"
        scrollable
    >
        <template v-slot:activator="{ props }">
            <v-btn
                v-bind="props"
                color="primary"
                size="x-large"
                variant="flat"
            >
                <v-icon
                    icon="mdi-dna"
                    size="large"
                    start
                />

                Annotate file
            </v-btn>
        </template>

        <template v-slot:default="{ isActive }">
            <v-card title="Annotate file">
                <v-card-text>
                    Algorithms:
                    <v-checkbox
                        v-for="algorithm in algorithms"
                        :key="algorithm"
                        hide-details
                        color="primary"
                        v-model="selectedAlgs"
                        :label="algorithm"
                        :value="algorithm"
                    ></v-checkbox>
                </v-card-text>

                <v-divider />

                <v-btn
                    v-bind="props"
                    :color="!fileSelected ? 'secondary' : 'success'"
                    size="x-large"
                    variant="flat"
                    tag="label"
                    class="mx-6"
                >
                    <v-icon
                        :icon="!fileSelected ? 'mdi-file' : 'mdi-check'"
                        size="large"
                        start
                    />

                    Select file
                    <input
                        ref="fileInput"
                        type="file"
                        hidden
                        accept=".tsv"
                        @change="onChange"
                    />
                </v-btn>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        text="Cancel"
                        @click="isActive.value = false"
                    ></v-btn>
                    <v-btn
                        class="px-4"
                        variant="flat"
                        :color="canSubmit ? 'primary' : 'grey'"
                        size="x-large"
                        @click="
                            () => {
                                isActive.value = false
                                submit()
                            }
                        "
                        :disabled="!canSubmit"
                    >
                        Submit
                        <v-icon
                            icon="mdi-send"
                            size="large"
                            end
                        />
                    </v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>
