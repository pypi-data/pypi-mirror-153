"""
vmd.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import molecular.external

import os
import socket
import subprocess
import tempfile


# The class VMD starts up an instance of VMD that Python can connect
# with. We can send commands, send structures, and close VMD.
class VMD:
    """
    The class VMD starts up an instance of VMD that Python can connect with.
    You can send commands, send structures, and close VMD.
    """

    def __init__(self, source=None, port=45000,
                 executable='C:\\Program Files (x86)\\University of Illinois\\VMD\\vmd.exe'):
        """

        Parameters
        ----------
        port : int
        executable : str
        """

        self.port = int(port)
        self.executable = str(executable)

        self._process = None
        self._socket = None
        self.connected = False

        # if source is not None:
        #     self.source(source)
        # else:
        #     self.connect()

    # Close VMD and the socket
    def close(self):
        # Mark as no longer connected
        self.connected = False

        # If the VMD process is no longer available, return error
        if self._process.poll() is not None:
            raise RuntimeError('VMD already terminated')

        # Exit VMD
        self._socket.sendall(b'exit\n')

    # Connect to VMD
    def connect(self):
        # Launch VMD
        vmd_server_script = os.path.join(molecular.external.__path__[0], 'vmd_server.tcl')
        with tempfile.TemporaryFile() as file:
            self._process = subprocess.Popen([
                self.executable,
                '-e',
                vmd_server_script,
                '-args',
                str(self.port)
            ], stdout=subprocess.PIPE, stdin=file, stderr=subprocess.PIPE)

        # Set up the socket
        self._socket = socket.socket()

        # Wait for VMD to load and then connect
        # There is probably a circumstance where this results in an
        # infinite loop --> should there be a timeout?
        while not self.connected:
            try:
                self._socket.connect(('localhost', self.port))
                self.connected = True
            except ConnectionRefusedError:
                pass

        # Mark as connected
        self.connected = True

    # Load a structure into VMD
    def load(self, structure):
        # Create temporary file
        file = tempfile.NamedTemporaryFile(delete=False)
        file.close()

        # Get temporary file name
        filename = file.name.replace('\\', '/')

        # Write out structure (just PDB for now; eventually PSF/DCD?)
        structure.to_pdb(filename)

        # Execute load command on VMD
        self.execute('mol new ' + filename + ' waitfor all')

        # Delete temporary file
        os.remove(filename)

    # Execute command
    def execute(self, command):
        # If the socket isn't open, don't do anything
        if not self.connected:
            raise RuntimeError('connection already terminated')

        # If the VMD process is no longer available, return error
        if self._process.poll() is not None:
            raise RuntimeError('VMD already terminated')

        # Execute the command
        command = str(command) + '\n'  # Need newline
        command = command.replace('$', '$::')  # Need to use global namespace
        command = command.replace('[', '[uplevel #0 ')  # For global namespace
        self._socket.sendall(command.encode())

        # Receive results (should buffer be user-specified?)
        result = self._socket.recv(4096).decode('ascii').strip()

        # Split retcode from rest of results
        return_code = int(result[0])
        result = result[1:]

        # Raise error
        if return_code:
            print(command)
            print(result)
            raise RuntimeError('VMD command error')

        # Return
        if len(result) != 0:
            return result

    def source(self, filename, verbose=False):
        """
        Source from file on disk.

        Parameters
        ----------
        filename : str
            Path to file on disk
        verbose : bool
        """

        process = subprocess.Popen([self.executable, '-e', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if verbose:
            stdout, stderr = process.communicate()
            print(stdout.decode('ascii'))
            print(stderr.decode('ascii'))


def run_vmd_source(filename, verbose=False):
    VMD().source(filename, verbose=verbose)
