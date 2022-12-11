from prefect import flow

@flow
def my_favorite_function():
    print("What is your favorite number?")
    return 42

@flow
def basic_favorite():
    print(f"Mine is: {my_favorite_function()}")

if __name__ == "__main__":
    basic_favorite()