import aiohttp


async def make_url(img_bytes):
    url = 'https://telegra.ph/upload'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={'file': img_bytes}) as response:
            if response.status == 200:
                data = await response.json()
                image_url = "https://telegra.ph" + data[0]['src']
                return image_url
            else:
                print(f"Error uploading file: {response.status}")
                return None
