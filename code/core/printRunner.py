from .runner import Runner

class PrintRunner(Runner):
    def run(self, inp):
        """Print the given input"""
        print(inp)
        return (inp, Runner.UNRESOLVED)