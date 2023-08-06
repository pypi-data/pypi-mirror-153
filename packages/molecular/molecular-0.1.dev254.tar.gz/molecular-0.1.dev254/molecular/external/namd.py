"""
namd.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import os
import subprocess


# Class to run NAMD simulations
# TODO use glovebox to store all NAMD PIDs
class NAMD:
    """
    NAMD class, which launches simulations. Eventually this will do more error
    checking; however, for today it's bare minimum. This will break if there
    are duplicate parameters in the config file.

    >>> from molecular import namd
    >>> md = namd()
    >>> md.start()

    See Also
    --------
    https://github.com/radakb/pynamd
    """

    # Initialize class instance
    def __init__(self, config_file, executable='namd2', n_jobs=None, background=False):
        """
        Initialize NAMD run.

        Parameters
        ----------
        config_file : str
            Path to NAMD configuration file.
        executable : str
            Location of NAMD executable. (Default: `namd2` in current working directory).
        n_jobs : int
            Number of jobs.
        background : bool
            Flag to indicate if NAMD task should be executed in the background.
        """

        # Properties
        self.config_file = str(config_file)
        self.executable = str(executable)
        self.n_jobs = int(n_jobs) if n_jobs is not None else None
        self.background = bool(background)

        # Runtime functions
        self._process = None

    # Check if running
    def _check_if_running(self):
        # If the job is already running, we cannot start again
        if not self.poll():
            raise RuntimeError('NAMD already running')

    # Copy NAMD configuration
    def copy(self):
        """
        Copy NAMD configuration.

        Returns
        -------
        molecular.external.namd
            New instance of NAMD class
        """

        return NAMD(
            config_file=self.config_file,
            executable=self.executable,
            n_jobs=self.n_jobs,
            background=self.background
        )

    # PID
    @property
    def pid(self):
        """
        Return process ID.

        Returns
        -------
        int
            Process ID on system.
        """

        if self._process is None:
            result = None
        else:
            result = self._process.pid

        return result

    # Poll
    def poll(self):
        """
        Check if simulations are still running.

        Returns
        -------
        None or int
            None if simulations are running, return code if simulations are finished.
        """

        if self._process is None:
            result = None
        else:
            result = self._process.poll()

        return result

    # Start simulations
    def start(self, output_file=None):
        """
        Start NAMD simulations.

        Parameters
        ----------
        output_file : str
            Path to output file to write. If not specified, uses name of configuration file with extension '.out'.
        """

        # Check if NAMD is already running
        if self.poll():
            raise RuntimeError('NAMD already running')

        # Set an output file
        if output_file is None:
            output_file = os.path.splitext(self.config_file)[0] + '.out'

        # Set up command
        command = [self.executable]
        if self.n_jobs is not None:
            command += ['+p' + str(self.n_jobs)]
        command += [self.config_file]

        # Open output file and run
        with open(output_file, 'w') as buffer:
            self._process = subprocess.Popen(command, stdout=buffer)

        # Should we wait?
        if not self.background:
            self._process.wait()
            if self._process.poll() != 0:
                raise RuntimeError('NAMD job did not finish successfully')

    # Stop simulations
    def stop(self):
        # Check if NAMD is already running
        if self.poll():
            self._process.kill()

        # Otherwise, alert that NAMD is not running
        # TODO should this be warning?
        else:
            pass


# TODO https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6
class NAMDConfiguration:
    def __init__(self, config_file=None):
        self.parameters = {}
        if config_file is not None:
            self.read(config_file)

    def __repr__(self):
        return str(self.parameters)

    def add(self, parameter, *args):
        args = list(args)
        # if len(args) > 1:
        #     args = [args]
        args = [args]
        self.parameters[parameter] = self.parameters.get(parameter, []) + args

    def read(self, config_file):
        with open(config_file, 'r') as buffer:
            lines = buffer.readlines()
            for line in lines:
                # Parse up to comment
                if '#' in line:
                    line = line[:line.find('#')]

                # Strip line
                line = line.strip()

                # If line is not empty,
                if len(line) != 0:
                    # Add
                    self.add(*line.split())

    def write(self, config_file):
        pass



    # def read_config(self, filename):
    #     with open(filename, 'r') as buffer:
    #         self.parameters = buffer.read()
    #
    # def read_output(self):
    #     return read_NAMD_output(self.name+'.out')
    #
    # def write_config(self):
    #     with open(self.name + '.namd', 'w') as buffer:
    #         buffer.write(self.parameters)
#
#
# # Function for reading NAMD output
# def read_NAMD_output(fname,ignore_first=False):
#     file=open(str(fname),'r')
#     lines=file.read().split('\n')
#     file.close()
#     keys=None
#     values=[]
#     for line in lines:
#         if line[:6] == 'ETITLE':
#             keys_=line.split()[1:]
#             if keys is None: keys=keys_
#             if keys != keys_:
#                 raise ValueError('keys change')
#         elif line[:6] == 'ENERGY':
#             values_=line.split()[1:]
#             values.append(values_)
#     if ignore_first: values=values[1:]
#     values=np.array(values,dtype=float)
#     df=pd.DataFrame()
#     for i,key in enumerate(keys):
#         df[key]=pd.Series(values[:,i])
#     return df
