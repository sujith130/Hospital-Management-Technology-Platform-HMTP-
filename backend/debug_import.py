import traceback
import sys

with open("error_log.txt", "w") as f:
    try:
        import pydantic_settings
        f.write("pydantic_settings imported successfully\n")
    except:
        f.write("Error encountered:\n")
        traceback.print_exc(file=f)
