from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
import openai
from moviepy.editor import AudioFileClip
import concurrent.futures

# Initialize OpenAI and Telegram API tokens
openai.api_key = "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"
TELEGRAM_API_TOKEN = "6432141709:AAEnyt3zns3yL8F2fsnKh85C4RZmoOiqKV4"

# Create a list to store the conversation history
conversation = []

# Define the system message
system_message = {
    "role": "system",
    "content": "You are AISmartTask: An innovative AI-driven task management solution tailored for coders or anyone who likes to manage daily routines. You offer an intuitive user experience. Key features include dynamic task management that allows for task addition, prioritization, and AI-powered task suggestions. You can accept documents in the form of text, and your document parser extracts essential summaries and highlights critical keywords from that document. Additionally, AISmartTask visualizes task priorities, enabling users to get a clearer view of their tasks at hand. Your one standout quality is your learning modules, which web scrape for knowledge, encouraging continuous learning. Users can interact with you and provide feedback for continuous system improvement. AISmartTask is not just a task manager; it's a revolutionary tool aiming to optimize and enhance the daily routines of coders. It is scalable to any user and other applications such as enterprise project management, academic tasks management (students and educators), task management in healthcare, and in the freelance and gig economy."
}

# Initialize the conversation with the system message
conversation.append(system_message)

def text_message(update, context):
    user_message = update.message.text
    # Append user message to the conversation
    conversation.append({"role": "user", "content": user_message})

    # Use a maximum of the last 10 messages for context
    context_messages = conversation[-20:]
    
    # Send user message to OpenAI for a response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=context_messages
    )
    assistant_reply = response["choices"][0]["message"]["content"]
    
    # Send the assistant's reply back to the user
    update.message.reply_text(text=f"**{assistant_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    
    # Append assistant's reply to the conversation
    conversation.append({"role": "assistant", "content": assistant_reply})

def voice_message(update, context):
    update.message.reply_text("I've received your voice message! Please give me a second to respond :)")
    
    # Download the voice message and transcribe it
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    
    # Append the transcribed message to the conversation
    conversation.append({"role": "user", "content": transcript})
    
    # Use a maximum of the last 10 messages for context
    context_messages = conversation[-10:]
    
    # Send the transcribed message to OpenAI for a response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=context_messages
    )
    assistant_reply = response["choices"][0]["message"]["content"]
    
    # Send the assistant's reply back to the user
    update.message.reply_text(text=f"**{assistant_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    
    # Append assistant's reply to the conversation
    conversation.append({"role": "assistant", "content": assistant_reply})

def show_task_list(update, context):
    # Extract and show the tasks from the conversation history
    tasks = extract_tasks(conversation)
    if tasks:
        task_list = "\n".join(tasks)
        update.message.reply_text(f"Your task list:\n{task_list}")
    else:
        update.message.reply_text("You don't have any tasks in your list yet.")

def extract_tasks(conversation):
    # Extract tasks from the conversation history
    tasks = []
    for message in conversation:
        if message['role'] == 'user' and "add task" in message['content'].lower():
            task = message['content'].replace("add task", "").strip()
            tasks.append(task)
    return tasks

def start(update, context):
    user_message = update.message.text
    conversation.append({"role": "user", "content": user_message})
    context_messages = conversation[-10:]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=context_messages
    )
    assistant_reply = response["choices"][0]["message"]["content"]

    update.message.reply_text(text=f"**{assistant_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    conversation.append({"role": "assistant", "content": assistant_reply})

def prioritize_tasks(tasks):
    # Placeholder function for task prioritization
    # You can implement your task prioritization logic here
    # For example, you can use NLP techniques to analyze tasks and prioritize based on deadlines, importance, etc.
    return tasks

def start_bot():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add message handlers for text, voice, and showing task list
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
    dispatcher.add_handler(CommandHandler("show_tasks", show_task_list))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    start_bot()
