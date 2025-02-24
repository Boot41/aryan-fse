# import logging
# import os
# from dotenv import load_dotenv
# from external_functions.AgentActions import AgentActions
# from external_functions.utility_functions import create_assessment_after_conversation
# from livekit.agents import (
#     AutoSubscribe,
#     JobContext,
#     JobProcess,
#     WorkerOptions,
#     cli,
#     metrics,
#     llm
# )
# from livekit.agents.pipeline import VoicePipelineAgent
# from livekit.plugins import deepgram, silero, turn_detector,openai
# from livekit.agents.llm import ChatContext 
# import json


# load_dotenv(dotenv_path=".env")


# def prewarm(proc: JobProcess):
#     proc.userdata["vad"] = silero.VAD.load()


# async def entrypoint(ctx: JobContext):
#     metadata = json.loads(participant.metadata)
#     logger.info(f"metadata : {metadata}")
#     logger = logging.getLogger("voice-agent")
#     fnc_ctx = AgentActions()
#     # get the user's info such as current subject and topic selected and store it in the context
#     user_email = ctx.room.name
#     print(user_email)
#     subject  = "maths"
#     topic = "addition"
#     initial_ctx = ChatContext().append(
#         role="system",
#         text=(
#             f"""You are a voice assistant created for helping students with topics they are struggling with. Your interface with users will be voice. 
#             You should use short and concise responses, and avoiding usage of unpronouncable punctuation. 
#             The current subject is maths and the current topic is addition.
#             Strictly provide answers to the question regarding this context only if user asks anything else just say "I can't provide you any information on that".
#             """
            
#         ),
#     )

#     logger.info(f"connecting to room {ctx.room.name}")
#     await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

#     # Wait for the first participant to connect
#     participant = await ctx.wait_for_participant()
#     logger.info(f"starting voice assistant for participant {participant.identity}")

#     print("----------------------------------------------metadataaaaaaa----------------------------------")
#     print(participant)
#     print("----------------------------------------------metadataaaaaaa----------------------------------")

#     agent = VoicePipelineAgent(
#         fnc_ctx=fnc_ctx,
#         vad=ctx.proc.userdata["vad"],
#         stt=deepgram.STT(),
#         llm = openai.LLM.with_groq(
#             model="llama3-8b-8192"
#         ),
#         tts=deepgram.TTS(
#             model= "aura-asteria-en"
#         ),
#         turn_detector=turn_detector.EOUModel(),
#         # minimum delay for endpointing, used when turn detector believes the user is done with their turn
#         min_endpointing_delay=0.5,
#         # maximum delay for endpointing, used when turn detector does not believe the user is done with their turn
#         max_endpointing_delay=5.0,
#         chat_ctx=initial_ctx,
#     )
   

#     usage_collector = metrics.UsageCollector()

#     @agent.on("metrics_collected")
#     def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
#         metrics.log_metrics(agent_metrics)
#         usage_collector.collect(agent_metrics)

#     agent.start(ctx.room, participant)

#     # The agent should be polite and greet the user when it joins :)
#     await agent.say("Hey, how can I help you today?", allow_interruptions=True)

#     ctx.add_shutdown_callback(create_assessment_after_conversation)
#     # there will be a cleanup funciton that will generate the assignment based on the user's doubts


# if __name__ == "__main__":
#     cli.run_app(
#         WorkerOptions(
#             entrypoint_fnc=entrypoint,
#             prewarm_fnc=prewarm,
#         ),
#     )







import asyncio
import logging
import os
import json
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import deepgram, openai, silero

load_dotenv()
logger = logging.getLogger("voice-assistant")
load_dotenv(dotenv_path=".env")

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    metadata = participant.metadata
    logger.info(f"metadata : {metadata}")
    logger.info(f"starting voice assistant for participant {participant.identity}")

    dg_model = "nova-3-general"
    if participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP:
        # use a model optimized for telephony
        dg_model = "nova-2-phonecall"

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(model=dg_model),
        llm = openai.LLM.with_groq(
            model="llama3-8b-8192"
        ),
        tts=deepgram.TTS(
            model= "aura-asteria-en"
        ),
        chat_ctx=initial_ctx,
    )

    agent.start(ctx.room, participant)

    usage_collector = metrics.UsageCollector()

    @agent.on("metrics_collected")
    def _on_metrics_collected(mtrcs: metrics.AgentMetrics):
        metrics.log_metrics(mtrcs)
        usage_collector.collect(mtrcs)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: ${summary}")

    ctx.add_shutdown_callback(log_usage)

    # listen to incoming chat messages, only required if you'd like the agent to
    # answer incoming messages from Chat
    chat = rtc.ChatManager(ctx.room)

    async def answer_from_text(txt: str):
        chat_ctx = agent.chat_ctx.copy()
        chat_ctx.append(role="user", text=txt)
        stream = agent.llm.chat(chat_ctx=chat_ctx)
        await agent.say(stream)

    @chat.on("message_received")
    def on_chat_received(msg: rtc.ChatMessage):
        if msg.message:
            asyncio.create_task(answer_from_text(msg.message))

    await agent.say("Hey, how can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )