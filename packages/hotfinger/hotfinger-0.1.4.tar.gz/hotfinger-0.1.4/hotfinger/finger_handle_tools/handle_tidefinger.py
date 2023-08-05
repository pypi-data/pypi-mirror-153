#!/usr/bin/env python
# coding=utf-8

"""
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-05-31 21:57:44
LastEditors: zmf96
LastEditTime: 2022-05-31 22:46:57
FilePath: /hotfinger/finger_handle_tools/handle_tidefinger.py
Description: 
"""

import json
import sqlite3

import bson
from cp_common.log import logger


def cmsfinger2json():
    conn = sqlite3.connect("./cms_finger.db")
    c = conn.cursor()

    cursor = c.execute("select * from tide;")
    tidefinger = {}
    for row in cursor:
        # logger.info(row)
        tidefinger[row[1]] = row
    conn.close()
    with open("tide2.json", "w", encoding="utf-8") as f:
        json.dump(tidefinger, f, indent=4, ensure_ascii=False)
    return tidefinger


def getfinger():
    with open("../data/hotfinger_v3.json", "r") as f:
        hotfinger = json.load(f)
    return hotfinger


def save2json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    tidefinger = cmsfinger2json()

    logger.info(len(tidefinger))

    hotfinger = getfinger()
    logger.info(len(hotfinger))

    hotfinger_set = set()
    tide_set = set(tidefinger)

    for item in hotfinger:
        hotfinger_set.add(item["name"])

    difffinger = sorted(tide_set - hotfinger_set)
    tide_set = sorted(tide_set)
    hotfinger_set = sorted(hotfinger_set)

    logger.info(difffinger)

    save2json("./tide_set.json", tide_set)
    save2json("./hotfinger_set.json", hotfinger_set)
    save2json("./diffinger.json", difffinger)

    finger_v4 = []

    for item in difffinger:
        logger.info(item)
        finger_v4.append(
            {
                "_id": {"$oid": str(bson.ObjectId())},
                "name": tidefinger[item][1],
                "content": {"/": tidefinger[item][2]},
                "tags": ["tide2"],
            }
        )
    save2json("./finger_v4.json", finger_v4)


if __name__ == "__main__":
    main()
