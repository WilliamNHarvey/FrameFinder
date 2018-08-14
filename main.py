from multiprocessing import Pool, Manager
from FileVideoStream import FileVideoStream
from processor import process_frame, imread

import time
import argparse

# Main methods
def main():
  count = 0
  while vidcap.remaining() > 0 or vidcap.more():
    if found.value > 0: return found.value
    if count % 30 == 0: print(".", end='', flush=True)
    img_rgb = vidcap.read()
    r = pool.apply(process_frame, (img_rgb, template, count))
    if r[0]:
      found.value = r[1]
      break
    count += 1

def main_async():
  count = 0
  while vidcap.remaining() > 0 or vidcap.more():
    img_rgb = vidcap.read()
    if found.value > 0: return found.value
    r = pool.apply_async(process_frame, (img_rgb, template, count), callback=check_res, error_callback=kill_pool)
    results.append(r)
    count += 1
  return found.value

# Async callbacks
def check_res(res):
  if res[1] % vidcap.fps == 0: print(".", end='', flush=True)
  if res[0]:
    found.value = res[1]
    close_pool()
    print_results(True)
    exit(1)

def kill_pool():
  pool.terminate()

# Output and cleanup
def close_pool():
  pool.close()
  pool.terminate()

def print_results(passed):
  if passed:
    print("\n\nFound at " + str("%.2f" % (found.value / vidcap.fps)) + " seconds")
    print('Output saved to frames/res%s.png' % found.value)
  else:
    print("\n\nNot found")
  print("--- {0} seconds --- {1} {2} processes ---".format(time.time() - start_time, "async" if ASYNC else "sync", processes))

# Execution script
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Find timestamp of image in video')
  parser.add_argument('--async', '-a', action='store_true',
                    help='Run asyncronously')
  parser.add_argument('--processes', '-p', dest='processes', type=int, action='store', default=1,
                    help='Number of processes to run on (default 1)')
  parser.add_argument('--video', '-v', action='store', type=str,
                    help='Video to traverse')
  parser.add_argument('--image', '-i', action='store', type=str,
                    help='Image to find')
  
  args = parser.parse_args()
  vidcap_file = args.video
  template_file = args.image
  errors = []
  if not vidcap_file:
    errors.append("Must pass video with --video or -v")
  if not template_file:
    errors.append("Must pass image with --image or -i")
  if len(errors) > 0:
    print(*errors, sep='\n')
    exit(0)
  
  ASYNC = args.async
  processes = args.processes

  start_time = time.time()
  print("Traversing", end='', flush=True)
  pool = Pool(processes=processes) # Worker
  m = Manager()
  found = m.Value('i', 0)
  results = []
  vidcap = FileVideoStream(vidcap_file).start()
  template = imread(template_file)
  if ASYNC:
    main_async()
    for r in results:
      if found.value:
        close_pool()
        print_results(True)
        exit(1)
      else:
        r.wait()
  else:
    main()
    if found.value:
      close_pool()
      print_results(True)
      exit(1)

  close_pool()
  print_results(False)
