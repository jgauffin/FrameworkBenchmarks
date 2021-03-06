
import subprocess
import sys
import setup_util
import os

def start(args, logfile, errfile):
  setup_util.replace_text("nodejs/hello.js", "mongodb:\/\/.*\/hello_world", "mongodb://" + args.database_host + "/hello_world")
  setup_util.replace_text("nodejs/hello.js", "localhost", args.database_host)

  try:
    npm(logfile, errfile)
    subprocess.Popen("node hello.js", shell=True, cwd="nodejs", stderr=errfile, stdout=logfile)
    return 0
  except subprocess.CalledProcessError:
    return 1

def npm(logfile, errfile):
  if os.name == 'nt':
    subprocess.check_call("copy package.json package.json.dist /y > NUL", shell=True, cwd="nodejs", stderr=errfile, stdout=logfile)
    setup_util.replace_text("nodejs/package.json", ".*mysql.*", "")
    setup_util.replace_text("nodejs/package.json", ".*mapper.*", "")
  
  try:
    subprocess.check_call("npm install", shell=True, cwd="nodejs", stderr=errfile, stdout=logfile)
  finally:
    if os.name == 'nt':
      subprocess.check_call("del package.json", shell=True, cwd="nodejs")
      subprocess.check_call("ren package.json.dist package.json", shell=True, cwd="nodejs", stderr=errfile, stdout=logfile)

def stop(logfile, errfile):
  if os.name == 'nt':
    subprocess.Popen("taskkill /f /im node.exe > NUL", shell=True, stderr=errfile, stdout=logfile)
    return 0
  
  p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
  out, err = p.communicate()
  for line in out.splitlines():
    if 'hello.js' in line:
      pid = int(line.split(None, 2)[1])
      try:
        os.kill(pid, 15)
      except OSError:
        pass
  return 0
