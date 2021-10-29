import os
import zipfile
from contextlib import closing
from io import BytesIO
from multiprocessing import Pool, Manager, cpu_count
from queue import Empty

import numpy as np
from pydicom import dicomio, datadict, errors

# tag names of default columns in the series list, this can be changed to pull out different tag names for columns
from DICOM.DicomFile import DicomFile
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


def loadDicomFiles(filenames, queue):
    """Load the Dicom files `filenames' and put an abbreviated tag->value map for each onto `queue'."""
    for filename in filenames:
        try:
            dcm = dicomio.read_file(filename, stop_before_pixels = True)
            tags = {t: dcm.get(t) for t in loadTags if t in dcm}
            queue.put((filename, tags))
        except errors.InvalidDicomError:
            pass


def loadDicomFile(filename):
    try:
        dicomFile = DicomFile(filename)
        return dicomFile
    except errors.InvalidDicomError:
        pass


def loadDicomDir(rootdir, statusfunc = lambda s, c, n: None, numprocs = None):
    """
    Load all the Dicom files from `rootdir' using `numprocs' number of processes. This will attempt to load each file
    found in `rootdir' and store from each file the tags defined in loadTags. The filenames and the loaded tags for
    Dicom files are stored in a DicomSeries object representing the acquisition series each file belongs to. The
    `statusfunc' callback is used to indicate loading status, taking as arguments a status string, count of loaded
    objects, and the total number to load. A status string of '' indicates loading is done. The default value causes
    no status indication to be made. Return value is a sequence of DicomSeries objects in no particular order.
    """
    allfiles = []
    for root, _, files in os.walk(rootdir):
        allfiles += [os.path.join(root, f) for f in files if f.lower() != "dicomdir"]

    numprocs = numprocs or cpu_count()
    m = Manager()
    queue = m.Queue()
    numfiles = len(allfiles)
    res = []
    series = {}
    count = 0

    if not numfiles:
        return []

    with closing(Pool(processes = numprocs)) as pool:
        for filesec in np.array_split(allfiles, numprocs):
            res.append(pool.apply_async(loadDicomFiles, (filesec, queue)))

        # loop so long as any process is busy or there are files on the queue to process
        while any(not r.ready() for r in res) or not queue.empty():
            try:
                filename, dcm = queue.get(False)
                seriesid = dcm.get("SeriesInstanceUID", "???")
                if seriesid not in series:
                    series[seriesid] = DicomSeries(seriesid, rootdir)

                series[seriesid].addFile(filename, dcm)
            except Empty:  # from queue.get(), keep trying so long as the loop condition is true
                pass

            count += 1
            # update status only 100 times, doing it too frequently really slows things down
            if numfiles < 100 or count % (numfiles // 100) == 0:
                statusfunc("Loading DICOM files", count, numfiles)

    for seri in series:
        series[seri].sortSeries()

    statusfunc("", 0, 0)
    # all the built dicomSeries object are returned as a list
    return list(series.values())


def loadDicomZip(filename, statusfunc = lambda s, c, n: None):
    """
    Load Dicom images from given zip file `filename'. This uses the status callback `statusfunc' like loadDicomDir().
    Loaded files will have their pixel data thus avoiding the need to reload the zip file when an image is viewed but is
    at the expense of load time and memory. Return value is a sequence of DicomSeries objects in no particular order.
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
                s.tagCache[len(s.filenames) - 1] = dcm
                s.imgCache[len(s.filenames) - 1] = img

            count += 1
            # update status only 100 times, doing it too frequently really slows things down
            if numfiles < 100 or count % (numfiles // 100) == 0:
                statusfunc("Loading DICOM files", count, numfiles)

    statusfunc("", 0, 0)

    return list(series.values())
