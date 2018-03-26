from base import LogService
import time

priority = 60000
retries = 60
# update_every = 3

ORDER = ['intel_gpu']
CHARTS = {
    'intel_gpu': {
        'options': [None, 'Intel GPU usage', 'percent', 'usage', 'intel_gpu.usage', 'line'],
        'lines': [
            ["render"],
            ["bitstream"],
            ["blitter"]
        ]
    }
}

class Service(LogService):
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)

        self.log_path = self.configuration.get('path', '/var/log/intel_gpu_top.log')
        self.order = ORDER
        self.definitions = CHARTS
        self.cnt = 0

    def _get_data(self):
        if self.cnt == 0:
            time.sleep(1)
        for i in range(0,15):
            try:
                raw = self._get_raw_data()
                if raw is None or not raw:
                    time.sleep(0.1)
                    continue
                else:
                    break
            except (ValueError, AttributeError):
                print "intel_gpu _get_raw_data() error"
                return None

        if raw is None or not raw:
            print "intel_gpu _get_raw_data() no data"
            return None
            
        row = raw[-1].split()

        if row[0] == "#":
            print "intel_gpu row[0] is hash"
            return None

        ret = {'render': row[1],
               'bitstream': row[3] if row[3] != "-1" else row[5]}

        if row[7] != "-1":
            ret['blitter'] = row[7]

        self.cnt += 1

        return ret
