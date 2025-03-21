import shutil

def check(dependency):
  if shutil.which(dependency):
      print(f"{dependency} is installed.")
      return True
  else:
      raise Exception(f"{dependency} is not installed.")