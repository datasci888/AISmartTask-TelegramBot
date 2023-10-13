# openinterpreter
Openinterpreter hackathon

<img width="1087" alt="Screen Shot 2023-10-13 at 11 13 36 AM" src="https://github.com/datasci888/openinterpreter/assets/119770980/9742e0fd-db80-4c27-8270-c65c45b7e74e">

# AISmartTaskTask
# AI-powered task manager with notifications, document analysis, and task visualization.

# Features:
* 		Task prioritization
* 		Automated notifications for upcoming tasks on Telegram
* 		Document analysis with keyword highlighting
* 		Visual representation of task priorities

# Dependencies:
* datetime
* time
* requests
* telegram
* openai
* matplotlib
* BeautifulSoup4
* re

# Configuration:
Before running the application:
* 		Replace Your OpenAI API Key with your OpenAI API key.
* 		Replace Your Telegram Bot Token with your Telegram bot token.
Class Structure:
* 		TaskManager: Handles adding, prioritizing, organizing, and retrieving tasks.
* 		Task: Represents a single task with name, deadline, and priority.
Telegram Bot Commands:
* /start: Start the AI Task Manager.
* /help: Show available commands.
* /add_task: Add a new task (Format: /add_task Buy groceries, 2023-12-31, 2)
* /list_tasks: List all tasks.
* /delete_task: Delete a task by ID (Format: /delete_task 1)
* /update_task: Update a task by ID (Format: /update_task 1, New Task, 2023-12-31, 2)
* /document: Analyze a document with keywords (Format: /document Sample document text. Keyword1; Keyword2; Keyword3)
* /feedback: Provide feedback on AI decisions.
* /upcoming_tasks: List upcoming tasks.

To Run:
'''
if __name__ == "__main__":
    main()
'''
