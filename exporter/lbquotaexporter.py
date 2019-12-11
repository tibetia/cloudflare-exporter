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

        families['loadbalancers'].add_metric([zone, pop_data['name']], 1)

    families = {
        'loadbalancers': GaugeMetricFamily(
            'loadbalancer',
            'Created loadbalancers',
            labels=[
                'zone',
                'name'
            ]
        )
    }

    for pop_data in raw_data:
        generate_metrics(pop_data, families)
    return generate_latest(RegistryMock(families.values()))


if __name__ == "__main__":
    import os

    source_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(source_dir, "sample-lbs")

    with open(path) as f:
        print(process(json.load(f)['result']))
