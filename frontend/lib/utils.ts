export const formatTimestamp = (timestamp: string) => {
  try {
    return new Date(timestamp).toLocaleTimeString();
  } catch {
    return "";
  }
};

export const shortId = () =>
  Math.random().toString(36).substring(2, 8) + Date.now().toString(36);

