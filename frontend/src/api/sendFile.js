export const sendFile = async (event) => {
    if (event.target?.files?.[0]) {
        const file = event.target?.files?.[0]

        const formData = new FormData()
        formData.append('file', file, file.name)
        const result = await fetch('/api/uploadfile', {
            method: 'POST',
            body: formData,
        }).then((res) => res.json())

        const files = JSON.parse(localStorage.getItem('files') || '[]')
        files.unshift({ name: file.name, id: result.id, date: new Date() })
        localStorage.setItem('files', JSON.stringify(files))

        return result
    }
}
