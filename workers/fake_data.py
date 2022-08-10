import os, json
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
    fake = Faker('de_DE')
    applicants = []
    for i in range(num_of_applicants):
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
    return applicants


# Async and concurrency http post request 
async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)
    async def sem_task(task):
        async with semaphore:
            return await task
   
    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def post_async(url, session, body):
    count_success = 0
    count_failed = 0
    try:
        async with session.post(url, json=body) as response:
            text = await response.text()
            count_success += 1
    except Exception:
        count_failed += 1
    return count_success, count_failed


async def main():
    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    session = aiohttp.ClientSession(connector=conn)
    url = CONF.API_URL + "/applicants"
    conc_req = 10
    _ = await gather_with_concurrency(conc_req, *[post_async(url, session, applicant) for applicant in make_list_dummy_applicants(1000)])


def run():
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
