"""Script to check that WAVE files fits a set of requirements."""

import argparse
import sys
import wave


def wavelint(
    filenames,
    nchannels=None,
    sample_width=None,
    frame_rate=None,
    nframes=None,
    compression_type=None,
    compression_name=None,
    max_duration=None,
    min_duration=None,
    quiet=False,
):
    """Check that a set of WAVE filenames fits some requirements.

    Parameters
    ----------

    filenames : list
      Set of file names to check.

    nchannels : int, optional
      Mandatory number of channels for the files. Use ``1`` if you
      want to assert that you are working with mono files, or whatever
      other number of channels for stereo files.

    sample_width : int, optional
      Number of bytes as size for sample width.

    frame_rate : int, optional
      Sampling frecuency, in Hz, that audio files must have .

    nframes : int, optional
      Number of frames that audio files must have.

    compression_type : str, optional
      Compression type that should have all audio files.

    compression_name : str, optional
      Name of the compression that should have all audio files.

    max_duration : float, optional
      Maximum duration in seconds that can have the files.

    min_duration : float, optional
      Minimum duration in seconds that can have the files.

    quiet : bool, optional
      Enabled, don't print output to stderr when a mismatch is found.

    Returns
    -------

    int: 0 if all files fits with arguments requirements, 1 otherwise.
    """
    exitcode = 0

    for filename in filenames:
        with wave.open(filename, "r") as f:

            if nchannels is not None:
                file_nchannels = f.getnchannels()
                if int(nchannels) != file_nchannels:
                    exitcode = 1
                    if not quiet:
                        sys.stderr.write(
                            f"Found {file_nchannels} channels ({nchannels}"
                            f" expected) at file {filename}\n"
                        )

            if sample_width is not None:
                file_sample_width = f.getsampwidth()
                if int(sample_width) != file_sample_width:
                    exitcode = 1
                    if not quiet:
                        sys.stderr.write(
                            f"Found sample width of {file_sample_width}"
                            f" ({sample_width} expected) at file {filename}\n"
                        )

            if frame_rate is not None:
                file_frame_rate = f.getframerate()
                if int(frame_rate) != file_frame_rate:
                    exitcode = 1
                    if not quiet:
                        sys.stderr.write(
                            f"Found frame rate of {file_frame_rate}"
                            f" ({frame_rate} expected) at file {filename}\n"
                        )

            if nframes is not None:
                file_nframes = f.getnframes()
                if int(nframes) != file_nframes:
                    exitcode = 1
                    if not quiet:
                        sys.stderr.write(
                            f"Found {file_nframes} number of frames"
                            f" ({nframes} expected) at file {filename}\n"
                        )

            if compression_type is not None:
                file_compression_type = f.getcomptype()
                if compression_type != file_compression_type:
                    exitcode = 1
                    if not quiet:
                        sys.stderr.write(
                            f"Found compression type '{file_compression_type}'"
                            f" ('{compression_type}' expected) at file"
                            f" {filename}\n"
                        )

            if compression_name is not None:
                file_compression_name = f.getcompname()
                if compression_name != file_compression_name:
                    exitcode = 1
                    if not quiet:
                        sys.stderr.write(
                            f"Found compression '{file_compression_name}'"
                            f" ('{compression_name}' expected) at file"
                            f" {filename}\n"
                        )

            if max_duration is not None or min_duration is not None:
                file_duration = round(f.getnframes() / f.getframerate(), 2)

            if max_duration is not None and max_duration < file_duration:
                exitcode = 1
                if not quiet:
                    sys.stderr.write(
                        f"Found greater duration ({float(file_duration)})"
                        f" than allowed ({float(max_duration)}) at file"
                        f" {filename}\n"
                    )

            if min_duration is not None and min_duration > file_duration:
                exitcode = 1
                if not quiet:
                    sys.stderr.write(
                        f"Found lower duration ({float(file_duration)})"
                        f" than allowed ({float(min_duration)}) at file"
                        f" {filename}\n"
                    )

    return exitcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="WAVE filenames to lint")
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    parser.add_argument(
        "-nchannels",
        "--nchannels",
        type=int,
        metavar="CHANNELS",
        required=False,
        default=None,
        dest="nchannels",
        help="Mandatory number of channels for the files.",
    )
    parser.add_argument(
        "-sample-width",
        "--sample-width",
        type=int,
        metavar="SAMPLE_WIDTH",
        required=False,
        default=None,
        dest="sample_width",
        help="Mandatory sample width in bytes for the files.",
    )
    parser.add_argument(
        "-frame-rate",
        "--frame-rate",
        type=int,
        metavar="FRAME_RATE",
        required=False,
        default=None,
        dest="frame_rate",
        help="Mandatory sampling frecuency, in Hz, for the files.",
    )
    parser.add_argument(
        "-nframes",
        "--nframes",
        type=int,
        metavar="NFRAMES",
        required=False,
        default=None,
        dest="nframes",
        help="Mandatory number of frames for the files.",
    )
    parser.add_argument(
        "-comptype",
        "--comptype",
        "-compression-type",
        "--compression-type",
        type=str,
        metavar="COMPTYPE",
        required=False,
        default=None,
        dest="compression_type",
        help="Mandatory compression type for the files.",
    )
    parser.add_argument(
        "-compname",
        "--compname",
        "-compression-name",
        "--compression-name",
        type=str,
        metavar="COMPNAME",
        required=False,
        default=None,
        dest="compression_name",
        help="Mandatory compression for the files.",
    )
    parser.add_argument(
        "-max-duration",
        "--max-duration",
        type=float,
        metavar="SECONDS",
        required=False,
        default=None,
        dest="max_duration",
        help="Maximum duration allowed for the files.",
    )
    parser.add_argument(
        "-min-duration",
        "--min-duration",
        type=float,
        metavar="SECONDS",
        required=False,
        default=None,
        dest="min_duration",
        help="Minimum duration allowed for the files.",
    )
    args = parser.parse_args()

    return wavelint(
        args.filenames,
        nchannels=args.nchannels,
        sample_width=args.sample_width,
        frame_rate=args.frame_rate,
        nframes=args.nframes,
        compression_type=args.compression_type,
        compression_name=args.compression_name,
        max_duration=args.max_duration,
        min_duration=args.min_duration,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    exit(main())
