export function formatTimeUtc(isoString: string): string {
  if (!isoString) {
    return "--:--:--";
  }
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) {
    return "--:--:--";
  }
  return date.toISOString().slice(11, 19);
}
