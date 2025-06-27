from datetime import datetime

def log_token_usage(prompt, response):
    try:
        usage = response.usage
        with open("token_log.txt", "a") as f:
            f.write(f"{datetime.now()} | Prompt Tokens: {usage.prompt_tokens}, "
                    f"Completion Tokens: {usage.completion_tokens}, "
                    f"Total: {usage.total_tokens}\nPrompt: {prompt}\n\n")
    except Exception as e:
        print(f"Logging error: {e}")

