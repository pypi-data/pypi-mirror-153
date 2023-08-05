# -*- coding: utf-8 -*-
"""
This module contains functions for turning a Python script into a .hex file
and flashing it onto a BBC micro:bit.

Copyright (c) 2015-2018 Nicholas H.Tollervey and others.

See the LICENSE file for more information, or visit:

https://opensource.org/licenses/MIT
"""

from __future__ import print_function

import argparse
import binascii
import ctypes
import os
import struct
import sys
import shutil
import base64, re
from io import BytesIO

from subprocess import check_output
import time

# nudatus is an optional dependancy
can_minify = True
try:
    import nudatus
except ImportError:  # pragma: no cover
    can_minify = False

#: The magic start address in flash memory for a Python script.
_SCRIPT_ADDR = 0x3e000


#: The help text to be shown when requested.
_HELP_TEXT = """
Flash Python onto the BBC micro:bit or extract Python from a .hex file.

If no path to the micro:bit is provided uflash will attempt to autodetect the
correct path to the device. If no path to the Python script is provided uflash
will flash the unmodified MicroPython firmware onto the device. Use the -e flag
to recover a Python script from a hex file. Use the -r flag to specify a custom
version of the MicroPython runtime.

Documentation is here: https://uflash.readthedocs.io/en/latest/
"""


#: MAJOR, MINOR, RELEASE, STATUS [alpha, beta, final], VERSION of uflash
_VERSION = (1, 2, 4, )
_MAX_SIZE = 8188


#: The version number reported by the bundled MicroPython in os.uname().
MICROPYTHON_VERSION = '1.0.1'


def get_version():
    """
    Returns a string representation of the version information of this project.
    """
    return '.'.join([str(i) for i in _VERSION])


def get_minifier():
    """
    Report the minifier will be used when minify=True
    """
    if can_minify:
        return 'nudatus'
    return None


def strfunc(raw):
    """
    Compatibility for 2 & 3 str()
    """
    return str(raw) if sys.version_info[0] == 2 else str(raw, 'utf-8')


def hexlify(script, minify=False):
    """
    Takes the byte content of a Python script and returns a hex encoded
    version of it.

    Based on the hexlify script in the microbit-micropython repository.
    """
    if not script:
        return ''
    # Convert line endings in case the file was created on Windows.
    script = script.replace(b'\r\n', b'\n')
    script = script.replace(b'\r', b'\n')
    if minify:
        if not can_minify:
            raise ValueError("No minifier is available")
        script = nudatus.mangle(script.decode('utf-8')).encode('utf-8')
    # Add header, pad to multiple of 16 bytes.
    data = b'MP' + struct.pack('<H', len(script)) + script
    # Padding with null bytes in a 2/3 compatible way
    data = data + (b'\x00' * (16 - len(data) % 16))
    if len(data) > _MAX_SIZE:
        # 'MP' = 2 bytes, script length is another 2 bytes.
        raise ValueError("Python script must be less than 8188 bytes.")
    # Convert to .hex format.
    output = [':020000040003F7']  # extended linear address, 0x0003.
    addr = _SCRIPT_ADDR
    for i in range(0, len(data), 16):
        chunk = data[i:min(i + 16, len(data))]
        chunk = struct.pack('>BHB', len(chunk), addr & 0xffff, 0) + chunk
        checksum = (-(sum(bytearray(chunk)))) & 0xff
        hexline = ':%s%02X' % (strfunc(binascii.hexlify(chunk)).upper(),
                               checksum)
        output.append(hexline)
        addr += 16
    return '\n'.join(output)


def unhexlify(blob):
    """
    Takes a hexlified script and turns it back into a string of Python code.
    """
    lines = blob.split('\n')[1:]
    output = []
    for line in lines:
        # Discard the address, length etc. and reverse the hexlification
        output.append(binascii.unhexlify(line[9:-2]))
    # Check the header is correct ("MP<size>")
    if (output[0][0:2].decode('utf-8') != u'MP'):
        return ''
    # Strip off header
    output[0] = output[0][4:]
    # and strip any null bytes from the end
    output[-1] = output[-1].strip(b'\x00')
    script = b''.join(output)
    try:
        result = script.decode('utf-8')
        return result
    except UnicodeDecodeError:
        # Return an empty string because in certain rare circumstances (where
        # the source hex doesn't include any embedded Python code) this
        # function may be passed in "raw" bytes from MicroPython.
        return ''


def embed_hex(runtime_hex, python_hex=None):
    """
    Given a string representing the MicroPython runtime hex, will embed a
    string representing a hex encoded Python script into it.

    Returns a string representation of the resulting combination.

    Will raise a ValueError if the runtime_hex is missing.

    If the python_hex is missing, it will return the unmodified runtime_hex.
    """
    if not runtime_hex:
        raise ValueError('MicroPython runtime hex required.')
    if not python_hex:
        return runtime_hex
    py_list = python_hex.split()
    runtime_list = runtime_hex.split()
    embedded_list = []
    # The embedded list should be the original runtime with the Python based
    # hex embedded two lines from the end.
    embedded_list.extend(runtime_list[:-5])
    embedded_list.extend(py_list)
    embedded_list.extend(runtime_list[-5:])
    return '\n'.join(embedded_list) + '\n'


def extract_script(embedded_hex):
    """
    Given a hex file containing the MicroPython runtime and an embedded Python
    script, will extract the original Python script.

    Returns a string containing the original embedded script.
    """
    hex_lines = embedded_hex.split('\n')
    script_addr_high = hex((_SCRIPT_ADDR >> 16) & 0xffff)[2:].upper().zfill(4)
    script_addr_low = hex(_SCRIPT_ADDR & 0xffff)[2:].upper().zfill(4)
    start_script = None
    within_range = False
    # Look for the script start address
    for loc, val in enumerate(hex_lines):
        if val[0:9] == ':02000004':
            # Reached an extended address record, check if within script range
            within_range = val[9:13].upper() == script_addr_high
        elif within_range and val[0:3] == ':10' and \
                val[3:7].upper() == script_addr_low:
            start_script = loc
            break
    if start_script:
        # Find the end of the script
        end_script = None
        for loc, val in enumerate(hex_lines[start_script:]):
            if val[9:41] == 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF':
                end_script = loc + start_script
                break
        # Pass the extracted hex through unhexlify
        return unhexlify('\n'.join(
            hex_lines[start_script - 1:end_script if end_script else -6]))
    return ''


def find_device(preferdisk=None, sizeCheck=None):
    """
    Returns a path on the filesystem that represents the plugged in BBC
    micro:bit that is to be flashed. If no micro:bit is found, it returns
    None.

    Works on Linux, OSX and Windows. Will raise a NotImplementedError
    exception if run on any other operating system.
    """
    # Check what sort of operating system we're on.
    if os.name == 'posix':
        # 'posix' means we're on Linux or OSX (Mac).
        # Call the unix "mount" command to list the mounted volumes.
        mount_output = check_output('mount').splitlines()
        mounted_volumes = [x.split()[2] for x in mount_output]
        
        for volume in mounted_volumes:
            if preferdisk:
                if type(preferdisk) is str:
                    preferdisk = preferdisk.encode('utf8')
                if volume.endswith(preferdisk):
                    return volume.decode('utf-8')
            else:
                if volume.endswith(b'MICROBIT'):
                    return volume.decode('utf-8')  # Return a string not bytes.
                elif volume.endswith(b'ARCADE-F4'):
                    return volume.decode('utf-8')  # Return a string not bytes.
                elif volume.endswith(b'NanoBit'):
                    return volume.decode('utf-8')  # Return a string not bytes.
    elif os.name == 'nt':
        # 'nt' means we're on Windows.

        def get_volume_name(disk_name):
            """
            Each disk or external device connected to windows has an attribute
            called "volume name". This function returns the volume name for
            the given disk/device.

            Code from http://stackoverflow.com/a/12056414
            """
            vol_name_buf = ctypes.create_unicode_buffer(1024)
            serial_number = None
            max_component_length = None
            file_system_flags = None
            ctypes.windll.kernel32.GetVolumeInformationW(
                ctypes.c_wchar_p(disk_name), vol_name_buf,
                ctypes.sizeof(vol_name_buf), serial_number, max_component_length, None, None, 0)
            return vol_name_buf.value

        #
        # In certain circumstances, volumes are allocated to USB
        # storage devices which cause a Windows popup to raise if their
        # volume contains no media. Wrapping the check in SetErrorMode
        # with SEM_FAILCRITICALERRORS (1) prevents this popup.
        #
        old_mode = ctypes.windll.kernel32.SetErrorMode(1)
        defaultPathList = ['MICROBIT', 'ARCADE-F4', 'NanoBit']
        try:
            for disk in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                path = '{}:\\'.format(disk)
                #
                # Don't bother looking if the drive isn't removable
                #
                if ctypes.windll.kernel32.GetDriveTypeW(path) != 2:
                    continue
                if os.path.exists(path):
                    pathName = get_volume_name(path)
                    if pathName in defaultPathList:
                        return path
                    elif sizeCheck != None:
                        if type(sizeCheck) == str:
                            sizeCheck = eval(sizeCheck.replace('M', '*1024*1024'))
                        total, used, free = shutil.disk_usage(path)
                        if abs(total - sizeCheck) < 0x20000:
                            return path
                    elif preferdisk != None:
                        if preferdisk == pathName:
                            return path
        finally:
            ctypes.windll.kernel32.SetErrorMode(old_mode)
    else:
        # No support for unknown operating systems.
        raise NotImplementedError('OS "{}" not supported.'.format(os.name))


def save_hex(hex_file, path):
    """
    Given a string representation of a hex file, this function copies it to
    the specified path thus causing the device mounted at that point to be
    flashed.

    If the hex_file is empty it will raise a ValueError.

    If the filename at the end of the path does not end in '.hex' it will raise
    a ValueError.
    """
    if not hex_file:
        return (-1, 'Cannot flash an empty .hex file.')
    if not path.endswith('.hex'):
        return (-1, 'The path to flash must be for a .hex file.')
    with open(path, 'wb') as output:
        output.write(hex_file.encode('ascii'))
        return (0, path)


def flash(path_to_python=None, paths_to_microbits=None,
          path_to_runtime=None, python_script=None, minify=False, echo=None):
    """
    Given a path to or source of a Python file will attempt to create a hex
    file and then flash it onto the referenced BBC micro:bit.

    If the path_to_python & python_script are unspecified it will simply flash
    the unmodified MicroPython runtime onto the device.

    If used, the python_script argument should be a bytes object representing
    a UTF-8 encoded string. For example::

        script = "from microbit import *\\ndisplay.scroll('Hello, World!')"
        uflash.flash(python_script=script.encode('utf-8'))

    If paths_to_microbits is unspecified it will attempt to find the device's
    path on the filesystem automatically.

    If the path_to_runtime is unspecified it will use the built in version of
    the MicroPython runtime. This feature is useful if a custom build of
    MicroPython is available.

    If the automatic discovery fails, then it will raise an IOError.
    """
    # Check for the correct version of Python.
    if not ((sys.version_info[0] == 3 and sys.version_info[1] >= 3) or
            (sys.version_info[0] == 2 and sys.version_info[1] >= 7)):
        raise RuntimeError('Will only run on Python 2.7, or 3.3 and later.')
    # Grab the Python script (if needed).
    python_hex = ''
    if path_to_python:
        if not path_to_python.endswith('.py'):
            return (-4, 'Python files must end in ".py".')
        with open(path_to_python, 'rb') as python_script:
            python_hex = hexlify(python_script.read(), minify)
    elif python_script:
        python_hex = hexlify(python_script, minify)

    # runtime = _RUNTIME
    # Load the hex for the runtime.
    if path_to_runtime:
        with open(path_to_runtime) as runtime_file:
            runtime = runtime_file.read()
    # Generate the resulting hex file.
    micropython_hex = embed_hex(runtime, python_hex)
    # Find the micro:bit.
    if not paths_to_microbits:
        found_microbit = find_device()
        if found_microbit:
            paths_to_microbits = [found_microbit]
    # Attempt to write the hex file to the micro:bit.
    if paths_to_microbits:
        for path in paths_to_microbits:
            hex_path = os.path.join(path, 'micropython.hex')
            print('Flashing Python to: {}'.format(hex_path))
            if echo:
                echo('Flashing Python to: {}'.format(hex_path))
            return save_hex(micropython_hex, hex_path)
    else:
        return (-2, 'Unable to find micro:bit. Is it plugged in?')

def copyfileobj(fsrc, fdst, callback, total, length=4*1024):
    copied = 0
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        copied += len(buf)
        callback(copied, total)
        # this is for mac, cache ENXIO in runtime
        fdst.flush()
        os.fsync(fdst)

def copyHex(path_to_hex, callback):
    # todo: support uf2 borads other than microbits
    
    paths_to_microbits = None
    
    found_microbit = find_device()
    if found_microbit:
        paths_to_microbits = [found_microbit]
        if paths_to_microbits:
            for path in paths_to_microbits:
                hex_path = os.path.join(path, 'micropython.hex')
                # print('Flashing Firmware to: {}'.format(path))
                # shutil.copyfile(path_to_hex, hex_path)
                if type(path_to_hex) == bytes:
                    fsrc = BytesIO(path_to_hex)
                    size = len(path_to_hex)
                elif path_to_hex.startswith("data:"):
                    if path_to_hex.startswith("data:application"):
                        b64 = re.sub('^data:application/.+;base64,', '', path_to_hex)
                    else:
                        b64 = re.sub('^data:text/.+;base64,', '', path_to_hex)
                    b64Data = base64.b64decode(b64)
                    fsrc = BytesIO(b64Data)
                    size = len(b64Data)
                else:
                    fsrc = open(path_to_hex, 'rb')
                    size = os.stat(path_to_hex).st_size
                with open(hex_path, 'wb') as fdst:
                    copyfileobj(fsrc, fdst, callback, size)
            return (0, paths_to_microbits[0])
        else:
            return (-1, 'Unable to find target')
    else:
        return (-1, 'Unable to find target')

def getDisk(disk_filter, size=None):
    found_microbit = find_device(disk_filter, size)
    return found_microbit

def extract(path_to_hex, output_path=None):
    """
    Given a path_to_hex file this function will attempt to extract the
    embedded script from it and save it either to output_path or stdout
    """
    with open(path_to_hex, 'r') as hex_file:
        python_script = extract_script(hex_file.read())
        if output_path:
            with open(output_path, 'w') as output_file:
                output_file.write(python_script)
        else:
            print(python_script)


def watch_file(path, func, *args, **kwargs):
    """
    Watch a file for changes by polling its last modification time. Call the
    provided function with *args and **kwargs upon modification.
    """
    if not path:
        raise ValueError('Please specify a file to watch')
    print('Watching "{}" for changes'.format(path))
    last_modification_time = os.path.getmtime(path)
    try:
        while True:
            time.sleep(1)
            new_modification_time = os.path.getmtime(path)
            if new_modification_time == last_modification_time:
                continue
            func(*args, **kwargs)
            last_modification_time = new_modification_time
    except KeyboardInterrupt:
        pass


# def main(argv=None):
#     """
#     Entry point for the command line tool 'uflash'.

#     Will print help text if the optional first argument is "help". Otherwise
#     it will ensure the optional first argument ends in ".py" (the source
#     Python script).

#     An optional second argument is used to reference the path to the micro:bit
#     device. Any more arguments are ignored.

#     Exceptions are caught and printed for the user.
#     """
#     if not argv:
#         argv = sys.argv[1:]

#     parser = argparse.ArgumentParser(description=_HELP_TEXT)
#     parser.add_argument('source', nargs='?', default=None)
#     parser.add_argument('target', nargs='*', default=None)
#     parser.add_argument('-r', '--runtime', default=None,
#                         help="Use the referenced MicroPython runtime.")
#     parser.add_argument('-e', '--extract',
#                         action='store_true',
#                         help=("Extract python source from a hex file"
#                               " instead of creating the hex file."), )
#     parser.add_argument('-w', '--watch',
#                         action='store_true',
#                         help='Watch the source file for changes.')
#     parser.add_argument('-m', '--minify',
#                         action='store_true',
#                         help='Minify the source')
#     parser.add_argument('--version', action='version',
#                         version='%(prog)s ' + get_version())
#     parser.add_argument('-u', '--uf2',
#                         action='store_true',
#                         help='UF2 like hex copy.')
#     parser.add_argument('-d', '--disk',
#                         action='store_true',
#                         help='Get Disk.')                    
#     args = parser.parse_args(argv)

#     if args.extract:
#         try:
#             extract(args.source, args.target)
#         except Exception as ex:
#             error_message = "Error extracting {source}: {error!s}"
#             print(error_message.format(source=args.source, error=ex),
#                   file=sys.stderr)
#             sys.exit(1)

#     elif args.watch:
#         try:
#             watch_file(args.source, flash,
#                        path_to_python=args.source,
#                        paths_to_microbits=args.target,
#                        path_to_runtime=args.runtime)
#         except Exception as ex:
#             error_message = "Error watching {source}: {error!s}"
#             print(error_message.format(source=args.source, error=ex),
#                   file=sys.stderr)
#             sys.exit(1)
#     elif args.uf2:
#         copyHex(args.source)
#     elif args.disk:
#         getDisk(args.source)
#     else:
#         try:
#             flash(path_to_python=args.source, paths_to_microbits=args.target,
#                   path_to_runtime=args.runtime, minify=args.minify)
#         except Exception as ex:
#             error_message = (
#                 "Error flashing {source} to {target}{runtime}: {error!s}"
#             )
#             source = args.source
#             target = args.target if args.target else "microbit"
#             if args.runtime:
#                 runtime = "with runtime {runtime}".format(runtime=args.runtime)
#             else:
#                 runtime = ""
#             print(error_message.format(source=source, target=target,
#                                        runtime=runtime, error=ex),
#                   file=sys.stderr)
#             sys.exit(1)
