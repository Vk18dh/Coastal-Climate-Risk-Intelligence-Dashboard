import axios from 'axios';
import { config } from '../config/env';

export const apiClient = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data: T;
}

// Global response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Infrastructure Error:', error?.response?.data || error.message);
    return Promise.reject(error);
  }
);
