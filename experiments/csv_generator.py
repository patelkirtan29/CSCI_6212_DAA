import random
import csv
import time
from faker import Faker
start_time = time.time()
# Initialize the Faker library to generate random data
fake = Faker()

# List of GWU departments
departments = [
    "School of Engineering & Applied Science",
    "College of Professional Studies",
    "School of Business",
    "Department of Computer Science",
    "Department of Electrical Engineering",
    "Department of Mechanical & Aerospace Engineering",
    "Department of Mathematics",
    "Department of Physics",
    "School of Medicine & Health Sciences",
    "Department of Public Policy",
    "Department of History",
    "Department of Political Science",
    "Department of Psychology",
    "School of Law",
    "School of Education",
    "Department of Sociology",
    "Department of Environmental Science",
    "Department of Anthropology",
    "Department of Economics",
    "Department of Geography"
]

# List of cities (just a sample)
cities = ["Washington", "New York", "Los Angeles", "Chicago", "San Francisco", "Boston", "Seattle", "Miami", "Dallas", "Denver"]

# Function to generate a single record
def generate_record(i):
    firstname = fake.first_name()
    lastname = fake.last_name()
    email = f"{firstname.lower()}.{lastname.lower()}@example.com"
    phone = fake.phone_number()
    city = random.choice(cities)
    score = random.randint(0, 1000)
    department = random.choice(departments)
    print("lines", i)
    return [firstname, lastname, email, phone, city, score, department]

# Generate a list of records
num_records = 10  # Generating 1 million records
records = [generate_record(_) for _ in range(num_records)]

# Writing the generated records to a CSV file
file_name = "gwu_gradebook1.csv"
header = ["firstname", "lastname", "email", "phone", "city", "score", "department"]

# Write to the CSV file
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(records)
# End timing
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Program completed in {elapsed_time:.2f} seconds.")
print(f"CSV file with {num_records} records has been generated: {file_name}")
