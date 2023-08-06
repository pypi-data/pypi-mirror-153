from typing import List, Optional, Union
from os import path
import random

from kcu import sh, kpath

from . import ffprobe

def reduce_audio_volume(
    path_in: str,
    path_out: str,
    volume: Union[int, str] = 0.25,
    debug: bool = False
) -> bool:
    sh.sh(
        'ffmpeg -y -i {} -filter:a "volume={}" {}'.format(path_in, volume, path_out),
        debug=debug
    )

    return path.exists(path_out)

def get_audio_from_video(
    path_in: str,
    path_out: str,
    debug: bool = False
) -> bool:
    sh.sh(
        'ffmpeg -y -i {} -vn -acodec copy {}'.format(path_in, path_out),
        debug=debug
    )

    return path.exists(path_out)

def mix_audios(
    audio_path_1: str,
    audio_path_2: str,
    path_out: str,
    duration: Optional[str] = 'longest',
    debug: bool = False
) -> bool:
    cmd = 'ffmpeg -y -i {} -i {} -filter_complex amix=inputs=2'.format(audio_path_1, audio_path_2)

    if duration:
        cmd += ':duration={}'.format(duration)

    cmd += ' ' + path_out
    sh.sh(cmd, debug=debug)

    return path.exists(path_out)

def mix_multiple_audios(
    audio_paths: List[str],
    path_out: str,
    duration: Optional[str] = 'longest',
    debug: bool = False
) -> bool:
    cmd = 'ffmpeg -y'

    for audio_path in audio_paths:
        cmd += ' -i ' + sh.path(audio_path)

    cmd += ' -filter_complex amix=inputs=' + str(len(audio_paths))

    if duration:
        cmd += ':duration={}'.format(duration)

    cmd += ' ' + path_out
    sh.sh(cmd, debug=debug)

    return path.exists(path_out)

def reencode_mp3(
    path_in: str,
    path_out: str,
    debug: bool = False
) -> bool:
    sh.sh(
        'ffmpeg -y -i ' + path_in + ' -codec:a libmp3lame -qscale:a 2 ' + path_out, debug=debug
    )

    return path.exists(path_out)

def reencode_aac(
    path_in: str,
    path_out: str,
    debug: bool = False
) -> bool:
    sh.sh('ffmpeg -y -i {} -codec:a aac {}'.format(path_in, path_out), debug=debug)

    return path.exists(path_out)

# for ex wav to m4a
def simple_reencode(
    path_in: str,
    path_out: str,
    debug: bool = False
) -> bool:
    sh.sh(f'ffmpeg -y -i {path_in} {path_out}', debug=debug)

    return path.exists(path_out)

def reencode(
    path_in: str,
    path_out: str,
    fps: Optional[Union[int, float, str]] = None,
    sar: Optional[str] = None,
    resolution: Optional[str] = None,
    debug: bool = False
) -> bool:
    ''' resolution and sar should be given in the following format: "x:y"
        fps should be lower than the original value so frames don't freeze
    '''

    cmd = 'ffmpeg -y -i {}'.format(path_in)

    if fps or sar:
        cmd_filter = ''

        if fps:
            cmd_filter += 'fps={}'.format(fps)
        if resolution:
            if len(cmd_filter) > 0:
                cmd_filter += ','

            cmd_filter += 'scale={}'.format(resolution)
        if sar:
            if len(cmd_filter) > 0:
                cmd_filter += ','

            cmd_filter += 'setsar={}'.format(sar)

        cmd += ' -filter:v ' + cmd_filter

    sh.sh('{} {}'.format(cmd, path_out), debug=debug)

    return path.exists(path_out)

def ts_to_mp4(
    path_in: str,
    path_out: str,
    debug: bool = False
) -> bool:
    sh.sh('ffmpeg -y -i {} -acodec copy -vcodec copy {}'.format(path_in, path_out), debug=debug)

    return path.exists(path_out)

def flip_video_horizontal(
    path_in: str,
    path_out: str,
    debug: bool = False
) -> bool:
    sh.sh('ffmpeg -y -i {} -vf hflip -c:a copy {}'.format(path_in, path_out), debug=debug)

    return path.exists(path_out)

def flip_video_vertical(
    path_in: str,
    path_out: str,
    debug: bool = False
) -> bool:
    sh.sh('ffmpeg -y -i {} -vf vflip -c:a copy {}'.format(path_in, path_out), debug=debug)

    return path.exists(path_out)

def rotate_video(
    path_in: str,
    path_out: str,
    times_90_degrees: int,
    debug: bool = False
) -> bool:
    times_90_degrees = times_90_degrees % 4

    rot_val = 1 if times_90_degrees > 0 else 2

    if times_90_degrees == 0:
        sh.cp(path_in, path_out)
    else:
        sh.sh(
            'ffmpeg -y -i {} -vf "{}" {}'.format(
                sh.path(path_in),
                ','.join(['transpose={}'.format(rot_val) for _ in range(times_90_degrees)]),
                sh.path(path_out)
            ),
            debug=debug
        )

    return path.exists(path_out)

def modify_audio(
    path_in: str,
    path_out: str,
    channels: Optional[int] = None,     # 2
    audio_rate: Optional[int] = None,   # 44100
    bit_rate: Optional[int] = None,     # 133
    debug: bool = False
) -> bool:
    cmd = 'ffmpeg -y -i {}'.format(path_in)

    if channels:
        cmd += ' -ac {}'.format(channels)

    if audio_rate:
        cmd += ' -ar {}'.format(audio_rate)

    if bit_rate:
        cmd += ' -ab {}k'.format(bit_rate)

    cmd += ' {}'.format(path_out)
    sh.sh(cmd, debug=debug)

    return path.exists(path_out)

def create_video_from_images(
    input_folder: str,
    output_file_path: str,
    seconds_per_image: float = 3.0,
    file_base_name: str = 'image',
    file_extension: str = '.jpg',
    debug: bool = False
) -> bool:
    start_number = 0

    while True:
        first_image_path = path.join(input_folder, file_base_name + '{:03d}'.format(start_number) + file_extension)

        if path.exists(first_image_path):
            break

        start_number += 1

    sh.sh(
        'ffmpeg -y -framerate ' + str(1.0/seconds_per_image) + ' -start_number ' + '{:03d}'.format(start_number) + ' -i ' + path.join(input_folder, file_base_name + '%03d' + file_extension) + ' -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" ' + output_file_path,
        debug=debug
    )

    return path.exists(output_file_path)

def create_video_from_image_paths(
    image_paths: List[str],
    output_file_path: str,
    seconds_per_image: float = 3.0,
    temp_folder_path: Optional[str] = None,
    debug: bool = False
) -> bool:
    temp_folder_path = temp_folder_path or path.join(kpath.folder_path_of_file(), '.__ffmpeg_images_temp')
    import os
    os.makedirs(temp_folder_path, exist_ok=True)

    file_base_name = 'image'
    i = 1
    file_extension = kpath.extension(image_paths[0], include_dot=True)

    for image_path in image_paths:
        new_image_path = path.join(temp_folder_path, file_base_name + '{:03d}'.format(i) + file_extension)
        sh.cp(image_path, new_image_path)
        i += 1

    res = create_video_from_images(temp_folder_path, output_file_path, seconds_per_image=seconds_per_image, file_base_name=file_base_name, file_extension=file_extension, debug=debug)
    kpath.remove(temp_folder_path)

    return res

def create_video_from_image(
    image_path: str,
    output_file_path: str,
    duration: float = 3.0,
    fps: float = 30.0,
    debug: bool = False
) -> bool:
    sh.sh(
        'ffmpeg -y -loop 1 -framerate ' + str(fps) + ' -i ' + image_path + ' -t ' + str(duration) + ' -pix_fmt yuv420p ' + output_file_path,
        debug=debug
    )

    return path.exists(output_file_path)

def remove_audio(
    input: str,
    output: str,
    debug: bool = False
) -> bool:
    sh.sh(
        'ffmpeg -y -i ' + sh.path(input) + ' -c copy -an ' + sh.path(output), debug=debug
    )

    return path.exists(output)

def add_silence_to_video(
    input: str,
    output: str,
    sample_rate: int = 48000,
    duration: str = 'shortest',
    debug: bool = False
) -> bool:
    cmd = 'ffmpeg -f lavfi -y -i anullsrc=channel_layout=stereo:sample_rate={} -i {} -c:v copy -c:a aac '.format(sample_rate, sh.path(input))

    if duration == 'shortest':
        cmd += '-shortest '

    cmd += sh.path(output)
    sh.sh(cmd, debug=debug)

    return path.exists(output)

def add_audio_to_video(
    input_a: str,
    input_v: str,
    output: str,
    duration: str = 'shortest',
    reencode: bool = False,
    debug: bool = False
) -> bool:
    cmd = 'ffmpeg -y -i ' + sh.path(input_v)+ ' -i ' + sh.path(input_a)

    if not reencode:
        cmd += ' -c:v copy -map 0:v:0 -map 1:a:0'

    if duration == 'shortest':
        cmd += ' -shortest'

    cmd += ' ' + sh.path(output)

    sh.sh(cmd, debug=debug)

    return path.exists(output)

def loop_audio_to_video(
    in_a: str,
    in_v: str,
    out: str,
    reencode: bool = False,
    debug: bool = False
) -> bool:
    return __loop_together(in_v, in_a, out, reencode=reencode, debug=debug)

def loop_video_to_audio(
    in_a: str,
    in_v: str,
    out: str,
    reencode: bool = False,
    debug: bool = False
) -> bool:
    return __loop_together(in_a, in_v, out, reencode=reencode, debug=debug)

def loop(
    in_path: str,
    out_path: str,
    length_seconds: float,
    debug: bool = False
) -> bool:
    sh.sh('ffmpeg -y -stream_loop -1 -i ' + sh.path(in_path) + ' -t ' + str(length_seconds) + ' ' + sh.path(out_path), debug=debug)

    return path.exists(out_path)

def trim(
    in_path: str,
    out_path: str,
    start_seconds: float = 0,
    stop_seconds: Optional[float] = None,
    duration: Optional[float] = None,
    reencode: bool = False,
    debug: bool = False
) -> bool:
    """PASS EITHER 'stop_seconds' OR 'duration'
    IF BOTH PASSED, 'duration' will be taken as preference
    """
    if stop_seconds is None and duration is None:
        print('Either, \'stop_seconds\' should e passed or \'duration\'')

        return False

    if duration is None:
        duration = stop_seconds - start_seconds

    sh.sh(
        'ffmpeg -y -ss {} -i {} -t {} {} {}'.format(__seconds_to_time_str(start_seconds), sh.path(in_path), __seconds_to_time_str(duration), '-c copy -avoid_negative_ts make_zero' if reencode else '-async 1', sh.path(out_path)),
        debug=debug
    )

    return path.exists(out_path)

def convert_video_to_16_9(
    in_path: str,
    out_path: str,
    debug: bool = False
) -> bool:
    w, h = ffprobe.video_resolution(in_path)

    if h is None or w is None:
        return False

    if h == 1080 and w == 1920:
        sh.cp(in_path, out_path)

        return True

    if w/h < 16/9:
        sh.sh(
            'ffmpeg -y -i ' + sh.path(in_path) + " -vf 'split[original][copy];[copy]scale=1920:-1,setsar=1:1,crop=h=1080,gblur=sigma=75[blurred];[original]scale=-1:1080[original_resized];[blurred][original_resized]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2' " + sh.path(out_path), debug=debug
        )
    else:
        sh.sh(
            'ffmpeg -y -i ' + sh.path(in_path) + " -vf 'split[original][copy];[copy]scale=-1:1080,setsar=1:1,crop=w=1920,gblur=sigma=75[blurred];[original]scale=1920:-1[original_resized];[blurred][original_resized]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2' " + sh.path(out_path), debug=debug
        )

    return path.exists(out_path)

def concat_videos(
    in_paths: List[str],
    out_path: str,
    reencode: bool = False,
    debug: bool = False
) -> bool:
    f = concat_videos_reencode if reencode else concat_videos_copy

    return f(in_paths, out_path, debug=debug)

def concat_videos_copy(
    in_paths: List[str],
    out_path: str,
    debug: bool = False
) -> bool:
    if len(in_paths) == 0:
        return False
    elif len(in_paths) == 1:
        sh.cp(in_paths[0], out_path)

        return True

    temp_txt_path = path.join(kpath.folder_path_of_file(out_path), '__temp_list.txt')

    with open(temp_txt_path, 'w') as f:
        f.write('\n'.join(['file \'' + p + '\'' for p in in_paths]))

    sh.sh('ffmpeg -y -f concat -safe 0 -i ' + sh.path(temp_txt_path) + ' -c copy ' + sh.path(out_path), debug=debug)
    kpath.remove(temp_txt_path)

    return path.exists(out_path)

def concat_videos_loop(
    in_paths: List[str],
    out_path: str,
    video_duration: float,
    randomize_videos: Optional[bool] = False,
    debug: bool = False
) -> bool:
    if len(in_paths) == 0:
        return False
    elif len(in_paths) == 1:
        sh.cp(in_paths[0], out_path)

        return True

    temp_txt_path = path.join(kpath.folder_path_of_file(out_path), '__temp_video_paths.txt')
    current_video_duration = 0
    final_text = ''

    while current_video_duration < video_duration:
        if randomize_videos:
            random.shuffle(in_paths)

        for vid_path in in_paths:
            final_text += 'file ' + '\'' + vid_path + '\'\n'
            subvid_duration = ffprobe.get_duration(vid_path)
            current_video_duration += subvid_duration

            if current_video_duration >= video_duration:
                with open(temp_txt_path, 'w') as f:
                    f.write(final_text)

                break

    sh.sh('ffmpeg -y -f concat -safe 0 -i ' + sh.path(temp_txt_path) + ' -c copy ' + sh.path(out_path), debug=debug)
    kpath.remove(temp_txt_path)

    return path.exists(out_path)

#aliases
concat_copy = concat_videos_copy
concat_audios_copy = concat_videos_copy

def concat_videos_reencode(
    in_paths: List[str],
    out_path: str,
    debug: bool = False
) -> bool:
    if len(in_paths) == 0:
        return False
    elif len(in_paths) == 1:
        sh.cp(in_paths[0], out_path)

        return path.exists(out_path)

    cmd = 'ffmpeg -y'

    for path_ in in_paths:
        cmd += ' -i ' + sh.path(path_)

    cmd += ' -filter_complex "'

    for i in range(len(in_paths)):
        cmd += '[{}:v] [{}:a] '.format(i, i)

    cmd += 'concat=n={}:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" '.format(len(in_paths)) + sh.path(out_path)

    sh.sh(cmd, debug=debug)

    return path.exists(out_path)

def get_frame(
    at_second: float,
    p_video_in: str,
    p_img_out: str,
    debug: bool = False
) -> bool:
    res = sh.sh(
        'ffmpeg -ss {} -i {} -frames:v 1 {}'.format(at_second, p_video_in, p_img_out),
        debug=debug
    )

    if debug:
        print(res)

    return path.exists(p_img_out)


# Private

# both in_reference_path and in_follower_path can be audio or video
# 1 needs to be video, the otheer needs to be audio
def __loop_together(
    in_reference_path: str,
    in_follower_path: str,
    out: str,
    reencode: bool = False,
    debug: bool = False
) -> bool:
    reference_dur = ffprobe.get_duration(in_reference_path)
    follower_dur = ffprobe.get_duration(in_follower_path)

    looped_follower_path = kpath.temp_path_for_path(in_follower_path)

    if reference_dur > follower_dur:
        if not loop(in_follower_path, looped_follower_path, reference_dur, debug=debug):
            return False
    else:
        looped_follower_path = None

    in_video_path = in_reference_path
    in_audio_path = looped_follower_path or in_follower_path

    if ffprobe.has_video(in_audio_path):
        in_video_path = in_audio_path
        in_audio_path = in_reference_path

    return add_audio_to_video(in_audio_path, in_video_path, out, reencode=reencode, debug=debug)

def __seconds_to_time_str(
    seconds: float
) -> str:
    h = int(seconds/3600)
    m = int((seconds - h*3600)/60)
    s = int(seconds - h*3600 - m*60)
    ms = seconds - int(seconds)

    ms_str = ("%.8f" % (ms)).strip('0') if ms > 0 else ''

    return "%02d:%02d:%02d" % (h, m, s) + ms_str