const cutoffs = [60, 3600, 86400, 86400 * 7, 86400 * 30, 86400 * 365, Infinity]
const units = ['second', 'minute', 'hour', 'day', 'week', 'month', 'year']

export const getRelativeTime = (date) => {
    const timeMs = date
    const deltaSeconds = Math.round((timeMs - Date.now()) / 1000)

    const unitIndex = cutoffs.findIndex(
        (cutoff) => cutoff > Math.abs(deltaSeconds)
    )

    const divisor = unitIndex ? cutoffs[unitIndex - 1] : 1

    const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })
    return rtf.format(Math.floor(deltaSeconds / divisor), units[unitIndex])
}
