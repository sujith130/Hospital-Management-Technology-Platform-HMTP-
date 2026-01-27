import traceback
import sys

with open("error_log_v1.txt", "w") as f:
    try:
        import pydantic
        f.write(f"pydantic imported successfully: {pydantic.VERSION}\n")
    except:
        f.write("Error encountered:\n")
        traceback.print_exc(file=f)
