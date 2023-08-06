import os
import subprocess

from . import LOG


def convert_markdown(report_file_path: str) -> bool:
    """Try to convert the markdown file to pdf or odt."""

    success = False
    if not os.path.isfile(report_file_path):
        LOG.warning(f"{report_file_path} is not a file. Aborting!")
        return success

    pdf_available = True
    try:
        subprocess.check_output(["pandoc", "--version"])
    except FileNotFoundError:
        # No pandoc available, therefore nothing else to do here.
        return False

    try:
        subprocess.check_output(
            [
                "pandoc",
                "--template",
                "eisvogel",
                "--listings",
                "-o",
                f"{report_file_path[:-3]}.pdf",
                report_file_path,
            ]
        )
        return True
    except FileNotFoundError as err:
        # Probably the template is not available
        LOG.debug(
            "Trying to use pandoc with template resulted in following error: "
            "%s",
            err,
        )

    except subprocess.CalledProcessError as err:
        # Probably no pdf engine installed
        LOG.debug("Trying to use pandoc resulted in following error: %s", err)
        pdf_available = False

    if pdf_available:
        try:
            subprocess.check_output(
                [
                    "pandoc",
                    "--listings",
                    "-o",
                    f"{report_file_path[:-3]}.pdf",
                    report_file_path,
                ]
            )
            return True
        except Exception as err:
            LOG.debug(
                "Trying to use pandoc resulted in following error: %s", err
            )

    try:
        subprocess.check_output(
            [
                "pandoc",
                "-s",
                "-t",
                "odt",
                "-o",
                f"{report_file_path[:-3]}.odt",
                report_file_path,
            ]
        )
        return True
    except Exception:
        pass

    LOG.warning(
        "Unable to convert markdown file. Check debug logs for more info."
    )
    return False
