#!/usr/bin/env python
# coding: utf-8

import logging


class SoftAssert():
    """Accumulate exceptions for later report

    Args:
        *exceptions: exception class (or iterable of exceptoin classes)
            to capture in further calls.

    Returns:
        callable (see __call__ for details). Also can be used as context.

    Attributes:
        message (str): aggregate report message prefix
        final_exception: exception to raise on final report (self.raise_errors)
    """
    message = "Errors collected"
    final_exception = AssertionError

    def __init__(self, *exceptions):
        self.errors = []
        self.track_exceptions = exceptions or AssertionError

    def __call__(self, func, *args, **kwargs):
        """Wrapper to run func inside a try block and collect exceptions

        Args:
            func (callable): callable to run
            *args, **kwargs: directly passed to func

        Returns:
            Same as func does
        """
        assert callable(func), "The first argument should be a callable"

        try:
            return func(*args, **kwargs)
        except self.track_exceptions as exc:
            logging.exception("Error happened, collecting")
            self.errors.append(exc)

    def __enter__(self):
        return self

    def __exit__(self):
        return self.raise_errors()

    def raise_errors(self, msg=None):
        """Raise exception if any errors were previously collected

        Args:
            msg (str): some alternative message to prefix error list output

        Raises:
            AssertionError by default, can be redefined in self.final_exception
        """
        if self.errors:
            raise self.final_exception(
                "{} (see logs above for tracebacks):\n{}".format(
                    self.message if msg is None else msg,
                    "\n".join(str(e) for e in self.errors)))
