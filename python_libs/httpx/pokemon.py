import asyncio
import httpx


async def main():
    pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'

    async with httpx.AsyncClient() as client:
        resp = await client.get(pokemon_url)
        pokemon = resp.json()
        print(pokemon['name'])


if __name__ == '__main__':
    asyncio.run(main())
