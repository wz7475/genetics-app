import { useFileStore } from '@/store'

export const sendFile = async (file, selectedAlgorithms) => {
    const fileStore = useFileStore()

    const formData = new FormData()
    formData.append('file', file, file.name)
    formData.append('algorithms', selectedAlgorithms.join(','))
    const result = await fetch('/api/uploadFile', {
        method: 'POST',
        body: formData,
    }).then((res) => res.json())

    fileStore.addFile(file.name, result.id)

    return result
}
