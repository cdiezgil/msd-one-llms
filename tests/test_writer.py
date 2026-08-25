import pytest
from unittest.mock import patch, MagicMock
from hid_driver.writer import send_image

def test_send_image_success():
    with patch('hid_driver.writer.hid.device') as mock_hid:
        mock_device = MagicMock()
        mock_hid.return_value = mock_device

        key_id = 5
        jpeg_bytes = b'A' * 600

        send_image(key_id, jpeg_bytes)

        mock_device.open.assert_called_once_with(0x0b00, 0x1000)
        
        # Should be called for init, 2 chunks (600 bytes), and flush = 4 calls total
        assert mock_device.write.call_count == 4
        
        # Init packet
        init_call_args = mock_device.write.call_args_list[0][0][0]
        assert len(init_call_args) == 512
        assert init_call_args[0:3] == b'\x43\x52\x54'
        assert init_call_args[10:12] == bytes([(600 >> 8) & 0xFF, 600 & 0xFF])
        assert init_call_args[12] == 5

        # Chunk 1
        chunk1_call_args = mock_device.write.call_args_list[1][0][0]
        assert len(chunk1_call_args) == 512
        assert chunk1_call_args == b'A' * 512

        # Chunk 2
        chunk2_call_args = mock_device.write.call_args_list[2][0][0]
        assert len(chunk2_call_args) == 512
        assert chunk2_call_args[:88] == b'A' * 88
        assert chunk2_call_args[88:] == b'\x00' * (512 - 88)

        # Flush packet
        flush_call_args = mock_device.write.call_args_list[3][0][0]
        assert len(flush_call_args) == 512
        assert flush_call_args[0:8] == b'\x43\x52\x54\x00\x00\x53\x54\x50'

        mock_device.close.assert_called_once()

def test_send_image_device_not_found():
    with patch('hid_driver.writer.hid.device') as mock_hid:
        mock_device = MagicMock()
        mock_device.open.side_effect = IOError("Device not found")
        mock_hid.return_value = mock_device

        # Should not raise exception
        send_image(1, b'abc')

        mock_device.open.assert_called_once_with(0x0b00, 0x1000)
        mock_device.write.assert_not_called()
