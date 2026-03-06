class SessionMemory:
    """
    Short-Term Memory (Session Memory)

    Stores conversation history during runtime.
    Only the last N messages are kept.
    """

    def __init__(self, max_messages=10):
        self.messages = []
        self.max_messages = max_messages

    def add_message(self, role: str, content: str):
        self.messages.append((role, content))

        # keep only last N messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_history(self):
        return self.messages

    def get_context(self):
        context = ""
        for role, msg in self.messages:
            context += f"{role}: {msg}\n"
        return context.strip()

    def clear(self):
        self.messages = []


# Interactive Session Test
if __name__ == "__main__":

    memory = SessionMemory()

    print("Session Memory Interactive Test")
    print("Type 'exit' to stop\n")

    while True:

        user_query = input("User: ")

        if user_query.lower() == "exit":
            break

        # store user message
        memory.add_message("User", user_query)

        # simulate agent reply
        agent_reply = f"I received: {user_query}"
        memory.add_message("Agent", agent_reply)

        print("Agent:", agent_reply)

        print("\n--- Current Session Memory ---")
        for msg in memory.get_history():
            print(msg)

        print("\nTotal messages stored:", len(memory.get_history()))
        print("------------------------------\n")