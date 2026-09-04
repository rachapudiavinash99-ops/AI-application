import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface Topic {
  id: number;
  name: string;
}

interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  result: string | null;
}

export default function Dashboard() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [topicId, setTopicId] = useState<number>(0);

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchTopics();
    fetchTasks();
  }, [token]);

  const fetchTopics = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/tasks/topics', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTopics(res.data);
      if (res.data.length > 0) setTopicId(res.data[0].id);
    } catch (e) { console.error(e); }
  };

  const fetchTasks = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/tasks/tasks', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTasks(res.data);
    } catch (e) { console.error(e); }
  };

  const submitTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/v1/tasks/tasks', {
        title, description, topic_id: topicId
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTitle('');
      setDescription('');
      fetchTasks();
    } catch (e) { console.error(e); }
  };

  return (
    <div style={{ padding: '20px' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #ccc', paddingBottom: '10px' }}>
        <h1>AI Workspace</h1>
        <button onClick={() => { logout(); navigate('/login'); }}>Logout</button>
      </header>
      
      <main style={{ display: 'flex', marginTop: '20px', gap: '20px' }}>
        <section style={{ flex: 1 }}>
          <h2>Create Task</h2>
          <form onSubmit={submitTask} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <select value={topicId} onChange={e => setTopicId(Number(e.target.value))}>
              {topics.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
            <input placeholder="Task Title" value={title} onChange={e => setTitle(e.target.value)} required />
            <textarea placeholder="Description / Prompt" rows={5} value={description} onChange={e => setDescription(e.target.value)} required />
            <button type="submit">Submit to AI</button>
          </form>
        </section>

        <section style={{ flex: 2 }}>
          <h2>Task History</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {tasks.map(task => (
              <div key={task.id} style={{ border: '1px solid #eee', padding: '10px', borderRadius: '4px' }}>
                <h3>{task.title} <small>({task.status})</small></h3>
                <p><strong>Prompt:</strong> {task.description}</p>
                {task.result && <p style={{ background: '#f9f9f9', padding: '10px' }}><strong>Result:</strong> {task.result}</p>}
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

// Layout fix applied
