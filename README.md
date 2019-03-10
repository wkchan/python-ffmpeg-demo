# python-ffmpeg-demo
### Version:
- v0.1.2

## Author
* Linus Chan (wkchan(dot)linus(at)gmail(dot)com)

## Comments
* currently available in MacOS only
* Added stream to hls feature
* Added stream to rtmp feature

## Prerequisites

* ```brew install ffmpeg```
* ```brew install ffprobe```
* install MAMP
* using nginx wirh rtmp module for the local RTMP server ```docker run -d -p 1935:1935 --name nginx-rtmp tiangolo/nginx-rtmp```




### Version:
- v0.1.1

## Author
* Linus Chan (wkchan(dot)linus(at)gmail(dot)com)

## Comments
* Updated naming style
* Added two pytest test cases
** ffprobe availability
** ffmpeg functionality


### Version:
- v0.1.0

## Author
* Linus Chan (wkchan(dot)linus(at)gmail(dot)com)

## Comments
- Init commit of python-ffmpeg evaluation
- Enable record Apple facetime to a particular out_filename
- Process the Apple facetime stream with numpy for effects

## Prerequisites

* brew install ffmpeg or set a path to your ffmpeg binary
* virtual environment
