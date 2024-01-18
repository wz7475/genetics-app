import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getFileStatus } from '@/api/getFileStatus'

export const useFileStore = defineStore('files', () => {
    const files = ref([])
    const ready = ref(false)

    const reloadFiles = async () => {
        const fileStorage = JSON.parse(localStorage.getItem('files') || '[]')
        ready.value = false

        files.value = await Promise.all(
            fileStorage.map((file) =>
                (async () => {
                    const status = (await getFileStatus(file.id)).status
                    return {
                        status,
                        time: new Date(file.date),
                        name: file.name,
                        id: file.id,
                    }
                })()
            )
        )

        ready.value = true
    }

    const removeFile = (index) => {
        files.value.splice(index, 1)

        const fileStorage = JSON.parse(localStorage.getItem('files') || '[]')
        fileStorage.splice(index, 1)
        localStorage.setItem('files', JSON.stringify(fileStorage))
    }

    const addFile = async (name, id) => {
        const files = JSON.parse(localStorage.getItem('files') || '[]')
        files.unshift({ name, id, date: new Date() })
        localStorage.setItem('files', JSON.stringify(files))

        await reloadFiles()
    }

    return {
        files,
        ready,
        reloadFiles,
        removeFile,
        addFile,
    }
})
