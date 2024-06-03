import telebot

# Define bot commands
def register_commands(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.reply_to(message, "Welcome to the Job Scraping Bot! Use /help to see available commands.")

    @bot.message_handler(commands=['help'])
    def handle_help(message):
        help_text = """
        Available commands:
        /start - Start the bot
        /help - Show available commands
        /setkeywords - Set or update keywords for job filtering
        /searchjobs - Manually search for jobs using the set keywords
        /applyall - Automatically apply to all jobs that match the set keywords
        /savedjobs - View the list of saved jobs for later review or application
        /appliedjobs - View the list of jobs the user has applied to
        /listsources - View the current list of job sources (websites, Telegram channels, groups)
        /addsource - Add a new job source (website, Telegram channel, group)
        /removesource - Remove an existing job source from the list
        /setnotifications - Set preferences for job notifications (e.g., frequency, types of jobs)
        /analyzemyresume - Submit a resume for AI analysis and keyword suggestions
        /subscribe - Subscribe to the bot’s services after the free trial
        /status - Check the current subscription status
        /cancel - Cancel the current subscription
        """
        bot.reply_to(message, help_text)

    # Add more command handlers here...
