# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/14 3:19 pm
# @File    : upload_files.py
# @Software: PyCharm
"""

from fastapi import APIRouter
from fastapi import File, UploadFile

from yeti.cfg import CONF

router = APIRouter(tags=["files"]
                   )


@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    content_type = file.content_type
    data = await file.read()
    # in byte
    file_size = len(data)

    print(len(data))

    return {"filename": file.filename}
