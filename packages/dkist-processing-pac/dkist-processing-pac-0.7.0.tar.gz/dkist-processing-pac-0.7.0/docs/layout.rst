Library Layout
==============

Components
----------

This library contains everything needed to compute demodulation matrices. It has 4 main parts:

+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Description                                                 | Code Thing                                                               |
+=============================================================+==========================================================================+
| A container for input data, :math:`\vec{I}_{obs}`           | `~dkist_processing_pac.input_data` package,                              |
|                                                             | specifically the                                                         |
|                                                             | `~dkist_processing_pac.input_data.dresser.Dresser`                       |
|                                                             | object                                                                   |
+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Parameterized Mueller matrices for optical elements         | the `~dkist_processing_pac.optics` package                               |
+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Objects to manage fitting parameters                        | `~dkist_processing_pac.fitter.fitter_parameters`                         |
| during fits and to return the final results                 | module, specifically the                                                 |
|                                                             | `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` |
|                                                             | object                                                                   |
+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Process to collect all the pieces and actually run the fits | the `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` object     |
+-------------------------------------------------------------+--------------------------------------------------------------------------+

Let's take a look at each one:

Input Data
**********

The Dresser contains :math:`\vec{I}_{obs}` for every bin provided by the instrument pipeline. See SPEC-0213 for more detailed definitions.
In addition to containing the actual measured intensities, this object also contains information about the geometry of
the telescope (needed for computing :math:`\mathbf{M}_{12}` and :math:`\mathbf{M}_{36}`) and the configuration of the
Calibration Unit (needed for computing :math:`\mathbf{C}`).

Optics
******

The Telescope object contains the machinery necessary to compute :math:`\mathbf{M}_{12}` and :math:`\mathbf{M}_{36}`.
The actual matrices are accessed via the `Telescope.TM <dkist_processing_pac.optics.telescope.Telescope.TM>` property.
It can also compute the inverse telescope matrix via the
`Telescope.generate_inverse_telescope_model <dkist_processing_pac.optics.telescope.Telescope.generate_inverse_telescope_model>` method.

The `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit` object contains the machinery necessary to compute
:math:`\mathbf{C}`, which is accessed via the `CalibrationUnit.CM <dkist_processing_pac.optics.calibration_unit.CalibrationUnit.CM>` property.

Parameters
**********

`~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` contains fitting parameters for every bin
provided by the instrument pipeline. There is a 1-to-1-to-1 mapping between a single :math:`\vec{I}_{obs}`, a single
set of fitting parameters, and a single fit result. To store the multiple `lmfit.Parameter` objects,
`~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` uses the custom `~dkist_processing_pac.fitter.fitter_parameters.NdParameterArray`.

Fitter
******

The `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` is the main interface between `dkist-processing-pac` and
instrument pipelines. It ingests a `~dkist_processing_pac.input_data.dresser.Dresser` prepared by the instrument and uses it to initialize
`~dkist_processing_pac.optics.telescope.Telescope`, `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit`,
and `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters`. It then uses all of these objects to fit
a modulation matrix for each in the Dresser.

Tying It All Together
---------------------

#. The instrument processes the PolCal files in whatever way is needed. These processed files are then organized into a
   dictionary with type ``Dict[int, List[FitsAccess]]``. The key is the CS step number and the value is a list of
   `FitsAccess` objects, each one corresponding to a single modulator state.
#. The instrument uses that dictionary to construct a `~dkist_processing_pac.input_data.dresser.Dresser`.
#. A `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` is created with that `~dkist_processing_pac.input_data.dresser.Dresser` and the “fit mode” and “init set” parameters taken from the input dataset document.
#. As part of its `__init__ <dkist_processing_pac.fitter.polcal_fitter.PolcalFitter>`, the `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` does the following:
    a. Use the `~dkist_processing_pac.input_data.dresser.Dresser` to initialize `~dkist_processing_pac.optics.telescope.Telescope` and `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit` objects
    b. Use the `~dkist_processing_pac.input_data.dresser.Dresser`, fit mode, and init set parameters to load sensible starting values into a
       `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` object. This is where we set the “global” parameters for the :math:`\mathbf{C}` matrix.
    c. Use that loaded `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` object to populate the `~dkist_processing_pac.optics.telescope.Telescope` and `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit` objects with
       the configuration parameters not provided directly by the `~dkist_processing_pac.input_data.dresser.Dresser`.
    d. For each bin in the `~dkist_processing_pac.input_data.dresser.Dresser`:
        i. Initialize the non-global parameters that are specific to that single bin’s
        ii. Run the damn fit of :math:`\mathbf{O}` and :math:`\mathbf{C}`.
        iii. Save the results
#. Once all bins are fit the set of all demodulation matrices is available to the instrument pipeline via the
   `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter.demodulation_matrices` property.

