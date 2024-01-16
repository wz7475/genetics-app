export const getFileStatus = async (taskId) => {
    return await fetch('api/getStatus', {
        method: 'POST',
        body: JSON.stringify({
            task_id: taskId,
        }),
    }).then((res) => res.json())
}
