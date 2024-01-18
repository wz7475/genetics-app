export const getAlgorithms = async () => {
    return (
        await fetch('api/availableAlgorithms', {
            method: 'GET',
        }).then((res) => res.json())
    ).algorithms
}
