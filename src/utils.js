export function findDeepestData(object) {
    if (object.data && typeof object.data === 'object') {
        return findDeepestData(object.data);
    }
    return object;
}