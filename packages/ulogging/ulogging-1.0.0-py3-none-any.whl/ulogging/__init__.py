# imports-------------------------------
from typing import Callable, Any, TextIO
import datetime
# --------------------------------------

class LogState: # class with log state

    name: str = "" # name of state
    message: str = "" # message of state

    def __init__(self, name: str, message: str) -> None:
        self.name = name
        self.message = message

class LogStates: # class with log states

    all_ok: LogState = LogState("ALL OK", "NO ERRORS") # when all ok
    low_importance_error: LogState = LogState("ERROR (LOW IMPORTANCE)", "ERROR: {error}") # low importance error
    high_importance_error: LogState = LogState("ERROR (!!!HIGH IMPORTANCE!!!)", "ERROR: {error}") # high importance error

class Logger: # main class

    step: int # log step
    file: TextIO = None # output file
    rec_format: str = "{step}. {time} [{state}] <{unit_name}>({args}){{{returned}}} ~{message}~" # record format for log_it
    err_rec_format: str = "{step}. {time} [{state}] <{unit_name}>({args}) ~{message}~" # error record format log_it
    here_rec_format: str = "{step}. {time} <{log_id}>" # record format for log_here
    time_format: str = "%Y-%m-%d %H:%M:%S:%f" # time format
    no_print = False # no print

    def __init__(self, file_name: str, 
                 rec_format: str = "{step}. {time} [{state}] <{unit_name}>({args}){{{returned}}} ~{message}~", 
                 err_rec_format: str = "{step}. {time} [{state}] <{unit_name}>({args}) ~{message}~", 
                 here_rec_format: str = "{step}. {time} <{log_id}>",
                 time_format: str = "%Y-%m-%d %H:%M:%S", 
                 no_print: bool = False) -> None:
        self.step = 0
        self.file = open(file_name, 'a')
        self.rec_format = rec_format
        self.err_rec_format = err_rec_format
        self.here_rec_format = here_rec_format
        self.time_format = time_format
        self.no_print = no_print
        self.file.write("*" * 100 + '\n')
        print("*" * 100)
        self.file.write(f"WORKING STARTED: {datetime.datetime.today().strftime(self.time_format)}"+ '\n')
        print(f"WORKING STARTED: {datetime.datetime.today().strftime(self.time_format)}")

    def log_it_low_importance(self, callback: Callable[..., Any]) -> Any:
        def logger(*args, **kwargs):
            self.step += 1
            try:
                returned = callback(*args, **kwargs)
                self.file.write(self.rec_format.format(
                    step = self.step,
                    time = datetime.datetime.today().strftime(self.time_format),
                    state = LogStates.all_ok.name,
                    unit_name = callback.__name__,
                    args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                    returned = returned,
                    message = LogStates.all_ok.message
                ) + '\n')
                if not self.no_print:
                    print(self.rec_format.format(
                        step = self.step,
                        time = datetime.datetime.today().strftime(self.time_format),
                        state = LogStates.all_ok.name,
                        unit_name = callback.__name__,
                        args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                        returned = returned,
                        message = LogStates.all_ok.message
                    ))
                return returned
            except Exception as err:
                self.file.write(self.err_rec_format.format(
                    step = self.step,
                    time = datetime.datetime.today().strftime(self.time_format),
                    state = LogStates.low_importance_error.name,
                    unit_name = callback.__name__,
                    args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                    message = LogStates.low_importance_error.message.format(error=err)
                ) + '\n')
                if not self.no_print:
                    print(self.err_rec_format.format(
                        step = self.step,
                        time = datetime.datetime.today().strftime(self.time_format),
                        state = LogStates.low_importance_error.name,
                        unit_name = callback.__name__,
                        args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                        message = LogStates.low_importance_error.message.format(error=err)
                    ))
                return None
        return logger

    def log_it_high_importance(self, callback: Callable[..., Any]) -> Any:
        def logger(*args, **kwargs):
            self.step += 1
            try:
                returned = callback(*args, **kwargs)
                self.file.write(self.rec_format.format(
                    step = self.step,
                    time = datetime.datetime.today().strftime(self.time_format),
                    state = LogStates.all_ok.name,
                    unit_name = callback.__name__,
                    args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                    returned = returned,
                    message = LogStates.all_ok.message
                ) + '\n')
                if not self.no_print:
                    print(self.rec_format.format(
                        step = self.step,
                        time = datetime.datetime.today().strftime(self.time_format),
                        state = LogStates.all_ok.name,
                        unit_name = callback.__name__,
                        args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                        returned = returned,
                        message = LogStates.all_ok.message
                    ))
                return returned
            except Exception as err:
                self.file.write(self.err_rec_format.format(
                    step = self.step,
                    time = datetime.datetime.today().strftime(self.time_format),
                    state = LogStates.high_importance_error.name,
                    unit_name = callback.__name__,
                    args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                    message = LogStates.high_importance_error.message.format(error=err)
                ) + '\n')
                if not self.no_print:
                    print(self.err_rec_format.format(
                        step = self.step,
                        time = datetime.datetime.today().strftime(self.time_format),
                        state = LogStates.high_importance_error.name,
                        unit_name = callback.__name__,
                        args = (str(*args) if len(args) > 0 else "") + (", " if len(args) > 0 and len(kwargs) > 0 else "") + (str(**kwargs) if len(kwargs) > 0 else ""),
                        message = LogStates.high_importance_error.message.format(error=err)
                    ))
                return None
        return logger

    def log_here(self, log_id: str) -> None:
        self.step += 1
        self.file.write(self.here_rec_format.format(
            step = self.step,
            time = datetime.datetime.today().strftime(self.time_format),
            log_id = log_id
        ) + '\n')
        if not self.no_print:
            print(self.here_rec_format.format(
                step = self.step,
                time = datetime.datetime.today().strftime(self.time_format),
                log_id = log_id
            ))