// /home/aryan/Documents/project/client/src/components/StartConversation.jsx

import React,{useState, useCallback, useRef, useEffect} from 'react';
import axios from 'axios';
import LiveKitElement from './livekit/LiveKitElement';
import { useUser } from '../../context/UserContext';

const StartConversation = () => {
  
  const [connectionDetails, updateConnectionDetails] = useState(undefined);

  const onConnectButtonClicked = useCallback(async () => {
    const response = await axios.post(import.meta.env.VITE_PUBLIC_CONN_DETAILS_ENDPOINT,
      {
        room: "testuser@gmail.com",
        name: "test_user_name",
      });
    console.log(response.data)
    const connectionDetailsData = response.data;
    updateConnectionDetails(connectionDetailsData);
  }, []);

    if (connectionDetails) {
      return (<LiveKitElement updateConnectionDetails={updateConnectionDetails} connectionDetails={connectionDetails} />)
    }
    else{
      return (<div className="bg-gray-800/70 backdrop-blur-sm p-8 rounded-lg shadow-2xl border border-gray-700/30 flex flex-col items-center">
      <p className="text-gray-300 mb-6">Click below to start a conversation with the chatbot.</p>
      <button
        onClick={onConnectButtonClicked}
        className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-3 px-6 rounded-lg shadow-md hover:from-purple-800 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-offset-2 transition-all duration-200"
      >
        Start a Conversation
      </button>
      </div>)
    }
  }

export default StartConversation;