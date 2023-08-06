import math
import re
from pathlib import Path
from loguru import logger

rgx_vtt_ts = re.compile(
    r"^(\d{2}:\d{2}:\d{2})\.(\d{3}) --> (\d{2}:\d{2}:\d{2})\.(\d{3})$"
)
rgx_vtt_header = re.compile(r"^\s*WEBVTT\s*$")
rgx_counter = re.compile(r"^\s*\d+\s*$")
rgx_srt_ts = re.compile(
    r"^(\d{2}:\d{2}:\d{2}),(\d{3}) --> (\d{2}:\d{2}:\d{2}),(\d{3})$"
)
rgx_empty = re.compile(r"^\s*$")
rgx_non_empty = re.compile(r"^.*\S.*$")
rgx_end_of_sentence = re.compile(r"^.*[\.\?!:]$")

rgx_after_punctuation = re.compile(r'[\.!?]\s+(\w)')


def seconds_to_vtt_time(secs_time):
    dec, whole = math.modf(secs_time)
    dec = round(dec, 3)
    hours, whole = divmod(whole, 3600)
    mins, whole = divmod(whole, 60)
    hours = int(hours)
    mins = int(mins)
    secs = int(whole)
    return f"{hours:02}:{mins:02}:{secs:02}" + f"{dec:.3f}".lstrip("0")


def vtt_to_srt(vtt_file):
    srt_version = ""
    counter = 1
    with open(vtt_file) as f:
        for line in f.readlines():
            m0 = rgx_vtt_ts.match(line)
            if m0:
                p0, p1, p2, p3 = m0.groups()
                srt_line = f"\n{counter}\n{p0},{p1} --> {p2},{p3}\n"
                srt_version += srt_line
                counter += 1
            elif rgx_empty.match(line) or rgx_vtt_header.match(line):
                pass
            else:
                srt_version += f"{line}"
    srt_version = srt_version.strip()
    return srt_version


def srt_to_vtt(srt_file):
    vtt_version = "WEBVTT\n\n"
    with open(srt_file) as f:
        for line in f.readlines():
            m = rgx_srt_ts.match(line)
            if rgx_empty.match(line) or rgx_counter.match(line):
                pass
            elif m:
                vtt_version += f"\n{m[0].replace(',', '.')}\n"
            else:
                vtt_version += f"{line}"
    return vtt_version


def is_valid_srt(caption):
    with open(caption) as f:
        state = 0
        for line in f.readlines():
            if state == 0 and rgx_counter.match(line):
                state = 1
            elif state == 1 and rgx_srt_ts.match(line):
                state = 2
            elif state == 2:
                if rgx_empty.match(line):
                    state = 0
            else:
                return False
    return True


def is_valid_vtt(caption):
    with open(caption) as f:
        state = 0
        for line in f.readlines():
            print(f"State: {state}, line: {line.strip()}")
            if state == 0 and rgx_vtt_header.match(line):
                state = 1
            elif (state == 1) and (
                (m0 := rgx_vtt_ts.match(line)) or rgx_empty.match(line)
            ):
                if m0:
                    state = 2
            elif (state == 2) and (
                (m0 := rgx_empty.match(line)) or (rgx_non_empty.match(line))
            ):
                if m0:
                    state = 1
            else:
                return False
    return True


def get_data_from_upload_request(request):
    video = request.FILES["video_file"]
    lang = request.POST["lang"]
    transcription_file = None
    if "caption_file" in request.FILES:
        transcription_file = request.FILES["caption_file"]
        logger.info(
            (
                f"Uploading video {video.name} with language {lang} and "
                f"transcript {transcription_file}"
            )
        )
    else:
        logger.info(
            (f"Uploading video {video.name} with language {lang} and no transcription")
        )
    return (video, lang, transcription_file)


def upload_transcription_file(video, lang, upload):
    logger.info("Uploading transcription file...")
    success = True
    caption_ext = Path(upload.name).suffix.strip(".")
    logger.info(f"Extension: {caption_ext}")
    try:
        transcription = video.subtitle_set.get(lang_code=lang)
        with open(transcription.get_path(sub_format=caption_ext), "wb+") as output_file:
            for chunk in upload.chunks():
                output_file.write(chunk)
        if caption_ext != "srt":
            transcription.convert_to_format(format="srt", force=True)
        transcription.convert_to_format(force=True)
    except Exception as e:
        logger.error("Something failed and transcription could not be uploaded!")
        logger.exception(e)
        success = False
    return success


def fix_captions_capitalization(vtt_caption):
    capitalized_captions = ""
    status = 0
    for line in vtt_caption.split("\n"):
        if (
            rgx_vtt_ts.match(line)
            or rgx_empty.match(line)
            or rgx_vtt_header.match(line)
        ):
            pass
        else:
            line = capitalize_line(line)
            if status == 0:
                line = f"{line[0:1].upper()}{line[1:]}"
            if rgx_end_of_sentence.match(line.strip()):
                status = 0
            else:
                status = 1
        capitalized_captions += f"{line}\n"
    return capitalized_captions


def capitalize_line(sentence):
    aux = list(sentence)
    for m in rgx_after_punctuation.finditer(sentence):
        pos = m.span()[1] - 1
        letter = aux[pos]
        aux[pos] = letter.upper()
    return "".join(aux)
