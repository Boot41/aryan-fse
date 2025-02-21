// /home/aryan/Documents/project/client/src/components/chatbot/CallPage.jsx

import React, { useState, useEffect } from 'react';

const CallPage = ({ onEndCall, onToggleMute, isMuted }) => {
  const [isBotThinking, setIsBotThinking] = useState(false);
  const [isUserSpeaking, setIsUserSpeaking] = useState(false);

  const simulateBotResponse = () => {
    // Simulate bot "thinking" and responding
    setIsBotThinking(true);
    setTimeout(() => {
      setIsBotThinking(false);
      // TODO: Play bot's voice response
    }, 2000); // Simulate a 2-second delay
  };

  const handleUserSpeech = () => {
    // Simulate user speaking (this would be replaced with actual voice input logic)
    setIsUserSpeaking(true);
    setTimeout(() => {
      setIsUserSpeaking(false);
      simulateBotResponse();
    }, 3000); // Simulate a 3-second user speech
  };

  return (
    <div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30">
      {/* Voice Call Interface */}
      <div className="text-center mb-6">
        {isUserSpeaking ? (
          <div className="bg-purple-700 text-white p-3 rounded-lg inline-block">
            Speaking...
          </div>
        ) : isBotThinking ? (
          <div className="bg-gray-700 text-white p-3 rounded-lg inline-block">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-100"></div>
              <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-200"></div>
            </div>
          </div>
        ) : (
          <div className="bg-gray-700 text-white p-3 rounded-lg inline-block">
            Ready to speak
          </div>
        )}
      </div>

      {/* Call Controls */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={handleUserSpeech}
          className="bg-purple-700 text-white p-3 rounded-lg shadow-md hover:bg-purple-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200"
        >
          Speak
        </button>
        <button
          onClick={onToggleMute}
          className={`${
            isMuted ? 'bg-gray-800' : 'bg-gray-700'
          } text-white p-3 rounded-lg shadow-md hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-offset-2 transition-all duration-200`}
        >
          {isMuted ? 'Unmute' : 'Mute'}
        </button>
        <button
          onClick={onEndCall}
          className="bg-red-600 text-white p-3 rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2 transition-all duration-200"
        >
          End Call
        </button>
      </div>
    </div>
  );
};

export default CallPage;