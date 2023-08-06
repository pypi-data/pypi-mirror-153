import statsd


def makeStatsdClient():
    return statsd.StatsClient("192.168.255.35", 8125, prefix="cgc-client")


def incrementMetric(metric):
    client = makeStatsdClient()
    client.incr(metric, 1)


def changeGauge(metric, value):
    client = makeStatsdClient()
    client.gauge(metric, value, delta=True)


def setupGauge(metric, value):
    client = makeStatsdClient()
    client.gauge(metric, value)


# incrementMetric("volume.create")
# changeGauge("volume.count", 8)
# print("metric sent")
# c.timing("stats.timed", 320)
# print("dupa")
