from agent import OpenClawAgent

agent = OpenClawAgent()

print("=== OPENCLAW AI AGENT ===")

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    response = agent.run(user_input)

    print(f"\nAgent: {response}")