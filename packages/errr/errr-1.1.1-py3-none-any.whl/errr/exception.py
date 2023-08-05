def _details_iter(labels, extras, values):
    labels, extras, values = iter(labels), iter(extras), iter(values)
    i = 1
    yielded_extras = False
    # Skip the first value, which is the error message itself.
    next(values, None)
    while True:
        label = next(labels, None)
        if not label and not yielded_extras:
            for y in extras:
                yield y
                i += 1
            yielded_extras = True
        try:
            value = next(values)
            actual_values = True
        except StopIteration:
            value = None
            actual_values = False
        if label:
            yield (label, value)
        elif actual_values:
            yield (i, value)
        else:
            break
        i += 1

def _match_iter(msg, start=None):
    start = msg.find("%", start) + 1
    while True:
        end = msg.find("%", start)
        match = msg[start:end]
        yield match, start, end
        start = end + 1

class DetailedErrorMetaclass(type):
    def __repr__(self):
        return "<class '{}'>".format(self.__module__ + "." + self.__name__)

class DetailedException(Exception, metaclass=DetailedErrorMetaclass):
    """
    Base Exception class
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        details = dict(_details_iter(self.get_detail_labels(), kwargs.items(), args))
        self.__dict__["details"] = details
        self.__dict__["msg"] = args[0] if len(args) > 0 else None

    def get_detail_labels(self):
        try:
            return super().get_detail_labels() + self.__class__._detail_labels
        except AttributeError:
            return self.__class__._detail_labels

    def __getattr__(self, attr):
        if attr in self.__class__._detail_labels:
            return self.details[attr]
        return self.__getattribute__(attr)

    def __setattr__(self, attr, value):
        if attr in self.details:
            self.details[attr] = value
            return
        super().__setattr__(attr, value)

    def __str__(self):
        msg = self._get_msg()
        details = self._get_details_msg()
        if details:
            msg += "\n\nDetails:\n" + details
        return msg

    def _get_msg(self):
        return self.interpolate(str(self.args[0] if len(self.args) > 0 else ""))

    def interpolate(self, msg, start=None):
        # Create an iterator that returns each portion of the string between 2 % %
        # E.g.: "Hi I %am% Robin%." would yield "am" and " Robin" in an infinite loop.
        matches = _match_iter(msg, start)
        match, start, end = next(matches)
        # Keep looking for a match until the last % has been found (the loop exits early
        # after the first replacement has been made, returning the result of a recursive
        # interpolation call continuing the interpolation where this loop stopped.
        while end != -1:
            # Split on '.' to see if there's any indices or attributes we should lookup in
            # the detail.
            parts = iter(match.split("."))
            detail = next(parts)
            # Use the detail and parts to lookup the replacement string.
            try:
                replacement = self.details[detail]
                # Loop over what's left in the iterator after taking out the detail.
                for part in parts:
                    # Try to use the part as attribute, if that doesn't work, try to use
                    # it as index and if that doesn't work, this is not a match and we
                    # should continue looking
                    try:
                        replacement = getattr(replacement, part)
                    except AttributeError:
                        replacement = replacement[part]
                # Turn the lookup result into a string and replace the match with it.
                replacement = str(replacement)
                replaced = msg[:(start - 1)] + replacement + msg[(end + 1):]
                # Interpolate the rest of the string recursively
                return self.interpolate(replaced, start - 1 + len(replacement))
            except (KeyError, IndexError, TypeError):
                pass
            # Match was not a valid replacement string, continue looking.
            match, start, end = next(matches)
        # Nothing to replace found at all, return original message
        return msg

    @classmethod
    def wrap(err_type, e, *details, prepend=None, append=None):
        interpolator = err_type("", *details)
        msg = ""
        if hasattr(interpolator, "interpolate"):
            if prepend is not None:
                msg = interpolator.interpolate(prepend)
            msg += str(e)
            if append is not None:
                msg += interpolator.interpolate(append)
        else:
            if prepend is not None:
                msg = prepend
            msg += str(e)
            if append is not None:
                msg += append
        err = err_type(msg, *details)
        err.__traceback__ = e.__traceback__
        raise err from None

    def _get_details_msg(self):
        pass

    def _details_concat(self):
        return "\n".join(map(_err_line, self.details.items()))

    def __init_subclass__(cls, list_details=False, details=[], **kwargs):
        super().__init_subclass__(**kwargs)
        if list_details:
            cls._get_details_msg = cls._details_concat
        cls._detail_labels = details

def _err_line(kv):
    return " {} {}: {}".format(chr(746), kv[0], kv[1])
