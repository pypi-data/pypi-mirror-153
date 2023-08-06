from httpx import AsyncClient
from pathlib import Path
from typing import Union

class R3nzSkin():

    @classmethod
    async def skinGetLatest(cls) -> Union[dict, None]:
        async with  AsyncClient() as client:
            result = await client.get("https://api.github.com/repos/R3nzTheCodeGOD/R3nzSkin/releases/latest")
            client.aclose()
        return result.json()

    @classmethod
    def isUpdate(cls, arg) -> bool:
        path = Path(__file__).parent
        with open(path / "latest", "r") as file:
            version = file.read()
            if arg == version.strip("\n"):
                file.close()
                return False
            else:
                file.close()
                return True

    @classmethod
    def writeVersion(cls, arg) -> None:
        path = Path(__file__).parent
        with open(path / "latest", "r") as file:
            file.truncate()
            file.write(arg)
            file.close()
        return None


    @classmethod
    def toMessage(cls, data) -> str:
        return f"""{data['name']}
作者：{data['author']['login']}
版本：{data['tag_name']}
描述：{data['body']}
更新日期：{data['published_at']}
下载链接：{data['assets'][0]['browser_download_url']}"""