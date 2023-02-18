from cx_Freeze import setup, Executable


setup(
    name = "Update yuzu EA",
    version = "0.1",
    executables = [Executable("pyUpEA.py")],
   )
