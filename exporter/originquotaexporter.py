#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json

from prometheus_client.core import GaugeMetricFamily
from prometheus_client.exposition import generate_latest


#def process(raw_data, zone):
def process(raw_data):
    class RegistryMock(object):
        def __init__(self, metrics):
            self.metrics = metrics

        def collect(self):
            for metric in self.metrics:
                yield metric

    def generate_metrics(pop_data, families):
	data = pop_data['origins']

        for i in range(0, len(data), 1):
            #print data[i]['name']

            families['loadbalancer_origins'].add_metric(
	        [data[i]['name'], str(data[i]['address']), 
		str(data[i]['enabled']), str(data[i]['weight'])], 1)

    families = {
        'loadbalancer_origins': GaugeMetricFamily(
            'loadbalancer_pool_origin',
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
