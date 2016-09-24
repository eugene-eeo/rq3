import statistics as stats


def stdev_mean(target):
    def metric(box, data):
        mean = stats.mean(box.seq(data))
        stdev = 0 if box.dimensions() == 1 else \
            stats.pstdev(box.seq(data), mu=mean)
        return (
            stdev > target,
            mean,
            )
    return metric
