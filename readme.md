# FrameFinder

A set of python scripts to find the timestamp an image appears in a video

## Use

```bash
=>python main.py -h
usage: main.py [-h] [--async] [--processes PROCESSES] [--video VIDEO]
               [--image IMAGE]

Find timestamp of image in video

optional arguments:
  -h, --help            show this help message and exit
  --async, -a           Run asyncronously
  --processes PROCESSES, -p PROCESSES
                        Number of processes to run on (default 1)
  --video VIDEO, -v VIDEO
                        Video to traverse
  --image IMAGE, -i IMAGE
                        Image to find
```

### Example

`python main.py -v example.mp4 -i example.png`

## Recommendations

Async is slower than synchronous for a low number of processes.
If you're running on a slow processor or a low number of cores, you should run this synchronously.
