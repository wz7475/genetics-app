<script setup>
import { sendFile } from '@/api/sendFile'
import { useRouter } from 'vue-router'

const router = useRouter()

const submit = async (event) => {
    await sendFile(event)

    router.push('/history')
}
</script>

<template>
    <v-container class="fill-height justify-center text-center d-flex">
        <v-sheet
            class="pa-8"
            elevation="8"
            rounded
        >
            <v-img
                height="300"
                src="@/assets/logo.svg"
            />
            <h1 class="text-h2 font-weight-bold">Gene annotation</h1>
            <div class="text-body-2 font-weight-light mb-n1">
                by Studenckie Geny
            </div>

            <div class="py-10" />

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
            <br />
            <v-btn
                min-width="164"
                variant="text"
                to="/history"
            >
                <v-icon
                    icon="mdi-history"
                    size="large"
                    start
                />

                Previous annotations
            </v-btn>
        </v-sheet>
    </v-container>
</template>
