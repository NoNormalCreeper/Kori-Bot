import httpx


class dataApi():
    '''
    从网易云音乐接口直接获取数据（实验性）
    '''
    headers = {"referer": "http://music.163.com"}
    cookies = {"appver": "2.0.2"}

    async def search(self, songName: str):
        '''
        搜索接口，用于由歌曲名查找id
        '''
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"http://music.163.com/api/search/get/",
                data={"s": songName, "limit": 5, "type": 1, "offset": 0},
                headers=self.headers,
                cookies=self.cookies
            )
        jsonified_r = r.json()
        if "result" not in jsonified_r:
            raise APINotWorkingException(r.text)
        return jsonified_r

    async def getHotComments(self, songId: int):
        '''
        获取热评
        '''
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"https://music.163.com/weapi/v1/resource/hotcomments/R_SO_4_{songId}?csrf_token=",
                data={
                    # 不知道从哪毛来的key
                    "params": 'D33zyir4L/58v1qGPcIPjSee79KCzxBIBy507IYDB8EL7jEnp41aDIqpHBhowfQ6iT1Xoka8jD+0p44nRKNKUA0dv+n5RWPOO57dZLVrd+T1J/sNrTdzUhdHhoKRIgegVcXYjYu+CshdtCBe6WEJozBRlaHyLeJtGrABfMOEb4PqgI3h/uELC82S05NtewlbLZ3TOR/TIIhNV6hVTtqHDVHjkekrvEmJzT5pk1UY6r0=',
                    "encSecKey": '45c8bcb07e69c6b545d3045559bd300db897509b8720ee2b45a72bf2d3b216ddc77fb10daec4ca54b466f2da1ffac1e67e245fea9d842589dc402b92b262d3495b12165a721aed880bf09a0a99ff94c959d04e49085dc21c78bbbe8e3331827c0ef0035519e89f097511065643120cbc478f9c0af96400ba4649265781fc9079'
                },
                headers=self.headers,
                cookies=self.cookies
            )
        jsonified_r = r.json()
        if "hotComments" not in jsonified_r:
            raise APINotWorkingException(r.text)
        return jsonified_r

    async def getSongInfo(self, songId: int):
        '''
        获取歌曲信息
        '''
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"http://music.163.com/api/song/detail/?id={songId}&ids=%5B{songId}%5D",
            )
        jsonified_r = r.json()
        if "songs" not in jsonified_r:
            raise APINotWorkingException(r.text)
        return jsonified_r


class dataGet(dataApi):
    '''
    从dataApi获取数据，并做简单处理
    '''

    api = dataApi()

    async def songIds(self, songName: str, amount=5) -> list:
        '''
        根据用户输入的songName 获取候选songId列表 [默认songId数量：5]
        '''
        songIds = list()
        r = await self.api.search(songName=songName)
        idRange = amount if amount < len(
            r["result"]["songs"]) else len(r["result"]["songs"])
        for i in range(idRange):
            songIds.append(r["result"]["songs"][i]["id"])
        return songIds

    async def songComments(self, songId: int, amount=3) -> dict:
        '''
        根据传递的单一songId，获取songComments dict [默认评论数量上限：3]
        '''
        songComments = dict()
        r = await self.api.getHotComments(songId)
        commentsRange = amount if amount < len(
            r['hotComments']) else len(r['hotComments'])
        for i in range(commentsRange):
            songComments[r['hotComments'][i]['user']
                         ['nickname']] = r['hotComments'][i]['content']
        return songComments

    async def songInfo(self, songId: int) -> dict:
        '''
        根据传递的songId，获取歌曲名、歌手、专辑等信息，作为dict返回
        '''
        songInfo = dict()
        r = await self.api.getSongInfo(songId)
        songInfo["songName"] = r["songs"][0]["name"]
        songArtists = list()
        for ars in r["songs"][0]["artists"]:
            songArtists.append(ars["name"])
        songArtistsStr = "、".join(songArtists)
        songInfo["songArtists"] = songArtistsStr

        songInfo["songAlbum"] = r["songs"][0]["album"]["name"]

        return songInfo


class dataProcess():
    '''
    将获取的数据处理为用户能看懂的形式
    '''

    @staticmethod
    async def mergeSongInfo(songInfos: list) -> str:
        '''
        将歌曲信息list处理为字符串，供用户点歌
        传递进的歌曲信息list含有多个歌曲信息dict
        '''
        songInfoMessage = "请输入欲点播歌曲的序号：\n"
        numId = 0
        for songInfo in songInfos:
            songInfoMessage += f"{numId}："
            songInfoMessage += songInfo["songName"]
            songInfoMessage += "-"
            songInfoMessage += songInfo["songArtists"]
            songInfoMessage += " 专辑："
            songInfoMessage += songInfo["songAlbum"]
            songInfoMessage += "\n"
            numId += 1
        return songInfoMessage

    @staticmethod
    async def mergeSongComments(songComments: dict) -> str:
        songCommentsMessage = '\n'.join(
            ['%s： %s' % (key, value) for (key, value) in songComments.items()])
        return songCommentsMessage


class APINotWorkingException(Exception):
    def __init__(self, wrongData):
        self.uniExceptionTip="网易云音乐接口返回了意料之外的数据：\n"
        self.wrongData = wrongData

    def __str__(self):
        return self.uniExceptionTip+self.wrongData
