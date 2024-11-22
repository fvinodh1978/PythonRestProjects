import random
import datetime
def generate_data():
    random_number = random.randint(1, 100)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Random number: {random_number}, Time: {current_time}"

if __name__ == "__main__":
    output = generate_data()
    print(output)