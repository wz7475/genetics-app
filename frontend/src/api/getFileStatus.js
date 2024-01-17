export const getFileStatus = async (taskId) => {
    return await fetch('api/getStatus', {
        method: 'POST',
        body: taskId,
    }).then((res) => res.json())
}
