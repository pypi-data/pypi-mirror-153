import time

# pylint: disable=import-error
from tests import volume_tests as vol, compute_tests as comp

volume = "test-volume"

vol.test_volume_create(volume)
time.sleep(3)

vol.test_volume_list(volume)
comp.test_compute_create(volume)
time.sleep(3)

comp.test_compute_list(volume)
comp.test_compute_delete()
vol.test_volume_delete(volume)
time.sleep(3)

comp.test_compute_list()
vol.test_volume_list()
