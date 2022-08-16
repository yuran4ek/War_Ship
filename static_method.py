try:
    number = int(input("Input number: "))
except ValueError as e:
    print("Mistake in number")
else:
    print(f"You are enter the {number}")
finally:
    print("Close the programm")
