import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !question) {
      alert('Please select a file and enter a question.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('question', question);

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/ask_question', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Response from backend:', response.data); // Debug log

      // Check if the response contains the expected "answer" key
      if (response.data && response.data.answer) {
        setAnswer(response.data.answer);
      } else {
        alert('No answer returned from the backend.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error occurred while fetching the answer.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="info">
        <h4>Naina Chabra</h4>
      </div>

      <h1 className="title">DriveX Assignment</h1>
      <h2>You ask, We answer</h2>

      <div className="formbox">
        <form onSubmit={handleSubmit}>
          <input
            type="file"
            accept=".xlsx, .xls"
            onChange={handleFileChange}
          />
          <input
            type="text"
            placeholder="Enter your question"
            value={question}
            onChange={handleQuestionChange}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Submit'}
          </button>
        </form>
      </div>

      {answer && (
        <div>
          <strong>Answer:</strong>
          <p className="ans">{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;