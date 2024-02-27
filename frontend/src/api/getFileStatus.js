export const getFileStatus = async (taskId) => {
    return await fetch('api/getDetailedStatus', {
        method: 'POST',
        body: JSON.stringify({ task_id: taskId }),
    }).then((res) => res.json())
}
