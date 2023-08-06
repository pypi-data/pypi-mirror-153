from subprocess import PIPE, Popen
from .GeneralUtilities import GeneralUtilities
from .ProgramRunnerBase import ProgramRunnerBase


class ProgramRunnerPopen(ProgramRunnerBase):

    @GeneralUtilities.check_arguments
    def run_program_argsasarray_async_helper(self,program:str, arguments_as_array: list[str]=[], working_directory: str=None,custom_argument:object=None) -> Popen:
        arguments_for_process = [program]
        arguments_for_process.extend(arguments_as_array)
        return Popen(arguments_for_process, stdout=PIPE, stderr=PIPE, cwd=working_directory, shell=True)

    # Return-values program_runner: Exitcode, StdOut, StdErr, Pid
    @GeneralUtilities.check_arguments
    def wait(self, process:Popen ,custom_argument:object) -> tuple[int, str, str, int]:
        pid = process.pid
        stdout, stderr = process.communicate()
        exit_code = process.wait()
        stdout = GeneralUtilities.bytes_to_string(stdout).replace('\r', '')
        stderr = GeneralUtilities.bytes_to_string(stderr).replace('\r', '')
        result = (exit_code, stdout, stderr, pid)
        return result

    @GeneralUtilities.check_arguments
    def run_program_argsasarray(self,program:str, arguments_as_array: list[str]=[], working_directory: str=None,custom_argument:object=None) -> tuple[int, str, str, int]:
        process:Popen=self.run_program_argsasarray_async_helper(program,arguments_as_array,working_directory,custom_argument)
        return self.wait(process, custom_argument)

    @GeneralUtilities.check_arguments
    def run_program(self, program:str,arguments: str="", working_directory: str=None,custom_argument:object=None) -> tuple[int, str, str, int]:
        return self.run_program_argsasarray(program,GeneralUtilities.arguments_to_array(arguments),working_directory,custom_argument)

    @GeneralUtilities.check_arguments
    def run_program_argsasarray_async(self,program:str, arguments_as_array: list[str]=[], working_directory: str=None,custom_argument:object=None) -> int:
        return self.run_program_argsasarray_async_helper(program,arguments_as_array,working_directory,custom_argument).pid

    @GeneralUtilities.check_arguments
    def run_program_async(self, program:str,arguments: str="", working_directory: str=None,custom_argument:object=None) ->int:
        return self.run_program_argsasarray_async(program,GeneralUtilities.arguments_to_array(arguments),working_directory,custom_argument)
