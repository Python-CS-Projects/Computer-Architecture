import sys

PRINT_TIM = 1

HALT = 2

memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    HALT
]

running = True
pc = 0

while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print("Tim!")
        pc += 1

    if command == HALT:
        running = False
