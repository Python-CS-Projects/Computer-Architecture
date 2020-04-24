"""CPU functionality."""

import sys

# LDI: load "immediate", store a value in a register, or "set this register to this value".
LDI = 0b10000010
# PRN: a pseudo-instruction that prints the numeric value stored in a register.
PRN = 0b01000111
HLT = 0b00000001  # HLT: halt the CPU and exit the emulator.


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # Register R0-R7
        self.ram = [0] * 256
        self.pc = 0  # Program Counter, which is the address/index of the current instruction
        self.running = True

    # Accepts the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]

    # Accept a value to write, and the address to write it to.
    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            # It needs to read the memory address that's stored in register `PC
            # Which is the current index in memory
            ir = self.ram_read(self.pc)
            # Sometimes the byte value is a register number,other times it's a constant value
            # Reg/Arg is one index over the pc
            operand_a = self.ram_read(self.pc + 1)
            # Value is one index over the pc
            operand_b = self.ram_read(self.pc + 2)
            # perform the actions needed for the instruction per the LS-8 spec
            if ir == LDI:
                # sets a specified register to a specified value.
                self.reg[operand_a] = operand_b
                self.pc += 3  # Add 3 to skip the operand_a & operand_b
            elif ir == PRN:
                print(self.reg[operand_a])  # Print value in given rgister
                self.pc += 2  # Add 2 to move to HLT
            elif ir == HLT:
                running = False
            else:
                print("Unknown instruction!")
                running = False

# cpu = CPU()
# cpu.load()
# cpu.run()
