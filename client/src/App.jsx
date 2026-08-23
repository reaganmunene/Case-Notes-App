import { useState, useEffect } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    fetch(`${API_URL}/notes`)
      .then(res => res.json())
      .then(data => setNotes(data));
  }, []);

  function handleSubmit(e) {
    e.preventDefault();

    fetch(`${API_URL}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    })
      .then(res => res.json())
      .then(newNote => {
        setNotes([...notes, newNote]);
        setTitle('');
        setContent('');
      });
  }

  return (
    <div>
      <h1>Case Notes</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="text"
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <button type="submit">Add Note</button>
      </form>

      <ul>
        {notes.map(note => (
          <li key={note.id}>
            <strong>{note.title}</strong>: {note.content}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;