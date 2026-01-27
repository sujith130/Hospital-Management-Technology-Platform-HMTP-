import traceback
import sys

with open("error_log_main.txt", "w") as f:
    f.write("Starting import...\n")
    f.flush()
    try:
        import app.main
        f.write("app.main imported successfully\n")
    except:
        f.write("Error encountered:\n")
        traceback.print_exc(file=f)
    f.flush()
