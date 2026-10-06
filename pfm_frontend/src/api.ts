import axios from 'axios';

// Per Expo SDK 49+ le variabili EXPO_PUBLIC_* sono inlineate a build time.
// Su dispositivo fisico va impostato l'IP della macchina sviluppatore, es.
// EXPO_PUBLIC_API_URL=http://192.168.1.10:8000
const env = (process.env ?? {}) as Record<string, string | undefined>;
export const BASE_URL = env.EXPO_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

export function setAuthHeader(token: string): void {
  api.defaults.headers.common.Authorization = `Bearer ${token}`;
}

export function clearAuthHeader(): void {
  delete api.defaults.headers.common.Authorization;
}

export function loginBody(username: string, password: string): string {
  return `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
}
