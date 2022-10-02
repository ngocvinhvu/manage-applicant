import os
import random
from faker import Faker
from datetime import datetime
from config import config
import aiohttp
import asyncio


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]

# Make a list of fake Applican's Infomations
def make_list_dummy_applicants(num):
    num_of_applicants = num
    fake = Faker("de_DE")
    applicants = []
    for i in range(num_of_applicants):
        # Create applicant date of birth
        d1 = datetime.strptime(f"1990/1/1", "%Y/%m/%d")
        d2 = datetime.strptime(f"2010/1/1", "%Y/%m/%d")
        dob = fake.date_between(d1, d2)
        # create applicant's name
        name = fake.name()
        identify_number = random.randrange(111111111, 999999999)
        phone_number = random.randrange(111111111, 999999999)
        # Create email
        email = fake.ascii_email()
        applicant = {}
        applicant.update(
            {
                "name": name,
                "email": email,
                "dob": str(dob).replace("-", "/"),
                "country": "Hanoi",
                "identify_number": identify_number,
                "phone_number": f"+84{phone_number}",
                "permanent_residence": "Hanoi",
                "nationality": "VIETNAM",
                "new_applicant": False,
                "place": "Hanoi"
            }
        )
        applicants.append(applicant)
    return applicants


# Async and concurrency http post request
async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def post_async(url, session, body):
    try:
        async with session.post(url, json=body) as response:
            _ = await response
            return
    except Exception:
        return


async def main():
    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    session = aiohttp.ClientSession(connector=conn)
    url = CONF.API_URL + "/applicants"
    conc_req = 10
    await gather_with_concurrency(
        conc_req,
        *[
            post_async(url, session, applicant)
            for applicant in make_list_dummy_applicants(1000)
        ],
    )


def run():
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
