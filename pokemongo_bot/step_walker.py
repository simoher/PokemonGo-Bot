import logger

from cell_workers.utils import distance, i2f, format_time, format_dist
from human_behaviour import random_lat_long_delta, sleep
from math import ceil, sqrt


class StepWalker(object):

    def __init__(self, bot, speed, initLat, initLng, destLat, destLng):
        self.bot = bot
        self.api = bot.api

        dist = distance(
            i2f(initLat),
            i2f(initLng),
            destLat,
            destLng
        )

        self.speed = speed

        self.destLat = destLat
        self.destLng = destLng

        self.steps = (dist + 0.0) / (speed + 0.0)

        if dist < 0.01 or self.steps < 1:
            self.dLat = 0
            self.dLng = 0
            self.magnitude = 0;
        else:
            self.dLat = (destLat - i2f(initLat)) / self.steps
            self.dLng = (destLng - i2f(initLng)) / self.steps
            self.magnitude = self._pythagorean(self.dLat, self.dLng)

    def step(self):
        dist = distance(
            i2f(self.api._position_lat),
            i2f(self.api._position_lng),
            self.destLat,
            self.destLng
        )
        # print 'distance'
        # print dist

        if (self.dLat == 0 and self.dLng == 0) or dist < 15:
            return True

        totalDLat = (self.destLat - i2f(self.api._position_lat))
        totalDLng = (self.destLng - i2f(self.api._position_lng))
        magnitude = self._pythagorean(totalDLat, totalDLng)
        unitLat = totalDLat / magnitude
        unitLng = totalDLng / magnitude

        scaledDLat = unitLat * self.magnitude
        scaledDLng = unitLng * self.magnitude

        cLat = i2f(self.api._position_lat) + scaledDLat + random_lat_long_delta()
        cLng = i2f(self.api._position_lng) + scaledDLng + random_lat_long_delta()

        self.api.set_position(cLat, cLng, 0)
        self.bot.heartbeat()
        sleep(1)  # sleep one second plus a random delta
        # self._work_at_position(
        #     i2f(self.api._position_lat), i2f(self.api._position_lng),
        #     alt, False)

    def _pythagorean(self, lat, lng):
        return sqrt((lat ** 2) + (lng ** 2))
