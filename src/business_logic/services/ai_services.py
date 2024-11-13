from __future__ import annotations

import os
import json
import asyncio
from logging import getLogger
from typing import TYPE_CHECKING, Optional, Any
from openai import AsyncOpenAI
import uuid

from pydub import AudioSegment
import io

from src.config import settings
from src.business_logic.services.prompts import (
    make_prompt_for_summary_and_questions,
)
from src.schemas.response_format import SummaryAndQuestions


logger = getLogger(__name__)
client = AsyncOpenAI(api_key=settings.openai_api_key)


async def create_thread() -> str:
    thread = await client.beta.threads.create()
    logger.info(f'Thread {thread.id} created')
    return thread.id


async def delete_thread(thread_id: str) -> None:
    await client.beta.threads.delete(thread_id=thread_id)


async def add_message(
        text: str,
        role: str,
        thread_id: str
):
    message = await client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=text
    )
    return message


async def create_run_and_get_result(
        assistant_id: str,
        thread_id: str,
        role='user',
        message: str = None,
        additional_instruction: Optional[str] = None,
        conversation_id: Optional[str] = None,  # для обращения в redis
) -> str:

    if message:
        await add_message(
            thread_id=thread_id,
            role=role,
            text=message
        )

    await wait_for_active_runs_to_complete(thread_id)

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        additional_instructions=additional_instruction,
    )

    if run.status == 'completed':
        messages = await client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value

    elif run.status == "requires_action":
        pass

    else:
        logger.error(run.status)


async def wait_for_active_runs_to_complete(thread_id: str) -> None:
    while True:
        runs = await client.beta.threads.runs.list(thread_id=thread_id)
        active_runs = [
            run for run in runs.data if run.status in [
                'active', 'requires_action'
            ]
        ]
        if not active_runs:
            break

        for run in active_runs:
            if run.status == 'requires_action':
                tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
                await client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=run.thread_id,
                    run_id=run.id,
                    tool_outputs=[
                        {"tool_call_id": tool_call.id, "output": "success"}
                    ]
                )
        await asyncio.sleep(1)


async def make_summary_and_questions(
        transcribtion: str,
) -> str:

    completion = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[

            {"role": "user", "content": make_prompt_for_summary_and_questions(transcribtion)},
        ],
        response_format=SummaryAndQuestions,
    )
    return completion.choices[0].message.parsed.result


def save_bytes_as_mp3(byte_data, child_id: str) -> str:
    unique_filename_path = os.path.join(os.getcwd(), "media", child_id, f"{uuid.uuid4()}.mp3")

    audio = AudioSegment.from_file(io.BytesIO(byte_data), format="wav")
    audio.export(unique_filename_path, format="mp3")
    return unique_filename_path


async def audio_to_text(file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        transcript = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return str(transcript)


async def text_to_audio(text: str, child_id: str) -> str:
    speech_file_path = os.path.join(os.getcwd(), "media", child_id, f"{uuid.uuid4()}.mp3")
    response = await client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path





