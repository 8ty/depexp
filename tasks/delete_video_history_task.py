from BiliClient import asyncbili
from queue import Queue
import logging

import asyncio
import random
import time
import datetime
import math


class DeleteVideoHistoryTask:

    def __init__(self, biliapi, enable, room_id, run_time = 5.5, delete_time = 0, sleep_time = 3):
        self.biliapi = biliapi
        self.enable = enable
        self.run_time = run_time * 60 * 60
        self.delete_time = delete_time if delete_time >= 0 else 0
        self.sleep_time = sleep_time
        self.start_time = time.time()
        if isinstance(room_id, str):
            self.room_id = room_id.split(',')
        elif isinstance(room_id, list):
            self.room_id = room_id
        else:
            self.room_id = [room_id]

    async def work(self):
        if not self.enable:
            return

        logging.info("检查删除视频历史任务")

        # 必须有房间号才能运行
        if not self.room_id:
            logging.warning("观看视频模块up主号未配置,已停止...")
        else:
            tasks = []
            for room_id in self.room_id:
                tasks.append(self.delete(room_id))
            if tasks:
                await asyncio.wait(map(asyncio.ensure_future, tasks))

    async def delete_video_history(self, room_id):
        count = 0
        video_history_data = await self.biliapi.getVideoHistory()
        for video_history in video_history_data['data']:
            if video_history['owner']['mid'] == room_id and video_history['progress'] == -1:
                count += 1
                if count <= self.delete_time:
                    continue
                kid = video_history['kid']
                await self.biliapi.deleteVideoHistory(kid)
                logging.info(f'删除视频 {video_history["title"]} 的观看历史记录')

    async def delete(self, room_id = None):
        while time.time() - self.start_time < self.run_time:
            if room_id is None:
                room_id = random.choice(self.room_id)

            await self.delete_video_history(room_id)
            await asyncio.sleep(self.sleep_time * 60)


async def delete_video_history_task(biliapi: asyncbili, task_config: dict) -> None:
    worker = DeleteVideoHistoryTask(biliapi, **task_config)
    await worker.work()
