#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json

from prometheus_client.core import GaugeMetricFamily
from prometheus_client.exposition import generate_latest


def process(raw_data, zone):
    class RegistryMock(object):
        def __init__(self, metrics):
            self.metrics = metrics

        def collect(self):
            for metric in self.metrics:
                yield metric

    def generate_metrics(pop_data, families):
	count = 0
	origin_data = pop_data['origins']

        for i in range(0, len(origin_data), 1):
            count = count + 1
            #print origin_data[i]['name']

            families['lb_origins'].add_metric(
	        [origin_data[i]['name'], str(origin_data[i]['address']), 
		str(origin_data[i]['enabled']), str(origin_data[i]['weight'])], 1)

    families = {
        'lb_origins': GaugeMetricFamily(
            'loadbalancer_pool_origins',
            'Created origins',
            labels=[
                'name',
                'address',
                'enabled',
                'weight'
            ]
        )
    }

    for pop_data in raw_data:
        generate_metrics(pop_data, families)
    return generate_latest(RegistryMock(families.values()))


if __name__ == "__main__":
    import os

    source_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(source_dir, "sample-origin")

    with open(path) as f:
        print(process(json.load(f)['result']))
