from brain.smart_exit import SmartExit

def run_test():

    smart = SmartExit()

    position = {
        "id": 1,
        "side": "LONG",
        "entry": 50,
        "size": 1
    }

    print("========== SMART EXIT TEST ==========\n")

    # 1. Small Profit
    print("Price = 52")
    print(smart.decide(position, 52))

    # 2. Partial Profit
    print("\nPrice = 53")
    print(smart.decide(position, 53))

    # 3. Profit Lock
    print("\nPrice = 55")
    print(smart.decide(position, 55))

    # 4. Trailing Protection (still safe)
    print("\nPrice = 54.5")
    print(smart.trailing_check(position, 54.5))

    # 5. Trailing Stop Trigger
    print("\nPrice = 53")
    print(smart.trailing_check(position, 53))


if __name__ == "__main__":
    run_test()
