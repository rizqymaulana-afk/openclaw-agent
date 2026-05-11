# run_autonomous.py

from autonomous_agent import (
    AutonomousAgent
)


agent = AutonomousAgent()

goal = input(
    "Masukkan goal: "
)

result = agent.run(goal)

print("\nFINAL RESULT:\n")

print(result)