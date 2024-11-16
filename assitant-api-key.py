import os
from openai import AzureOpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("C:/Dev/ai-assistant/env.env"))

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

# Create an assistant
assistant = client.beta.assistants.create(
    name="Math Assist",
    instructions="You are an AI assistant that can write code to help answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model=os.getenv("DEPLOYMENT_NAME")
)

# Create a thread
thread = client.beta.threads.create()

# Add a user question to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

# Run the thread and poll for the result
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
)

print("Run completed with status: " + run.status)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.to_json(indent=2))