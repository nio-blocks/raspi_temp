from unittest.mock import patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..raspi_temp_block import RasPiTemp


class TestRasPiTemp(NIOBlockTestCase):

    @patch(RasPiTemp.__module__ + '.subprocess')
    def test_process_signals(self, mock_subprocess):
        """Signals are enriched with CPU temperature."""
        mock_subprocess.call.return_value = b'temp=3.14'C\n'
        blk = RasPiTemp()
        self.configure_block(blk, {'enrich': {'exclude_existing': False}})
        blk.start()
        blk.process_signals([Signal({'foo': 'bar'})])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'temp_C': 3.14, 'foo': 'bar'})
