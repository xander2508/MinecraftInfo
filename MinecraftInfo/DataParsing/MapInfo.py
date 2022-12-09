import json
import os
import re  # DELETE
import sys  # DELETE
import html2text
from itertools import groupby

from MinecraftInfo.Util.FileOpener import LoadWebJsonFile
from MinecraftInfo.Util.JsonQueries import GetClaimURL
from MinecraftInfo.DataParsing.SqlQueryHandler import SqlQueryHandler
from MinecraftInfo.Util.SqlQueries import (
    AddUser,
    AddCityClaim,
    LinkCityUsers,
    AddNationClaim,
    LinkNationCity,
    ClearClaimDatabase,
)


def UpdateClaimInfo(sqlQueryHandler: object) -> None:
    sqlQueryHandler.QueueQuery(ClearClaimDatabase)
    URL = GetClaimURL()
    WebJson = LoadWebJsonFile(URL)
    NationList = {}
    for Claim in WebJson["sets"]["me.angeschossen.lands"]["areas"]:
        NationList = ProcessClaim(
            WebJson["sets"]["me.angeschossen.lands"]["areas"][Claim],
            NationList,
            sqlQueryHandler,
        )
    for nation in NationList:
        AddNation(
            nation,
            NationList[nation][0],
            NationList[nation][1],
            NationList[nation][2],
            sqlQueryHandler,
        )


def ProcessClaim(claim: json, nationList, sqlQueryHandler: object) -> dict:
    XCoord = GetCoordAverage(claim["x"])
    ZCoord = GetCoordAverage(claim["z"])
    nationList = ProcessHTMLDesc(
        claim["desc"], XCoord, ZCoord, nationList, sqlQueryHandler
    )
    return nationList


def GetCoordAverage(coord: list) -> int:
    return int(sum(coord) / len(coord))


def ProcessHTMLDesc(
    HTML: str, XCoord: int, ZCoord: int, nationList: dict, sqlQueryHandler: object
) -> dict:
    RawList = html2text.html2text(HTML).split("\n")
    SplitList = [list(group) for k, group in groupby(RawList, bool) if k]

    CityName = SplitList[0][0].strip()
    CityLevel = SplitList[1][0].split(": ")[-1]
    CityChunks = SplitList[1][1].strip("  * Chunks: (.*)")
    CityPlayers = list(
        map(
            str.strip,
            (
                re.sub(f"  \* Players \([0-9]+\): ", "", SplitList[1][2])
                + "".join(SplitList[1][3:])
            ).split(","),
        )
    )
    AddCity(
        CityName, CityLevel, CityChunks, CityPlayers, XCoord, ZCoord, sqlQueryHandler
    )
    if len(SplitList) > 2:
        NationName = re.search(
            "\*\*This land belongs to nation (.*):\*\*", SplitList[2][0]
        ).group(1)
        NationLevel = SplitList[3][0].split(": ")[-1]
        NationCapital = SplitList[3][1].split(": ")[-1]
        NationLands = list(
            map(
                str.strip,
                (
                    re.sub(
                        f"  \* Lands \(total players: [0-9]+\): ", "", SplitList[3][2]
                    )
                    + "".join(SplitList[3][3:])
                ).split(","),
            )
        )
        if NationName not in nationList:
            nationList[NationName] = [NationLevel, NationCapital, NationLands]
    return nationList


def AddNation(
    nationName: str,
    nationLevel: str,
    nationCapital: str,
    nationLands: list,
    sqlQueryHandler: object,
) -> None:
    sqlQueryHandler.QueueQuery(AddNationClaim, nationName, nationLevel, nationCapital)
    for cityName in nationLands:
        sqlQueryHandler.QueueQuery(LinkNationCity, nationName, cityName)


def AddCity(
    cityName: str,
    cityLevel: str,
    cityChunks: int,
    cityPlayers: list,
    XCoord: int,
    ZCoord: int,
    sqlQueryHandler: object,
) -> None:
    sqlQueryHandler.QueueQuery(
        AddCityClaim, cityName, cityLevel, cityChunks, XCoord, ZCoord
    )
    for player in cityPlayers:
        sqlQueryHandler.QueueQuery(AddUser, player)
        sqlQueryHandler.QueueQuery(LinkCityUsers, player, cityName)
