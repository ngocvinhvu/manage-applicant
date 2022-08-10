import os
from faker import Faker
from datetime import datetime
from config import config
import aiohttp
import asyncio


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]


num_of_applicants = 1000

fake = Faker('de_DE')

applicants = []

for customers_id in range(num_of_applicants):
    # Create applicant date of birth 
    d1 = datetime.strptime(f'1990/1/1', '%Y/%m/%d')
    d2 = datetime.strptime(f'2010/1/1', '%Y/%m/%d')
    dob = fake.date_between(d1, d2)

    #create applicant's name
    name = fake.name()
    
    # Create email 
    email = fake.ascii_email()

    applicant = {}
    applicant.update({"name": name, "email": email, "dob": str(dob).replace("-", "/"), "country": "VIETNAM"})
    applicants.append(applicant)


async def main():
    async with aiohttp.ClientSession() as session:
        for applicant in applicants:
            pokemon_url = f"{CONF.API_URL}/applicants"
            async with session.post(url=pokemon_url, json=applicant) as resp:
                applicant = await resp.json()


def run():
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
