// /home/aryan/Documents/project/client/src/routes/TalkWithChatbot.jsx

import React, { useState } from 'react';
import StartConversation from '../components/chatbot/StartConversation';
import CallPage from '../components/chatbot/CallPage';

const TalkWithChatbot = () => {
  const [isCallStarted, setIsCallStarted] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  const handleStartCall = () => {
    // TODO: Initiate WebRTC connection
    setIsCallStarted(true);
  };

  const handleEndCall = () => {
    // TODO: End WebRTC connection
    setIsCallStarted(false);
  };

  const handleToggleMute = () => {
    // TODO: Mute/unmute audio
    setIsMuted((prev) => !prev);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-8">
      <h2 className="text-4xl font-bold text-center text-white mb-8">Talk with Chatbot</h2>
      <div className="max-w-4xl mx-auto">
        {!isCallStarted ? (
          <StartConversation onStartCall={handleStartCall} />
        ) : (
          <CallPage onEndCall={handleEndCall} onToggleMute={handleToggleMute} isMuted={isMuted} />
        )}
      </div>
    </div>
  );
};

export default TalkWithChatbot;