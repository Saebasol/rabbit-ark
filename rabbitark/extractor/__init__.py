import os
import re
import traceback

directory = os.path.dirname(os.path.realpath(__file__))


def load():
    failed = []

    for extension in [
        re.sub(".py", "", file) for file in os.listdir(directory) if not "__" in file
    ]:
        try:
            __import__("rabbitark.extractor." + extension)
        except:
            traceback.print_exc()
            failed.append(extension)

    return failed
