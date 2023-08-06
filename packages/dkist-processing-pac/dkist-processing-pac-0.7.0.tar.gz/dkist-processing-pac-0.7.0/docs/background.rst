Background
==========

An input Stokes vector that has traveled through DKIST down to the entrance of the Coude lab can be described as
:math:`\vec{S}_{coud\acute{e}} = \mathbf{M}_{36} \mathbf{M}_{12} \vec{S}_{in}`, where :math:`\mathbf{M}_{12}`
is a combination of the Mueller matrices for mirrors 1 and 2 (primary and secondary), and :math:`\mathbf{M}_{36}`,
is the same for mirrors 3 - 6. The reason for grouping them together like this will become clear later. Also note that
some rotation matrices have been omitted, but the general concept is correct.

Once light enters the Coude lab it bounces off a bunch of mirrors and goes through an instrument optic that is
constantly cycling through a series of different polarizing states. We call this the **modulator**, and those different
states the **modulation states**. After the modulator the light finally hits the CCD.

CCDs only measure intensity (Stokes I); they cannot directly measure the polarization state of light. So what we do is
measure the total intensity at each of the different modulation states and then use all of those different measurements
to solve for the input Stokes vector. In matrix math this looks like

.. math::

  \vec{I}_{obs} = \mathbf{O} \vec{S}_{coud\acute{e}}

where O is what we call the modulation matrix. The modulation matrix is Mx4, where M is the number of modulation states.
The result is that is a vector of length M; one measurement of intensity for each modulation state. If M is at least 4
then the equation above is perfectly constrained and can be solved using linear algebra. In practice most DKIST
instruments use M=8 (ViSP uses M=10) to over-constrain the problem and help reduce errors that arise from non-ideal
conditions.

So, to put the whole optical train together, the relationship between what is actually recorded, :math:`\vec{I}_{obs}`,
and what we want to know, :math:`\vec{S}_{in}`, is

.. math:: \vec{I}_{obs} = \mathbf{O}\ \mathbf{M}_{36}\ \mathbf{M}_{12} \vec{S}_{in}.
  :label: full

Fortunately we already know what :math:`\mathbf{M}_{12}` and :math:`\mathbf{M}_{36}` are because we measured them in a
lab, so if we know :math:`\mathbf{O}` then we’re set…

The Rol of PolCal Data
----------------------
…Unfortunately we don’t. We have a pretty damn good idea, but instruments change often enough that :math:`\mathbf{O}`
needs to be computed every time science data are acquired. To do this we take PolCal data. During this task type the
**Calibration Unit** (CU) is inserted in the GOS between mirrors 2 and 3. The CU has a bunch of optics that can change
the polarization state of light and these optics are inserted into the beam in a series of steps. The full set of different CU
configurations is called a **Calibration Sequence** (CS). The light path now looks like this:

.. math::
  \vec{I}_{obs, i} = \mathbf{O}\ \mathbf{M}_{36}\ \mathbf{C}_i\ \mathbf{M}_{12} \vec{S}_{in},

where :math:`\mathbf{C}_i` is the Mueller matrix of the CU at CS step *i*. The reason this helps us is that when taking
PolCal data we point the telescope at unpolarized light so we know what :math:`\vec{S}_{in}` is. We also know what
:math:`\mathbf{C}` is and thus we have everything we need to solve the equation for :math:`\mathbf{O}`!

(Note that we need the multiple CS steps because many of the CS configurations are degenerate with each other so we need
to sample a lot (~12) of different ones before we have enough to truly constrain the problem).

Important Note About Bins
*************************

In practice we actually fit :math:`\mathbf{C}` simultaneously with :math:`\mathbf{O}`. Like :math:`\mathbf{O}`, we
have a very good idea of what :math:`\mathbf{C}` should be, but it needs to be refined every time. When an instrument
pipeline provides input data they actually provide a bunch of :math:`\vec{I}_{obs}` values: one for each of their bins.
Thus we have to do a separate fit for each :math:`\vec{I}_{obs}` value. The :math:`\mathbf{C}` matrix, though, is
constant across all :math:`\vec{I}_{obs}` values because the Calibration Unit is the same for all bins.

Demodulation Matrices and Science Pipelines
-------------------------------------------

In equation :math:numref:`full` above  if we know :math:`\mathbf{O}` then we can solve for :math:`\vec{S}_{in}` given
:math:`\vec{I}_{obs}`. This is what the science pipelines do. That math looks like this:

.. math::

  \vec{S}_{in} = \mathbf{M}_{12}^{-1} \mathbf{M}_{36}^{-1} \mathbf{O}^{-1}\vec{I}_{obs},

where :math:`\mathbf{M}^{-1}` indicates the matrix inverse. We call the inverse of the modulation matrix the
**demodulation matrix**. `dkist-processing-pac` computes demodulation matrices. (It also computes the inverse of the
mirror matrices, but those are constant).