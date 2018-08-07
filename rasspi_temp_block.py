import subprocess
from nio import Block
from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.properties import VersionProperty


class RasPiTemp(EnrichSignals, Block):

    version = VersionProperty('0.1.0')

    def process_signals(self, signals):
        outgoing_signals = []
        for signal in signals:
            raw_temp=subprocess.check_output(['/opt/vc/bin/vcgencmd','measure_temp']).decode()
            temp = float(raw_temp.split('=')[-1].split('\'')[0])
            new_signal = self.get_output_signal({'temp_C': temp}, signal)
            outgoing_signals.append(new_signal)
        self.notify_signals(outgoing_signals)
