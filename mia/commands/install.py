"""
Install MIA custom ROM to a device (real or emulated).

Usage:
  mia install [--emulator] [--skip-os] [--push-only] [--no-reboot] <definition>

Command options:
    --emulator   Use running emulator instead of a real device.
    --skip-os    Do not push base OS zip. (Prior push required for successful install.)
    --push-only  Only push the OS and update zips.
    --no-reboot  Do not reboot the device once all the files are in place.

"""

# Import custom helpers.
from mia.helpers.android import *
from mia.helpers.utils import *


def main():
    # Get the MIA handler singleton.
    handler = MiaHandler()

    # Create the builds folder.
    update_zip_name = '%s.%s' % (handler.args['<definition>'], 'mia-update.zip')
    update_zip_path = os.path.join(handler.get_workspace_path(), 'builds',
                                   update_zip_name)

    if not os.path.isfile(update_zip_path):
        # raise Exception('ERROR: Please run the build command first.')
        print('ERROR: Please run the build command first.')
        sys.exit(1)

    # Get the OS file name.
    os_zip_name = handler.get_os_zip_filename()
    os_zip_path = os.path.join(handler.get_workspace_path(), 'resources',
                               os_zip_name)

    if not os.path.isfile(os_zip_path):
        # raise Exception('ERROR: Please run the build command first.')
        print('ERROR: OS archive not found.')
        sys.exit(1)

    # Push the mia-update.zip to the device.
    push_file_to_device('update archive', update_zip_path,
                        '/sdcard/mia-update.zip')

    # Push the mia-os.zip to the device.
    if not handler.args['--skip-os']:
        push_file_to_device('OS archive', os_zip_path, '/sdcard/mia-os.zip')

    if handler.args['--push-only']:
        print('\n' + 'Finished pushing the files onto the device.')
        sys.exit(0)

    # Set the openrecoveryscript.
    set_open_recovery_script()

    if not handler.args['--no-reboot']:
        print('\n' + 'Rebooting the device into recovery...')
        reboot_device('recovery')