import {
  LiveKitRoom,
  RoomAudioRenderer,
  VoiceAssistantControlBar,
} from "@livekit/components-react";
import "@livekit/components-styles";
import { NoAgentNotification } from "./NoAgentNotification";
import SimpleVoiceAssistant from "./SimpleVoiceAssistant";
import { useEffect, useState } from "react";

const API_BASE_URL = 'http://localhost:8000/api';

function check_confirm_assignment(){
    const transcripts = JSON.parse(localStorage.getItem('recived_transcriptions'));
    if(transcripts){
      for (var j=0; j<transcripts.length; j++) {
          if(transcripts[j].match("noidontwanttocreateanassignment"))return false;
          else if (transcripts[j].match("yescreateanassignment")) return true;
      }
      return false;
    }
}

async function generateAssignment(user_email, subject, topic) {
  try {
    const response = await fetch(`${API_BASE_URL}/generate-custom-assignment/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({
        student_email:user_email,
        subject,
        topic
      })
    });

    if (!response.ok) {
      throw new Error('Failed to generate assignment');
    }

    const data = await response.json();
    console.log('Assignment generated:', data);
    return data;
  } catch (error) {
    console.error('Error generating assignment:', error);
    return null;
  }
}

export default function LiveKitElement({connectionDetails,updateConnectionDetails,conversationParams}) {
  const [agentState, setAgentState] = useState("disconnected");
  
  const disconnectHandler = async () => {
    updateConnectionDetails(undefined);
    const user_confirmed_assignment = check_confirm_assignment();
    
    if(user_confirmed_assignment){
      const user_email = localStorage.getItem('userEmail');
      await generateAssignment(user_email, conversationParams.subject, conversationParams.topic);
    }
    // here we will call a backed function that will create an assignment for the logged in user 
  };
  return (
    <div
      data-lk-theme="default"
      className="h-full grid content-center bg-[var(--lk-bg)]"
    >
      <LiveKitRoom
        token={connectionDetails?.participantToken}
        serverUrl={connectionDetails?.serverUrl}
        connect={connectionDetails !== undefined}
        audio={true}
        video={false}
        onMediaDeviceFailure={onDeviceFailure}
        onDisconnected={disconnectHandler}
        className="grid grid-rows-[2fr_1fr] items-center"
      >
        <SimpleVoiceAssistant onStateChange={setAgentState} />
        <VoiceAssistantControlBar  agentState={agentState} />
        <RoomAudioRenderer/>
        <NoAgentNotification state={agentState} />
      </LiveKitRoom>
    </div>
  );
}



function onDeviceFailure(error) {
  console.error(error);
  alert(
    "Error acquiring camera or microphone permissions. Please make sure you grant the necessary permissions in your browser and reload the tab"
  );
}