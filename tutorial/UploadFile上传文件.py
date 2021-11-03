# -*- coding: utf-8 -*-
# @Time    : 2021/4/25 16:01
# @Author  : wanghao
# @File    : UploadFile上传文件.py
# @Software: PyCharm
import os
import time
import aiofiles
from typing import  List
from fastapi import FastAPI, UploadFile, File



app = FastAPI()


# 限制上传文件大小方案:https://github.com/tiangolo/fastapi/issues/362
@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    st = time.time()
    if not os.path.exists('./files'):
        os.mkdir('./files')
    try:
        for file in files:
            async with aiofiles.open(f'./files/{file.filename}','wb') as w:
                contents = await file.read()
                # print(contents)
                await w.write(contents)
            # with open(f'./files/{file.filename}','wb') as w:
            #     contents = await file.read()
            #     # print(contents)
            #     w.write(contents)

        return {"message": "success", 'time': time.time() - st,"filenames": [file.filename for file in files]}
    except Exception as e:
        return {"message": str(e), 'time': time.time() - st,"filenames": [file.filename for file in files]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='UploadFile上传文件:app', host="0.0.0.0", port=8001, reload=True)
