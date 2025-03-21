import { useState, useEffect } from 'react';
import { getUserProfile } from '../services/api';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await getUserProfile();
        console.log('APIから返されたユーザーデータ:', userData);
        setUser(userData);
      } catch (err) {
        setError('ユーザー情報の取得に失敗しました。');
        console.error('Error fetching user data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return <div className="loading">読み込み中...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="dashboard">
      <h2>ダッシュボード</h2>
      {user && (
        <div className="user-profile">
          <h3>ユーザープロフィール</h3>
          <p><strong>メールアドレス:</strong> {user.email}</p>
          {user.username && <p><strong>ユーザー名:</strong> {user.username}</p>}
          
          <div className="debug-info">
            <h4>デバッグ情報:</h4>
            <pre>{JSON.stringify(user, null, 2)}</pre>
          </div>
        </div>
      )}
      <div className="dashboard-content">
        <h3>保護されたコンテンツ</h3>
        <p>このページはJWT認証が成功している場合のみ表示されます。</p>
      </div>
    </div>
  );
}

export default Dashboard;
