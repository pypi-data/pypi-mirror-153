# coding=utf-8
#
# timer.py in pisnp/utility
#
# created by 谢方圆 (XIE Fangyuan) on 2022-06-05
# Copyright © 2022 谢方圆 (XIE Fangyuan). All rights reserved.
#
# Timer.


from datetime import timedelta
from functools import wraps
from time import time
from typing import Any, Callable

from sty import fg


class Timer:
    @staticmethod
    def time(function: Callable) -> Callable:
        """decorator to time the running process of a function.

        :param function: A function to be timed.
        :return: A decorated timed function.
        """

        @wraps(function)
        def tictoc(*args, **kwargs) -> Any:
            start_time = time()
            returned = function(*args, **kwargs)
            end_time = time()

            print(f'''Took {fg.yellow}{timedelta(
                seconds=end_time - start_time
            )}{fg.rs} to run.''')

            return returned

        return tictoc
