# subtitle_normalizer

**subtitle_normalizer** is a library that provides some useful functionalities when
working with subtitle files. In particular, the module includes functions to rearrange
the captions, joining and splitting them according to the given arguments, while
automatically recalculating the start and end times.

Some of the functionalities provided are:
    - Cleaning some symbols that sometimes appear in the captions (like HTML tags)
    - Joining and splitting of the subtitles to make them match the punctuation
    - Passing a silences file (generated with ffmpeg) to improve the subtitles matching
      the sound
    - Custom configuration of the symbols used to split the sentences.
    - Custom configuration of the desired length of the captions.
