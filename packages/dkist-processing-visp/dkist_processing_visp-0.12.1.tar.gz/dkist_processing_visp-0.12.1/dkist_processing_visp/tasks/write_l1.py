"""Visp write L1 task."""
import logging
import uuid
from typing import Literal

import numpy as np
from astropy.io import fits
from astropy.time import Time
from dkist_processing_common.tasks import WriteL1Frame

from dkist_processing_visp.models.constants import VispConstants


class VispWriteL1Frame(WriteL1Frame):
    """
    Task class for writing out calibrated l1 ViSP frames.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs
    """

    @property
    def constants_model_class(self):
        """Get Visp pipeline constants."""
        return VispConstants

    def add_dataset_headers(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]
    ) -> fits.Header:
        """
        Add the VISP specific dataset headers to L1 FITS files.

        Parameters
        ----------
        header : fits.Header
            calibrated data header

        stokes :
            stokes parameter

        Returns
        -------
        fits.Header
            calibrated header with correctly written l1 headers
        """
        if stokes.upper() not in self.constants.stokes_params:
            raise ValueError("The stokes parameter must be one of I, Q, U, V")
        # ---Spectral---
        header["DNAXIS1"] = header["NAXIS1"]
        header["DTYPE1"] = "SPECTRAL"
        header["DPNAME1"] = "dispersion axis"
        header["DWNAME1"] = "wavelength"
        header["DUNIT1"] = header["CUNIT1"]
        # ---Spatial 1---
        header["DNAXIS2"] = header["NAXIS2"]
        header["DTYPE2"] = "SPATIAL"
        header["DPNAME2"] = "spatial along slit"
        header["DWNAME2"] = "helioprojective latitude"
        header["DUNIT2"] = header["CUNIT2"]

        # ---Spatial 2---
        header["DNAXIS3"] = self.constants.num_raster_steps
        header["DTYPE3"] = "SPATIAL"
        header["DPNAME3"] = "raster scan step number"
        header["DWNAME3"] = "helioprojective longitude"
        header["DUNIT3"] = header["CUNIT3"]
        # Raster position in dataset
        header["DINDEX3"] = (
            header["VSPSTP"] + 1
        )  # Current position in raster scan which counts from zero

        # Set the base number of dataset axes to 3
        num_axis = 3

        # ---Temporal---
        if self.constants.num_map_scans > 1:
            num_axis += 1
            header[
                f"DNAXIS{num_axis}"
            ] = self.constants.num_map_scans  # total number of raster scans in the dataset
            header[f"DTYPE{num_axis}"] = "TEMPORAL"
            header[f"DPNAME{num_axis}"] = "time"
            header[f"DWNAME{num_axis}"] = "time"
            header[f"DUNIT{num_axis}"] = "s"
            # Temporal position in dataset
            header[f"DINDEX{num_axis}"] = header["VSPMAP"]  # Current raster scan

        # ---Stokes---
        if self.constants.correct_for_polarization:
            num_axis += 1
            header[f"DNAXIS{num_axis}"] = 4  # I, Q, U, V
            header[f"DTYPE{num_axis}"] = "STOKES"
            header[f"DPNAME{num_axis}"] = "polarization state"
            header[f"DWNAME{num_axis}"] = "polarization state"
            header[f"DUNIT{num_axis}"] = ""
            # Stokes position in dataset - stokes axis goes from 1-4
            header[f"DINDEX{num_axis}"] = self.constants.stokes_params.index(stokes.upper()) + 1

        else:
            logging.info("Spectrographic data detected. Not adding DNAXIS information.")

        header["DNAXIS"] = num_axis
        header["DAAXES"] = 2  # Spectral, spatial
        header["DEAXES"] = num_axis - 2  # Total - detector axes

        # VISP has a wavelength axis in the frame and so FRAMEWAV is hard to define. Use LINEWAV.
        header["LEVEL"] = 1
        header["WAVEBAND"] = self.constants.spectral_line
        header["WAVEUNIT"] = -9  # nanometers
        header["WAVEREF"] = "Air"
        # The wavemin and wavemax assume that all frames in a dataset have identical wavelength axes
        header["WAVEMIN"] = header["CRVAL1"] - (header["CRPIX1"] * header["CDELT1"])
        header["WAVEMAX"] = header["CRVAL1"] + (
            (header["NAXIS1"] - header["CRPIX1"]) * header["CDELT1"]
        )

        # Binning headers
        header["NBIN1"] = 1
        header["NBIN2"] = 1
        header["NBIN3"] = 1
        header["NBIN"] = header["NBIN1"] * header["NBIN2"] * header["NBIN3"]

        return header

    @staticmethod
    def _replace_header_values(header: fits.Header, data: np.ndarray) -> fits.Header:
        """
        Replace the FILE_ID and DATE keywords with new values.

        This is overloaded from dkist-processing-common because DATE-END is computed correctly in ScienceCalibration
        and the *-common version of this method would overwrite that key.
        """
        header["FILE_ID"] = uuid.uuid4().hex
        header["DATE"] = Time.now().fits
        # Remove BZERO and BSCALE as their value should be recalculated by astropy upon fits write
        header.pop("BZERO", None)
        header.pop("BSCALE", None)
        # Make sure that NAXIS is set to the shape of the data in case of squeezing
        header["NAXIS"] = len(data.shape)
        return header
