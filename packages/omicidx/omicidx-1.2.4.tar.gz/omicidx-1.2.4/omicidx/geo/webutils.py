import httpx
import asyncio
import logging
from io import StringIO
from tenacity import retry
from tenacity.stop import stop_after_attempt
from . import parser as gp
from asyncio import Semaphore

lock = Semaphore(10)

def jsonify(txt):
    entity = []
    accession = None
    in_table = False
    for line in StringIO(txt):
        try:
            if (isinstance(line, bytes)):
                line = line.decode()
        except:
            pass
        line = line.strip()

        # ignore table details for now

        if (line.endswith('table_begin')):
            in_table = True
        if (line.endswith('table_end')):
            in_table = False
            continue
        if (in_table):
            continue

        # ignore comments

        if (line.startswith('#')):
            continue

        if (line.startswith('^')):
            if (accession is not None):
                yield (gp._parse_single_entity_soft(entity))
            accession = gp._split_on_first_equal(line)[1]
            entity = []

        entity.append(line)
    yield (gp._parse_single_entity_soft(entity))


async def get_geo_accession_soft(accession: str, targ: str='all', view: str= "brief"):
    logging.info(f'Accessing accession {accession} in SOFT format')
    url = (
        "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?targ={}&acc={}&form=text&view={}"
        .format(targ, accession, view))
    
    @retry(stop=stop_after_attempt(10))
    async def _perform_get(url: str) -> str:
        logging.info(f"fetching{url}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
        return resp.text

    res = await _perform_get(url)
    for i in jsonify(res):
        yield(i.json())


async def stuff(acc):
    print('here')
    async with lock:
        async for i in get_geo_accession_soft(acc):
            print(i)

async def abc():
    results = asyncio.gather(*[stuff(acc) for acc in gp.get_geo_accessions(etyp='GSE',batch_size=10)])

if __name__ == '__main__':
    asyncio.run(abc())