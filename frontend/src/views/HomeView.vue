<script setup>
const uploadFile = () => {}
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
                min-width="228"
                size="x-large"
                variant="flat"
                class="mb-8"
                to="/history"
                @click="uploadFile"
            >
                <v-icon
                    icon="mdi-dna"
                    size="large"
                    start
                />

                Annotate file
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
