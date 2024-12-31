import argparse


class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        options = ", ".join(action.option_strings)
        if action.nargs == 0:
            return options
        return f"{options} {self._format_args(action, action.dest.upper())}"
