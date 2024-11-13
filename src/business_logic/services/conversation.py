from __future__ import annotations

from typing import TYPE_CHECKING

from typing import Union, Optional
from logging import getLogger
import asyncio

from src.business_logic.services.transcribtion_getting import get_transcript
from src.presentation.models import StartData, ProcessingData
from src.business_logic.services.ai_services import (
    add_message,
    create_thread,
    create_run_and_get_result,
    make_summary_and_questions,
    save_bytes_as_mp3,
    text_to_audio,
    audio_to_text
)
from src.data_access.orm import (
    get_or_create_child
)
from src.utils.file_system_operations import (
    create_or_clean_directory_in_media,
    delete_files_in_directory
)
from src.config import settings

logger = getLogger(__name__)


async def start_conversation(data: StartData):
    # получаем транскрипцию
    transcription = get_transcript(data.video_url)

    # получаем саммари и вопросы
    summary_and_questions = await make_summary_and_questions(transcription)

    # создаём тред
    thread_id = await create_thread()

    # получаем объект ребёнка (новый полностью или обновлённый старый)
    child = await get_or_create_child(
        child_id=data.child_id,
        thread=thread_id,
        additional_instructions=summary_and_questions
    )

    # генерируем стартовое сообщение ассистента
    first_message = await create_run_and_get_result(
        assistant_id=settings.child_assistant_id,
        thread_id=thread_id,
        additional_instruction=summary_and_questions,
    )

    # создаём папку для данного child_id в media, если её нет, либо очищаем её, если есть
    create_or_clean_directory_in_media(directory_name=child.child_id)

    # преобразуем текст в аудио
    path_to_voice = await text_to_audio(
        text=first_message,
        child_id=child.child_id
    )

    return path_to_voice


async def process_conversation(data: ProcessingData):

    child = await get_or_create_child(
        child_id=data.child_id,
    )

    # сохраняем голос ребенка в mp3
    path_to_voice = await save_bytes_as_mp3(
        byte_data=data.child_voice,
        child_id=child.child_id
    )

    # преобразуем аудио в текст
    text = await audio_to_text(
        file_path=path_to_voice
    )

    # получаем ответ ассистента
    assistant_answer = await create_run_and_get_result(
        assistant_id=settings.child_assistant_id,
        thread_id=child.thread,
        message=text,
        additional_instruction=child.additional_instructions,
    )

    # текст в голос
    final_audio_path = await text_to_audio(
        text=assistant_answer,
        child_id=child.child_id
    )

    return final_audio_path




