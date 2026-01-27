import traceback
with open("error_log_asyncpg.txt", "w") as f:
    f.write("Start\n")
    try:
        import asyncpg
        f.write("asyncpg ok\n")
    except:
        traceback.print_exc(file=f)
