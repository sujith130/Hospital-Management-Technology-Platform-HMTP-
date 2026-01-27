import traceback
import sys

with open("error_log_fastapi.txt", "w") as f:
    try:
        import fastapi
        f.write(f"fastapi imported successfully: {fastapi.__version__}\n")
    except:
        f.write("Error encountered:\n")
        traceback.print_exc(file=f)
