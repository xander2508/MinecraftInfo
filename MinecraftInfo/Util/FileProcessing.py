import base64
import json
from MinecraftInfo.Util.JsonQueries import GetMapPath
from MinecraftInfo.Util.JsonQueries import GetAPI_URL, GetRenderURL
import requests
import cv2
import numpy as np
import copy

from MinecraftInfo.Util.WebsiteSqlQueries import GetClaimInfo


def GetMap() -> dict:
    Filepath = "./MinecraftInfo/DataStorage/Map/" + GetMapPath()
    Image = cv2.imread(Filepath, cv2.IMREAD_UNCHANGED)
    return Image


def GenerateMap(Map: dict, Claims: dict, Names: bool, Capital: str = "None") -> str:
    # Names
    # False = None
    # True = Capital
    NewMap = copy.deepcopy(Map)

    CaptialX = 0
    CaptialZ = 0
    Size = 50
    ImageArray = np.full((4717, 4717, 4), (255, 255, 255, 0), np.uint8)
    for Claim in Claims:
        _, ClaimCoords, _, _, _ = GetClaimInfo(Claim)
        ClaimCoordsXZ = ClaimCoords.split(",")
        X = int((int(ClaimCoordsXZ[0]) + 7500) / 3.17998728005)
        Z = int((int(ClaimCoordsXZ[1]) + 7500) / 3.17998728005)
        cv2.line(
            ImageArray, (X - Size, Z - Size), (X + Size, Z + Size), (0, 0, 0, 255), 40
        )
        cv2.line(
            ImageArray, (X + Size, Z - Size), (X - Size, Z + Size), (0, 0, 0, 255), 40
        )
        cv2.line(
            ImageArray, (X - Size, Z - Size), (X + Size, Z + Size), (0, 0, 255, 255), 20
        )
        cv2.line(
            ImageArray, (X + Size, Z - Size), (X - Size, Z + Size), (0, 0, 255, 255), 20
        )
        if Names and Claim == Capital:
            CaptialX = X
            CaptialZ = Z
    if Names:
        try:
            Font = cv2.FONT_HERSHEY_SIMPLEX
            TextSize = cv2.getTextSize(Capital, Font, 5, 10)[0]
            TextX = int(TextSize[0] / 2)
            TextZ = int(TextSize[1] / 2)
            cv2.putText(
                ImageArray,
                Capital,
                (CaptialX - TextX, CaptialZ + TextZ - Size * 3),
                Font,
                5,
                (255, 255, 255, 255),
                40,
            )
            cv2.putText(
                ImageArray,
                Capital,
                (CaptialX - TextX, CaptialZ + TextZ - Size * 3),
                Font,
                5,
                (0, 0, 0, 255),
                30,
            )
            cv2.putText(
                ImageArray,
                Capital,
                (CaptialX - TextX, CaptialZ + TextZ - Size * 3),
                Font,
                5,
                (0, 0, 255, 255),
                10,
            )
        except:
            pass
    y1, y2 = 0, 0 + ImageArray.shape[0]
    x1, x2 = 0, 0 + ImageArray.shape[1]
    alpha_s = ImageArray[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    for c in range(0, 3):
        NewMap[y1:y2, x1:x2, c] = (
            alpha_s * ImageArray[:, :, c] + alpha_l * NewMap[y1:y2, x1:x2, c]
        )
    Base64PNG = base64.b64encode(cv2.imencode(".png", NewMap)[1]).decode()

    NewMap = (
        "<img id='base64image' width='70%' height='70%' src='data:image/png;base64, "
        + Base64PNG
        + "' />"
    )
    return NewMap


def GetUserModel(user: str) -> str:
    API_URL = GetAPI_URL()
    RenderURL = GetRenderURL()
    Headers = {"Content-Type": "application/json"}

    Session = requests.Session()
    Response = Session.post(API_URL, headers=Headers, data='"' + user + '"')
    try:
        ID = json.loads(Response.text)[0]["id"]
    except:
        return ""
    return '<img src="' + RenderURL + ID + '?overlay=true"><br>'
