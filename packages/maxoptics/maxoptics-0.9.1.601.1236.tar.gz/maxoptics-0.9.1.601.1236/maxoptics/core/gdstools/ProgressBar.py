class ProgressBar:
    def __init__(
        self,
        iteration,
        total,
        prefix="loading:",
        suffix="Complete",
        decimals=1,
        length=100,
        fill="█",
        printEnd="\r",
    ):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """

        self.iteration = iteration
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd

    def walk(self, step=1):
        self.iteration += step
        percent = ("{0:." + str(self.decimals) + "f}").format(
            100 * (self.iteration / float(self.total))
        )
        filledLength = int(self.length * self.iteration // self.total)
        bar = self.fill * filledLength + "-" * (self.length - filledLength)

        # show percent progress
        # print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)

        # show iteration progress
        print(
            f"\r{self.prefix} |{bar}| {self.iteration}/{self.total} {self.suffix}",
            end=self.printEnd,
        )

        # Print New Line on Complete
        if self.iteration >= self.total:
            print("\r{}".format(" " * (self.length + 50)), end=self.printEnd)
            print()
