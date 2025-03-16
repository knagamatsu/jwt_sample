import axios from 'axios';

// ベースURLはViteのプロキシ経由で利用する（相対パス）
const API_URL = '/api'; 

// Axiosインスタンスを作成
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// リクエストインターセプタ - 認証トークンを追加
api.interceptors.request.use(
  (config) => {
    console.log('Sending request to:', config.url, 'with data:', config.data);
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// レスポンスインターセプタ - エラーハンドリング
api.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    console.error('Full error object:', error);
    return Promise.reject(error);
  }
);

// ユーザー登録
export const registerUser = async (userData) => {
  try {
    console.log('Registering user with data:', userData);
    const response = await api.post('/register', userData);
    console.log('Registration successful:', response.data);
    return response.data;
  } catch (error) {
    console.error('Registration failed:', error);
    throw error;
  }
};

// ユーザーログイン
export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/login', credentials);
    return response.data;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

// ユーザープロフィール取得
export const getUserProfile = async () => {
  try {
    const response = await api.get('/users/me');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
    throw error;
  }
};

export default api;
