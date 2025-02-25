// /home/aryan/Documents/project/client/src/components/StartConversation.jsx

import React, { useState, useCallback, useRef, useEffect } from 'react';
import axios from 'axios';
import LiveKitElement from './livekit/LiveKitElement';
import { useUser } from '../../context/UserContext';
import { getSubjectsAndTopics } from '../../api';

const StartConversation = () => {
  const [connectionDetails, updateConnectionDetails] = useState(undefined);
  const [subjects, setSubjects] = useState({});
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useUser();
  const [userData, setUserData] = useState(null);

  // Fetch subjects and topics on component mount
  useEffect(() => {
    const fetchSubjectsAndTopics = async () => {
      try {
        const response = await getSubjectsAndTopics();
        setSubjects(response.data);
        setLoading(false);
      } catch (error) {
        setError('Failed to load subjects and topics');
        setLoading(false);
      }
    };

    fetchSubjectsAndTopics();
  }, []);

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    setUserData(storedUser);
  }, []);

  const onConnectButtonClicked = useCallback(async () => {
    const response = await axios.post(import.meta.env.VITE_PUBLIC_CONN_DETAILS_ENDPOINT,
      {
        room: userData?.email || "testuser@gmail.com",
        name: userData?.name || "test_user_name",
        topic: selectedTopic,
        subject: selectedSubject
      });
    console.log(response.data)
    const connectionDetailsData = response.data;
    updateConnectionDetails(connectionDetailsData);
  }, [selectedTopic, selectedSubject, userData]);

  if (connectionDetails) {
    return (<LiveKitElement updateConnectionDetails={updateConnectionDetails} conversationParams={{subject: selectedSubject, topic: selectedTopic}} connectionDetails={connectionDetails} />)
  } else {
    return (
      <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30 flex flex-col items-center">
        <p className="text-gray-300 mb-6">Select a subject and topic to start a conversation with the chatbot.</p>
       
        {loading ? (
          <p className="text-gray-400">Loading subjects and topics...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <div className="w-full max-w-md space-y-4 mb-6">
            {/* Subject Dropdown */}
            <div>
              <label htmlFor="subject" className="block text-sm font-medium text-gray-300 mb-2">
                Select Subject
              </label>
              <select
                id="subject"
                value={selectedSubject}
                onChange={(e) => {
                  setSelectedSubject(e.target.value);
                  setSelectedTopic(''); // Reset topic when subject changes
                }}
                className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
              >
                <option value="">Choose a subject</option>
                {Object.keys(subjects).map((subject) => (
                  <option key={subject} value={subject}>
                    {subject}
                  </option>
                ))}
              </select>
            </div>

            {/* Topic Dropdown - Only show if subject is selected */}
            {selectedSubject && (
              <div>
                <label htmlFor="topic" className="block text-sm font-medium text-gray-300 mb-2">
                  Select Topic
                </label>
                <select
                  id="topic"
                  value={selectedTopic}
                  onChange={(e) => setSelectedTopic(e.target.value)}
                  className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
                >
                  <option value="">Choose a topic</option>
                  {subjects[selectedSubject]?.topics.map((topic) => (
                    <option key={topic} value={topic}>
                      {topic}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>
        )}

        <button
          onClick={onConnectButtonClicked}
          disabled={!selectedSubject || !selectedTopic}
          className={`bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-3 px-6 rounded-lg shadow-md transition-all duration-200 w-full max-w-md
            ${(!selectedSubject || !selectedTopic)
              ? 'opacity-50 cursor-not-allowed'
              : 'hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2'
            }`}
        >
          Start a Conversation
        </button>
      </div>
    )
  }
}

export default StartConversation;