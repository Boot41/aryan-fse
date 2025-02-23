import {
  LiveKitRoom,
  RoomAudioRenderer,
  VoiceAssistantControlBar,
} from "@livekit/components-react";
import "@livekit/components-styles";
import { useState } from "react";
import { NoAgentNotification } from "./NoAgentNotification";
import SimpleVoiceAssistant from "./SimpleVoiceAssistant";

export default function LiveKitElement({connectionDetails,updateConnectionDetails}) {
  const [agentState, setAgentState] = useState("disconnected");
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
        onDisconnected={() => {
          updateConnectionDetails(undefined);
        }}
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