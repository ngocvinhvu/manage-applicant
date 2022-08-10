from faker import Faker
from random import randrange
from datetime import datetime

num_of_applicants = 1000

fake = Faker("vi_VI")

applicants = []

for customers_id in range(num_of_applicants):
    # Create date of birth
    d1 = datetime.strptime(f"1990/1/1", "%Y/%m/%d")
    d2 = datetime.strptime(f"2010/1/1", "%Y/%m/%d")
    dob = fake.date_between(d1, d2)

    # create customer's name
    name = fake.name()

    # Create email
    email = fake.ascii_email()

    applicant = {}
    applicant.update({"name": name, "email": email, "dob": dob, "country": "VIETNAM"})
    applicants.append(applicant)
