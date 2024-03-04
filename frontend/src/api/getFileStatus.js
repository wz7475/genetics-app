export const getFileStatus = async (taskId) => {
    return await fetch('api/getDetailedStatus', {
        method: 'POST',
        body: JSON.stringify({ task_id: taskId }),
        headers: { 'Content-Type': 'application/json' },
    }).then((res) => res.json())
}
