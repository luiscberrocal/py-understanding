import asyncio
import time

import httpx


async def main():
    pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'

    async with httpx.AsyncClient() as client:
        resp = await client.get(pokemon_url)
        pokemon = resp.json()
        print(pokemon['name'])


async def main2():
    async with httpx.AsyncClient() as client:
        for number in range(1, 151):
            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'

            resp = await client.get(pokemon_url)
            pokemon = resp.json()
            print(pokemon['name'])


asyncio.run(main())

if __name__ == '__main__':
    start_time = time.time()
    # asyncio.run(main())

    asyncio.run(main2())

    print("--- %s seconds ---" % (time.time() - start_time))
