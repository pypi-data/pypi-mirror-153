from __future__ import division

import datetime
import math
import multiprocessing
from multiprocessing import Pool
import os
import os.path as osp
from pathlib import Path
import shutil
import subprocess
import tempfile
from tempfile import NamedTemporaryFile

import cv2
import skvideo.io
from tqdm import tqdm

from pybsc.timestamp_utils import get_timestamp_indices_wrt_base


def hhmmss_to_seconds(ts):
    try:
        return float(ts)
    except ValueError:
        return sum(
            float(x) * 60 ** i
            for i, x in enumerate(reversed(ts.split(':'))))


def get_video_aspect_ratio(video_path):
    w, h = get_video_size(video_path)
    gcd = math.gcd(w, h)
    return w // gcd, h // gcd


def get_video_duration(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    return float(metadata['video']['@duration'])


def get_video_avg_frame_rate(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    a, b = metadata['video']['@avg_frame_rate'].split('/')
    a = int(a)
    b = int(b)
    return a / b


def get_video_size(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    height = int(metadata['video']['@height'])
    width = int(metadata['video']['@width'])
    return width, height


def get_video_n_frame(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    if '@nb_frames' not in metadata['video']:
        fps = get_video_avg_frame_rate(video_path)
        return int(fps * get_video_duration(video_path))
    return int(metadata['video']['@nb_frames'])


def get_video_creation_time(video_path):
    metadata = skvideo.io.ffprobe(video_path)
    tag_dict = {}
    for tag in metadata['video']['tag']:
        tag_dict[tag['@key']] = tag['@value']
    if 'creation_time' not in tag_dict:
        return None
    creation_time = tag_dict['creation_time']
    created_at = datetime.datetime.strptime(
        creation_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    return created_at


def split_video(video_file_path, output_path=None,
                start_time=None, end_time=None,
                hflip=False, vflip=False,
                out_to_null=True):
    if start_time is None and end_time is None:
        raise ValueError
    start_time = start_time or 0.0
    end_time = end_time or get_video_duration(video_file_path)
    command = ['ffmpeg',
               '-y',
               '-ss', str(start_time),
               '-t', str(end_time - start_time),
               '-i', str(video_file_path)]
    if hflip is True:
        command.extend(['-vf', 'hflip'])
    if vflip is True:
        command.extend(['-vf', 'vflip'])

    stdout = None
    stderr = None
    if out_to_null:
        stdout = subprocess.DEVNULL
        stderr = subprocess.DEVNULL
    if output_path is None:
        suffix = Path(video_file_path).suffix
        with NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
            command.append(tmp.name)
            if not out_to_null:
                print(f'Running \"{" ".join(command)}\"')
            proc = subprocess.Popen(command,
                                    stdout=stdout,
                                    stderr=stderr)
            proc.wait()
            shutil.copy(tmp.name, video_file_path)
    else:
        command.append(str(output_path))
        if not out_to_null:
            print(f'Running \"{" ".join(command)}\"')
        proc = subprocess.Popen(command,
                                stdout=stdout,
                                stderr=stderr)
        proc.wait()


def split_video_from_stamps(
        video_file_path,
        start_stamps, end_stamps,
        output_paths=None,
        output_dirpath=None,
        filename_tmpl='video_{start_frame:05}_{end_frame:05}.mp4',
        show_progress=True,
        parallel_process=False,
        n_jobs=8,
        hflip=False, vflip=False):
    if len(start_stamps) != len(end_stamps):
        raise RuntimeError(
            'Length not much len(start_stamps) != len(end_stamps)'
            '({})!=({})'.format(len(start_stamps), len(end_stamps)))
    fps = get_video_avg_frame_rate(video_file_path)
    if output_paths is None:
        output_paths = []
        if output_dirpath is None:
            tmp_output_dir = tempfile.TemporaryDirectory()
            tmp_output_dir.cleanup()
            os.makedirs(tmp_output_dir.name, exist_ok=True)
            output_dirpath = tmp_output_dir.name
        output_dirpath = Path(output_dirpath)
        for i, (s, e) in enumerate(zip(start_stamps, end_stamps)):
            start_frame = int(math.ceil(s * fps))
            end_frame = int(math.ceil(e * fps))
            output_paths.append(output_dirpath
                                / filename_tmpl.format(
                                    start_frame=start_frame,
                                    end_frame=end_frame))
    if parallel_process is False:
        for i, (s, e, video_out) in tqdm(enumerate(zip(
                start_stamps, end_stamps, output_paths)),
                                         total=len(output_paths),
                                         disable=show_progress is False):
            split_video(video_file_path, video_out, start_time=s, end_time=e,
                        hflip=hflip, vflip=vflip)
    else:
        cpu_count = multiprocessing.cpu_count()
        if n_jobs == -1 or n_jobs == 'full':
            n_jobs = min(cpu_count, len(output_paths))
        elif n_jobs == 'half':
            n_jobs = min(cpu_count // 2, len(output_paths))
        p = Pool(n_jobs)
        for i, (s, e, video_out) in enumerate(zip(
                start_stamps, end_stamps, output_paths)):
            p.apply_async(split_video,
                          args=(video_file_path, video_out, s, e,
                                hflip, vflip))
        p.close()
        p.join()
    return output_paths


def extract_target_frame_from_timestamp(video_filepath, timestamp):
    """Extract target frame from timestamp.

    Parameters
    ----------
    video_filepath : str
        video filepath
    timestamp : float
        timestamp in seconds.

    Returns
    -------
    image : numppy.ndarray
    """
    duration = get_video_duration(video_filepath)
    timestamp = max(0.0, min(duration, timestamp))
    vidcap = cv2.VideoCapture(str(video_filepath))
    vidcap.set(cv2.CAP_PROP_POS_MSEC, int(timestamp * 1000))
    success, image = vidcap.read()
    return image


def calc_frame_to_second_coefficient(duration, n_frame, sampling_sec=None):
    """Calculate Frame to Second coefficient.

    Parameters
    ----------
    duration : float
        video duration
    n_frame : int
        number of frame
    sampling_sec : float
        time of sampling seconds

    Returns
    -------
    frame_to_second : float
        calculated frame to second coefficient.

    Examples
    --------
    >>> calc_frame_to_second_coefficient(30, 60, sampling_sec=0.1)
    0.5
    >>> calc_frame_to_second_coefficient(30, 60, sampling_sec=0.1) * 3
    1.5
    """
    duration = float(duration)
    n_frame = float(n_frame)
    fps = n_frame / duration
    if sampling_sec is not None:
        return duration * math.ceil(fps * sampling_sec) / n_frame
    else:
        return duration / n_frame


def calc_second_to_frame_coefficient(duration, n_frame, sampling_sec=None):
    """Calculate Second to Frame coefficient.

    This is inverse of calc_frame_to_second_coefficient.

    Parameters
    ----------
    duration : float
        video duration
    n_frame : int
        number of frame
    sampling_sec : float
        time of sampling seconds

    Returns
    -------
    second_to_frame : float
        calculated second to frame coefficient.

    Examples
    --------
    >>> calc_second_to_frame_coefficient(30, 60, sampling_sec=0.1)
    2.0
    >>> int(1.99 * calc_second_to_frame_coefficient(4, 4))
    1
    >>> int(1.99 * calc_second_to_frame_coefficient(4, 4, sampling_sec=2.0))
    0
    """
    return 1.0 / calc_frame_to_second_coefficient(
        duration, n_frame, sampling_sec)


def load_frame(video_path, start=0.0, duration=-1,
               target_size=None, sampling_frequency=None):
    """Load frame

    Parameters
    ----------
    video_path : str or pathlib.Path
        input video path.
    start : float
        start time
    duration : int or float
        duration. If this value is `-1`, load all frames.

    Returns
    -------
    frames : list[numpy.ndarray]
        all frames.
    stamps : list[float]
        time stamps.
    """
    video_path = str(video_path)
    vid = cv2.VideoCapture(video_path)
    fps = vid.get(cv2.CAP_PROP_FPS)
    vid.set(cv2.CAP_PROP_POS_MSEC, start)
    vid_avail = True
    if sampling_frequency is not None:
        frame_interval = int(math.ceil(fps * sampling_frequency))
    else:
        frame_interval = 1
    cur_frame = 0
    while True:
        stamp = float(cur_frame) / fps
        vid_avail, frame = vid.read()
        if not vid_avail:
            break
        if duration != -1 and stamp > start + duration:
            break
        if target_size is not None:
            frame = cv2.resize(frame, target_size)
        yield frame, stamp
        cur_frame += frame_interval
        vid.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
    vid.release()


def count_frames(video_path, start=0.0, duration=-1,
                 sampling_frequency=None):
    video_duration = get_video_duration(video_path)
    video_duration -= start
    if duration > 0:
        video_duration = max(video_duration - duration, 0)
    fps = get_video_avg_frame_rate(video_path)
    if sampling_frequency is not None:
        return int(math.ceil(
            video_duration * fps
            / int(math.ceil(fps * sampling_frequency))))
    else:
        return int(math.ceil(video_duration * fps))


def video2fileframes(
        video_path,
        output_path=None,
        filename_tmpl='img_{:05}.jpg'):
    if output_path is None:
        tmp_output_dir = tempfile.TemporaryDirectory()
        tmp_output_dir.cleanup()
        os.makedirs(tmp_output_dir.name, exist_ok=True)
        output_path = tmp_output_dir.name
    output_path = Path(output_path)
    outfiles = []
    timestamps = []
    for i, (frame, stamp) in enumerate(
            load_frame(video_path), 0):
        outfile = output_path / filename_tmpl.format(i)
        cv2.imwrite(str(outfile), frame)
        outfiles.append(outfile)
        timestamps.append(stamp)
    return outfiles, timestamps


def split_video_to_fileframe_from_sections(
        outfiles, timestamps, start_stamps, end_stamps,
        output_path=None,
        filename_tmpl='img_{:05}.jpg',
        dirname_tmpl='frames_{:05}-{:05}'):
    if output_path is None:
        tmp_output_dir = tempfile.TemporaryDirectory()
        tmp_output_dir.cleanup()
        os.makedirs(tmp_output_dir.name, exist_ok=True)
        output_path = tmp_output_dir.name
    output_path = Path(output_path)
    output_frame_parent_paths = []
    for start_stamp, end_stamp in zip(start_stamps, end_stamps):
        start = get_timestamp_indices_wrt_base(timestamps, start_stamp)
        end = get_timestamp_indices_wrt_base(timestamps, end_stamp)
        frame_outpath = output_path / filename_tmpl.format(start, end)
        os.makedirs(str(frame_outpath), exist_ok=True)
        for i, filename in enumerate(outfiles[start:end]):
            filename = Path(filename)
            shutil.copy(filename, frame_outpath / filename_tmpl.format(i))
        output_frame_parent_paths.append(frame_outpath)
    return output_frame_parent_paths
