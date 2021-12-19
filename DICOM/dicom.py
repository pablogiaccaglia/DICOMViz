import os
import zipfile
from contextlib import closing
from io import BytesIO
from multiprocessing import Pool, Manager, cpu_count
from queue import Empty
from typing import Optional

import numpy as np
from pydicom import dicomio, datadict, errors

# tag names of default columns in the series list, this can be changed to pull out different tag names for columns
from DICOM.DicomFileWrapper import DicomFileWrapper
from DICOM.DicomSeries import DicomSeries

seriesListColumns = (
    "NumImages",
    "SeriesNumber",
    "PatientName",
    "SeriesInstanceUID",
    "SeriesDescription",
)

# names of columns in tag tree, this shouldn't ever change
tagTreeColumns = ("Name", "Tag", "Value")

# list of tags to initially load when a directory is scanned, loading only these speeds up scanning immensely
loadTags = (
    "SeriesInstanceUID",
    "TriggerTime",
    "PatientName",
    "SeriesDescription",
    "SeriesNumber",
)

# keyword/full name pairs for extra properties not represented as Dicom tags
extraKeywords = {
    "NumImages":    "# Images",
    "TimestepSpec": "Timestep Info",
    "StartTime":    "Start Time",
    "NumTimesteps": "# Timesteps",
    "TimeInterval": "Time Interval",
}

# maps keywords to their full names
keywordNameMap = {v[4]: v[2] for v in datadict.DicomDictionary.values()}
keywordNameMap.update(extraKeywords)

fullNameMap = {v: k for k, v in keywordNameMap.items()}  # maps full names to keywords


def loadDicomFiles(filenames, queue) -> None:
    """Load the Dicom files `filenames' and put an abbreviated tag->value map for each onto `queue'."""
    for filename in filenames:
        try:
            dcm = dicomio.read_file(filename, stop_before_pixels = True)
            tags = {t: dcm.get(t) for t in loadTags if t in dcm}
            queue.put((filename, tags))
        except errors.InvalidDicomError:
            pass


def loadDicomFile(filename) -> Optional[DicomFileWrapper]:
    try:
        dicomFile = DicomFileWrapper(filename)
        return dicomFile
    except errors.InvalidDicomError:
        pass


def loadDicomDir(rootDirectory, numberOfProcesses = None) -> list:

    allFiles = []
    for root, _, files in os.walk(rootDirectory):
        allFiles += [os.path.join(root, f) for f in files if f.lower() != "dicomdir"]

    numberOfProcesses = numberOfProcesses or cpu_count()
    m = Manager()
    queue = m.Queue()
    numFiles = len(allFiles)
    res = []
    dictOfSeries = {}

    if not numFiles:
        return []

    with closing(Pool(processes = numberOfProcesses)) as pool:

        for fileSequence in np.array_split(allFiles, numberOfProcesses):
            res.append(pool.apply_async(loadDicomFiles, (fileSequence, queue)))

        # loop so long as any process is busy or there are files on the queue to process
        while any(not r.ready() for r in res) or not queue.empty():
            try:
                filename, dcm = queue.get(False)
                seriesID = dcm.get("SeriesInstanceUID", "???")

                if seriesID not in dictOfSeries:
                    dictOfSeries[seriesID] = DicomSeries(seriesID, rootDirectory)

                dictOfSeries[seriesID].addFile(filename, dcm)

            except Empty:
                pass

    for seriesDictKey in dictOfSeries:
        dictOfSeries[seriesDictKey].sortSeries()
        pass

    # all the built dicomSeries object are returned as a list
    return list(dictOfSeries.values())


def loadDicomZip(filename) -> list:
    """
    Load Dicom images from given zip file `filename'.
    """
    series = {}
    count = 0

    with zipfile.ZipFile(filename) as z:
        names = z.namelist()
        numfiles = len(names)

        for n in names:
            nfilename = "%s?%s" % (filename, n)
            s = BytesIO(z.read(n))

            try:
                dcm = dicomio.read_file(s)
            except:
                pass  # ignore files which aren't Dicom files, various exceptions raised so no concise way to do this
            else:
                seriesid = dcm.get("SeriesInstanceUID", "???")

                if seriesid not in series:
                    series[seriesid] = DicomSeries(seriesid, nfilename)

                # need to load image data now since we don't want to reload the zip file later when an image is viewed
                try:  # attempt to create the image matrix, store None if this doesn't work
                    rslope = float(dcm.get("RescaleSlope", 1) or 1)
                    rinter = float(dcm.get("RescaleIntercept", 0) or 0)
                    img = dcm.pixel_array * rslope + rinter
                except:
                    img = None

                s = series[seriesid]
                s.addFile(nfilename, dcm)
                s._tagCache[len(s.sortedFileNamesList) - 1] = dcm
                s._imgCache[len(s.sortedFileNamesList) - 1] = img

            count += 1

    return list(series.values())
