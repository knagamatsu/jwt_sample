import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// Axiosインスタンスを作成
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプタ - 認証トークンを追加
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ユーザー登録
export const registerUser = async (userData) => {
  const response = await api.post('/register', userData);
  return response.data;
};

// ユーザーログイン
export const loginUser = async (credentials) => {
  const response = await api.post('/login', credentials);
  return response.data;
};

// ユーザープロフィール取得
export const getUserProfile = async () => {
  const response = await api.get('/users/me');
  return response.data;
};

export default api;
