"""Testing functions for 2016 Day 8"""
from sol import Screen


def test_screen_operations():
    """Test screen operations and instructions on a small example"""
    print("Init 3x7 Screen")
    screen = Screen(height=3, width=7)
    print(screen.display())

    instructions: list[str] = [
        "rect 3x2",
        "rotate column x=1 by 1",
        "rotate row y=0 by 4",
        "rotate column x=1 by 1"
    ]
    for instruction in instructions:
        print(instruction)
        screen.parse_and_apply_instruction(instruction)
        print(screen.display())


if __name__ == "__main__":
    test_screen_operations()
