import re
import math
import copy
from pathlib import Path
from pysrt import SubRipFile, SubRipItem, SubRipTime
from typing import Union, Tuple, Optional

clean_rgx = re.compile(r"\s*<.*?>")
dash_rgx = re.compile(r"(\w)-(\w)")
digitos_rgx = re.compile(
    r"silence_end: (?P<end>\d*\.*\d*) \| silence_duration: (?P<duration>\d*\.*\d*)"
)

LIMIT_CPS = 17
RECOMMENDED_CPS = 15
MAX_SEPARATION = 1250

PRIMARY_SYM = ["."]
SECONDARY_SYM = [",", ";", "?", "!", ":"]
TERTIARY_SYM = [" "]


#################
# Aux functions #
#################
def milliseconds_to_subriptime(millis: int) -> SubRipTime:
    """
    Convert a number of milliseconds to a SubRipTime (somewhat similar to datetime.time)

    :param millis: total time in milliseconds
    :returns: a SubRipTime(hours, minutes, seconds, milliseonds) object
    """
    hours, remaining = divmod(millis, (1000 * 60 * 60))
    minutes, remaining = divmod(remaining, (1000 * 60))
    seconds, milliseconds = divmod(remaining, 1000)
    return SubRipTime(hours, minutes, seconds, milliseconds)


def subriptime_to_milliseconds(subriptime: SubRipTime) -> int:
    """
    Convert a SubRipTime object to milliseconds

    :param subriptime: a SubRipTime obj (somewhat similar to datetime.time)
    :returns: the total number of milliseconds represented in that object
    """
    total_millis = (
        ((((subriptime.hours * 60) + subriptime.minutes) * 60) + subriptime.seconds)
        * 1000
    ) + subriptime.milliseconds
    return total_millis


#################
# Text cleaning #
#################
def cleanhtml(raw_html: str) -> str:
    """
    Takes a string that might contain HTML marks and removes them using regex, leaving
    just the text. Also removes a couple of other markers

    :param raw_html: a string that may contain HTML and other kind of markup text
    :returns: the same text clean of any markup
    """
    cleantext = re.sub(clean_rgx, "", raw_html)
    cleantext = cleantext.replace("[vacilación]", "...")
    cleantext = cleantext.replace("&nbsp;", " ")
    return cleantext


##############
# CPS fixing #
##############
def fix_subtitles_cps(subtitles: SubRipFile) -> SubRipFile:
    cps_fixed_subs = SubRipFile()
    j = 1
    skip_next = False
    for i in range(len(subtitles)):
        sub = subtitles[i]
        if skip_next:
            skip_next = False
            continue
        if sub.characters_per_second < LIMIT_CPS:
            cps_fixed_subs.append(
                SubRipItem(index=j, start=sub.start, end=sub.end, text=sub.text)
            )
            j += 1
            continue

        prev_sub = None
        next_sub = None
        if len(cps_fixed_subs) > 0:
            prev_sub = cps_fixed_subs[-1]
        if i != (len(subtitles) - 1):
            next_sub = subtitles[i + 1]

        merge_prev_sub = None
        merge_next_sub = None
        if prev_sub and (sub.start - prev_sub.end).ordinal < 1500:
            merge_prev_sub = SubRipItem(
                start=prev_sub.start, end=sub.end, text=f"{prev_sub.text} {sub.text}"
            )
        if next_sub and (next_sub.start - sub.end).ordinal < 1500:
            merge_next_sub = SubRipItem(
                start=sub.start, end=next_sub.end, text=f"{sub.text} {next_sub.text}"
            )

        merge_sub = None
        if (merge_prev_sub is not None) and (merge_next_sub is not None):
            if (
                merge_prev_sub.characters_per_second
                < merge_next_sub.characters_per_second
            ) and (merge_prev_sub.characters_per_second < sub.characters_per_second):
                merge_sub = merge_prev_sub
                cps_fixed_subs.pop()
                j -= 1
            else:
                merge_sub = merge_next_sub
                skip_next = True
        elif merge_prev_sub is not None:
            merge_sub = merge_prev_sub
            cps_fixed_subs.pop()
            j -= 1
        elif merge_next_sub is not None:
            merge_sub = merge_next_sub
            skip_next = True
        else:
            merge_sub = sub
        merge_sub.index = j
        cps_fixed_subs.append(merge_sub)
        j += 1
    return cps_fixed_subs


####################
# Subtitle merging #
####################
def join_subtitle_sentences(
    subs: SubRipFile, max_length: int = 120, split_mode: int = 2
):
    for ronda in range(3):
        new_subs = SubRipFile()
        prev_s = subs[0]
        cum_text = prev_s.text
        cum_start = prev_s.start
        i = 0
        for s in subs[1:]:
            last_char = cum_text.strip()[-1]
            aux = f"{cum_text} {s.text}"
            if (
                (ronda == 0 and last_char in (PRIMARY_SYM + SECONDARY_SYM))
                or (ronda == 1 and last_char in PRIMARY_SYM)
                or (
                    not should_force_join(last_char, split_mode)
                    and len(aux) > max_length
                )
                or (s.start - prev_s.end > MAX_SEPARATION)
            ):
                new_subs.append(
                    SubRipItem(index=i, text=cum_text, start=cum_start, end=prev_s.end)
                )
                cum_text = s.text
                cum_start = s.start
                prev_s = s
                i += 1
                continue
            cum_text = aux
            prev_s = s
        new_subs.append(
            SubRipItem(index=i, text=cum_text, start=cum_start, end=prev_s.end)
        )
        subs = new_subs
    return subs


def should_force_join(char, split_mode):
    if split_mode >= 3:
        return False
    if split_mode >= 2:
        if char in (SECONDARY_SYM + PRIMARY_SYM):
            return False
        else:
            return True
    if split_mode >= 1:
        if char in PRIMARY_SYM:
            return False
        else:
            return True
    return False


######################
# Subtitle splitting #
######################
def split_sentence_by_punctuation(
    text: str,
    start: SubRipTime,
    end: SubRipTime,
    split_mode: int,
    recommended_size: int,
):
    duration = subriptime_to_milliseconds(end - start)
    ltext = len(text)
    if ltext <= recommended_size:
        return [(text, start, end)]

    primary_symbols = []
    secondary_symbols = []
    tertiary_symbols = []
    if split_mode >= 1:
        primary_symbols = PRIMARY_SYM
    if split_mode >= 2:
        secondary_symbols = SECONDARY_SYM
    if split_mode >= 3:
        tertiary_symbols = TERTIARY_SYM
    primary_positions = []
    secondary_positions = []
    tertiary_positions = []
    for i, c in enumerate(text):
        if i in (0, ltext - 1):
            continue
        if (
            (c in primary_symbols)
            and not (text[i - 1].isdigit() and text[i + 1].isdigit())
            and not (text[i + 1] == ".")
        ):
            primary_positions.append(i)
        elif c in secondary_symbols:
            secondary_positions.append(i)
        elif c in tertiary_symbols:
            tertiary_positions.append(i)

    if len(primary_positions) > 0:
        symbol_positions = primary_positions
    elif len(secondary_positions) > 0:
        symbol_positions = secondary_positions
    elif len(tertiary_positions) > 0:
        symbol_positions = tertiary_positions
    else:
        return [(text, start, end)]

    selected_position = 0
    distance = math.inf
    for p in symbol_positions:
        distance_aux = abs(p - ltext / 2)
        if distance_aux < distance:
            distance = distance_aux
            selected_position = p
    if selected_position == 0:
        return [(text, start, end)]

    sentence_a = text[: selected_position + 1].strip()
    sentence_b = text[selected_position + 1 :].strip()
    proportions = [(len(sentence_a) / ltext), (len(sentence_b) / ltext)]

    duration_a = int(duration * proportions[0])
    start_a = start
    end_a = start_a + milliseconds_to_subriptime(duration_a)
    start_b = end_a
    end_b = end

    results = []
    if len(sentence_a) > recommended_size:
        results += split_sentence_by_punctuation(
            sentence_a, start_a, end_a, split_mode, recommended_size
        )
    else:
        results.append((sentence_a, start_a, end_a))

    if len(sentence_b) > recommended_size:
        results += split_sentence_by_punctuation(
            sentence_b, start_b, end_b, split_mode, recommended_size
        )
    else:
        results.append((sentence_b, start_b, end_b))
    return results


def split_subs_by_punctuation(subtitles, split_mode, subtitle_len=120):
    result_subs = SubRipFile()
    i = 1
    for s in subtitles:
        frags = split_sentence_by_punctuation(
            text=s.text,
            start=s.start,
            end=s.end,
            split_mode=split_mode,
            recommended_size=subtitle_len,
        )
        for frag in frags:
            result_subs.append(
                SubRipItem(index=i, text=frag[0], start=frag[1], end=frag[2])
            )
            i += 1
    return result_subs


#####################
# Silence treatment #
#####################
def load_silences(silences_file: Path) -> list:
    """
    Read a silences file and return its contents in list of dicts form

    :param silences_file: path to a silences (*.slc) file, as generated by find_silences
    :returns: a list of dicts, each representing start, end and duration of a silence
    """
    f = open(silences_file, "r")
    silences = []
    for line in f:
        if "silence_end" in line:
            m = digitos_rgx.search(line)
            if m is not None:
                end = float(m.group("end"))
                duration = float(m.group("duration"))
                silences.append(
                    {
                        "start": end - duration,
                        "end": end,
                        "duration": duration,
                    }
                )
    return silences


def check_silence(
    silences: list, time: SubRipTime
) -> Union[SubRipTime, Tuple[SubRipTime, SubRipTime]]:
    """
    Given a list of silences and a specific time, get silence start and end times if the
    provided time is placed within a silence.
    E.g. if there is a silence between seconds 1.0 and 1.8, and time is 1.2, the
    function would return (1.0, 1.8). On the other hand, if time is 0.8, it would return
    (0.8, 0.8) because there is no silence

    :param silences: a list of silences in the video as given by load_silences
    :param time: a specific input time in SubRipTime format
    :returns: silence start and end times or the original time
    """
    result = time
    for silence in silences:
        if (
            time.ordinal > silence["start"] * 1000
            and time.ordinal < silence["end"] * 1000
        ):
            result = (
                milliseconds_to_subriptime(int(silence["start"] * 1000)),
                milliseconds_to_subriptime(int(silence["end"] * 1000)),
            )
            break
    return result


def align_subs_to_silences(subtitles, silences_file):
    result_subs = SubRipFile()
    sils = load_silences(silences_file)
    for s in subtitles:
        if s.characters_per_second > RECOMMENDED_CPS:
            result_subs.append(s)
            continue
        aux_sub = copy.deepcopy(s)
        start_silence = check_silence(sils, s.start)
        if not isinstance(start_silence, SubRipTime):
            aux_sub.start = start_silence[1]
            if aux_sub.characters_per_second > RECOMMENDED_CPS:
                aux_sub.start = s.start

        end_silence = check_silence(sils, s.end)
        if not isinstance(end_silence, SubRipTime):
            aux_sub.end = end_silence[0]
            if aux_sub.characters_per_second > RECOMMENDED_CPS:
                aux_sub.end = s.end
        result_subs.append(aux_sub)
    return result_subs


####################
# Central function #
####################
def resegment_sub(
    subtitle: SubRipFile,
    silences_file: Optional[Path] = None,
    split_mode: int = 2,
    line_length: int = 120,
) -> SubRipFile:
    for s in subtitle:
        s.text = cleanhtml(s.text).strip()
        s.text = s.text.replace("\n", " ")
        s.text = dash_rgx.sub(r"\1 \2", s.text)
    # subtitle = fix_subtitles_cps(subtitle)
    subtitle = split_subs_by_punctuation(
        subtitle, split_mode=split_mode, subtitle_len=0
    )
    subtitle = join_subtitle_sentences(subtitle, line_length, split_mode)
    if silences_file:
        subtitle = align_subs_to_silences(subtitle, silences_file)
    return subtitle
