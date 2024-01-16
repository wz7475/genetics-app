export const sendFile = async (event) => {
    if (event.target?.files?.[0]) {
        const file = event.target?.files?.[0]

        const formData = new FormData()
        formData.append('file', file, file.name)
        const result = await fetch('/api/uploadfile', {
            method: 'POST',
            body: formData,
        }).then((res) => res.json())

        return result
    }
}
