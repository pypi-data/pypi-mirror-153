from ..imports import *
from .readers import *
from .writers import *


class Rainbow:
    """
    Rainbow objects represent the flux of some astrophysical
    object as a function of both wavelength and time.

    The general stucture of a Rainbow object contains a
    1D array of wavelengths, a 1D array of times, and a
    2D array of flux values (with row as wavelength and
    column as time).
    """

    # all Rainbows must contain these core dictionaries
    _core_dictionaries = ["fluxlike", "timelike", "wavelike", "metadata"]

    # define which axis is which
    waveaxis = 0
    timeaxis = 1

    def __init__(
        self,
        filepath=None,
        format=None,
        wavelength=None,
        time=None,
        flux=None,
        uncertainty=None,
        wavelike=None,
        timelike=None,
        fluxlike=None,
        metadata=None,
        **kw,
    ):
        """
        Initialize a Rainbow object from a file, from arrays
        with appropriate units, or from dictionaries with
        appropriate ingredients.

        Parameters
        ----------

        filepath : str
            The filepath pointing to the file or group of files
            that should be read.
        format : str
            The file format of the file to be read. If None,
            the format will be guessed automatically from the
            filepath.

        wavelength : astropy.unit.Quantity
            A 1D array of wavelengths, in any unit.
        time : astropy.unit.Quantity or astropy.unit.Time
            A 1D array of times, in any unit.
        flux : np.array
            A 2D array of flux values.
        uncertainty : np.array
            A 2D array of uncertainties, associated with the flux.

        wavelike : dict
            A dictionary containing 1D arrays with the same
            shape as the wavelength axis. It must at least
            contain the key 'wavelength', which should have
            astropy units of wavelength associated with it.
        timelike : dict
            A dictionary containing 1D arrays with the same
            shape as the time axis. It must at least
            contain the key 'time', which should have
            astropy units of time associated with it.
        fluxlike : dict
            A dictionary containing 2D arrays with the shape
            of (nwave, ntime), like flux. It must at least
            contain the key 'flux'.
        metadata : dict
            A dictionary containing all other metadata
            associated with the dataset, generally lots of
            individual parameters or comments.
        kw : dict
            Additional keywords will be passed along to
            the function that initializes the rainbow.
            If initializing from arrays (`time=`, `wavelength=`,
            ...), these keywords will be interpreted as
            additional arrays that should be sorted by their
            shape into the appropriate dictionary. If
            initializing from files, the keywords will
            be passed on to the reader.

        Examples
        --------
        ```
        # initalize from a file
        r1 = Rainbow('my-neat-file.abc', format='abcdefgh')

        # initalize from arrays
        r2 = Rainbow(wavelength=np.linspace(1, 5, 50)*u.micron,
                     time=np.linspace(-0.5, 0.5, 100)*u.day,
                     flux=np.random.normal(0, 1, (50, 100)))

        # initialize from dictionaries
        f3 = Rainbow(wavelike=dict(wavelength=np.linspace(1, 5, 50)*u.micron),
                     timelike=dict(time=np.linspace(-0.5, 0.5, 100)*u.day),
                     fluxlike=dict(flux=np.random.normal(0, 1, (50, 100))))

        """
        # metadata are arbitrary types of information we need
        self.metadata = {}

        # wavelike quanities are 1D arrays with nwave elements
        self.wavelike = {}

        # timelike quantities are 1D arrays with ntime elements
        self.timelike = {}

        # fluxlike quantities are 2D arrays with nwave x time elements
        self.fluxlike = {}

        # try to intialize from the exact dictionaries needed
        if (
            (type(wavelike) == dict)
            and (type(timelike) == dict)
            and (type(fluxlike) == dict)
        ):
            self._initialize_from_dictionaries(
                wavelike=wavelike,
                timelike=timelike,
                fluxlike=fluxlike,
                metadata=metadata,
            )
        # then try to initialize from arrays
        elif (wavelength is not None) and (time is not None) and (flux is not None):
            self._initialize_from_arrays(
                wavelength=wavelength,
                time=time,
                flux=flux,
                uncertainty=uncertainty,
                **kw,
            )
            if metadata is not None:
                self.metadata.update(**metadata)
        # then try to initialize from a file
        elif (type(filepath) == str) or (type(filepath) == list):
            self._initialize_from_file(filepath=filepath, format=format, **kw)

        # finally, tidy up by guessing the wavelength scale
        self._guess_wscale()

    def _validate_uncertainties(self):
        """
        Do some checks on the uncertainty values.
        """
        if self.uncertainty is None and len(self.fluxlike) > 0:
            message = f"""
            Hmmm...it's not clear which column corresponds to the
            flux uncertainties for this Rainbow object. The
            available `fluxlike` columns are:
                {self.fluxlike.keys()}
            A long-term solution might be to fix the `from_x1dints`
            reader, but a short-term solution would be to pick one
            of the columns listed above and say something like

            x.fluxlike['uncertainty'] = x.fluxlike['some-other-relevant-error-column']

            where `x` is the Rainbow you just created.
            """
            warnings.warn(message)
            return

        # kludge to replace zero uncertainties
        if np.all(self.uncertainty == 0):
            warnings.warn("\nUncertainties were all 0, replacing them with 1!")
            self.fluxlike["uncertainty"] = np.ones_like(self.flux)

    def save(self, filepath="test.rainbow.npy", format=None, **kw):
        """
        Save this Rainbow out to a file.

        Parameters
        ----------
        filepath : str
            The filepath pointing to the file to be written.
            (For now, it needs a `.rainbow.npy` extension.)
        format : str
            The file format of the file to be written. If None,
            the format will be guessed automatically from the
            filepath."""

        # figure out the best writer
        writer = guess_writer(filepath, format=format)

        # use that writer to save the file
        writer(self, filepath, **kw)

    def _initialize_from_dictionaries(
        self, wavelike={}, timelike={}, fluxlike={}, metadata={}
    ):
        """
        Populate from dictionaries in the correct format.

        Parameters
        ----------
        wavelike : dict
            A dictionary containing 1D arrays with the same
            shape as the wavelength axis. It must at least
            contain the key 'wavelength', which should have
            astropy units of wavelength associated with it.
        timelike : dict
            A dictionary containing 1D arrays with the same
            shape as the time axis. It must at least
            contain the key 'time', which should have
            astropy units of time associated with it.
        fluxlike : dict
            A dictionary containing 2D arrays with the shape
            of (nwave, ntime), like flux. It must at least
            contain the key 'flux'.
        metadata : dict
            A dictionary containing all other metadata
            associated with the dataset, generally lots of
            individual parameters or comments.
        """

        # update the four core dictionaries
        self.wavelike.update(**wavelike)
        self.timelike.update(**timelike)
        self.fluxlike.update(**fluxlike)
        self.metadata.update(**metadata)

        # validate that something reasonable got populated
        self._validate_core_dictionaries()

    def _get_core_dictionaries(self):
        """
        Get the core dictionaries of this Rainbow.

        Returns
        -------
        core : dict
            Dictionary containing the keys
            ['wavelike', 'timelike', 'fluxlike', 'metadata']
        """
        return {k: vars(self)[k] for k in self._core_dictionaries}

    def _initialize_from_arrays(
        self, wavelength=None, time=None, flux=None, uncertainty=None, **kw
    ):
        """
        Populate from arrays.

        Parameters
        ----------
        wavelength : astropy.unit.Quantity
            A 1D array of wavelengths, in any unit.
        time : astropy.unit.Quantity or astropy.unit.Time
            A 1D array of times, in any unit.
        flux : np.array
            A 2D array of flux values.
        uncertainty : np.array
            A 2D array of uncertainties, associated with the flux.
        kw : dict
            Additional keywords will be interpreted as arrays
            that should be sorted into the appropriate location
            based on their size.
        """

        # store the wavelength
        self.wavelike["wavelength"] = wavelength

        # store the time
        self.timelike["time"] = time

        # store the flux and uncertainty
        self.fluxlike["flux"] = flux
        self.fluxlike["uncertainty"] = uncertainty

        # sort other arrays by shape
        for k, v in kw.items():
            self._put_array_in_right_dictionary(k, v)

        # validate that something reasonable got populated
        self._validate_core_dictionaries()

    def _put_array_in_right_dictionary(self, k, v):
        """
        Sort an input into the right core dictionary
        (timelike, wavelike, fluxlike) based on its shape.

        Parameters
        ----------
        k : str
            The key for the (appropriate) dictionary.
        v : np.array
            The quantity to sort.
        """
        if np.shape(v) == self.shape:
            self.fluxlike[k] = v
        elif np.shape(v) == (self.nwave,):
            self.wavelike[k] = v
        elif np.shape(v) == (self.ntime,):
            self.timelike[k] = v
        else:
            raise ValueError("'{k}' doesn't fit anywhere!")

    def _initialize_from_file(self, filepath=None, format=None, **kw):
        """
        Populate from a filename or group of files.

        Parameters
        ----------

        filepath : str
            The filepath pointing to the file or group of files
            that should be read.
        format : str
            The file format of the file to be read. If None,
            the format will be guessed automatically from the
            filepath.
        kw : dict
            Additional keywords will be passed on to the reader.
        """

        # make sure we're dealing with a real filename
        assert filepath is not None

        # pick the appropriate reader
        reader = guess_reader(filepath=filepath, format=format)
        reader(self, filepath, **kw)

        # validate that something reasonable got populated
        self._validate_core_dictionaries()
        self._validate_uncertainties()

    def _create_copy(self):
        """
        Create a copy of self, with the core dictionaries copied.
        """
        new = type(self)()
        new._initialize_from_dictionaries(
            **copy.deepcopy(self._get_core_dictionaries())
        )
        return new

    def _guess_wscale(self, relative_tolerance=0.05):
        """
        Try to guess the wscale from the wavelengths.

        Parameters
        ----------

        relative_tolerance : float
            The fractional difference to which the differences
            between wavelengths should match in order for a
            linear or logarithmic wavelength scale to be
            assigned. For example, the default value of 0.01
            means that the differences between all wavelength
            must be within 1% of each other for the wavelength
            scale to be called linear.
        """

        # give up if there's no wavelength array
        if self.wavelength is None:
            return "?"

        # calculate difference arrays
        w = self.wavelength.value
        dw = np.diff(w)
        dlogw = np.diff(np.log(w))

        # test the three options
        if np.allclose(dw, np.median(dw), rtol=relative_tolerance):
            self.metadata["wscale"] = "linear"
        elif np.allclose(dlogw, np.median(dlogw), rtol=relative_tolerance):
            self.metadata["wscale"] = "log"
        else:
            self.metadata["wscale"] = "?"

    def _guess_tscale(self, relative_tolerance=0.01):
        """
        Try to guess the tscale from the times.

        Parameters
        ----------

        relative_tolerance : float
            The fractional difference to which the differences
            between times should match in order for us to call
            the times effectively uniform, or for us to treat
            them more carefully as an irregular or gappy grid.
        """

        # give up if there's no time array
        if self.time is None:
            return "?"

        # calculate difference arrays
        t = self.time.value
        dt = np.diff(t)

        # test the three options
        if np.allclose(dt, np.median(dt), rtol=relative_tolerance):
            self.metadata["tscale"] = "uniform"
        else:
            self.metadata["tscale"] = "?"

    @property
    def wavelength(self):
        """
        The 1D array of wavelengths (with astropy units of length).
        """
        return self.wavelike.get("wavelength", None)

    @wavelength.setter
    def wavelength(self, value):
        """
        The 1D array of wavelengths (with astropy units of length).
        """
        self.wavelike["wavelength"] = value
        self._validate_core_dictionaries()

    @property
    def time(self):
        """
        The 1D array of time (with astropy units of time).
        """
        return self.timelike.get("time", None)

    @property
    def flux(self):
        """
        The 2D array of fluxes (row = wavelength, col = time).
        """
        return self.fluxlike.get("flux", None)

    @property
    def uncertainty(self):
        """
        The 2D array of uncertainties on the fluxes.
        """
        return self.fluxlike.get("uncertainty", None)

    @property
    def ok(self):
        """
        The 2D array of whether data is OK (row = wavelength, col = time).
        """
        return self.fluxlike.get("ok", np.ones_like(self.flux).astype(bool))

    @ok.setter
    def ok(self, value):
        """
        The 2D array of whether data is OK (row = wavelength, col = time).
        """
        self.fluxlike["ok"] = value
        if value is not None:
            assert np.shape(value) == self.shape

    def __getattr__(self, key):
        """
        If an attribute/method isn't explicitly defined,
        try to pull it from one of the core dictionaries.

        Let's say you want to get the 2D uncertainty array
        but don't want to type `self.fluxlike['uncertainty']`.
        You could instead type `self.uncertainty`, and this
        would try to search through the four standard
        dictionaries to pull out the first `uncertainty`
        it finds.

        Parameters
        ----------
        key : str
            The attribute we're trying to get.
        """
        if key not in self._core_dictionaries:
            for dictionary_name in self._core_dictionaries:
                try:
                    return self.__dict__[dictionary_name][key]
                except KeyError:
                    pass
        message = f"🌈.{key} does not exist for this Rainbow"
        raise AttributeError(message)

    def __setattr__(self, key, value):
        """
        When setting a new attribute, try to sort it into the
        appropriate core directory based on its size.

        Let's say you have some quantity that has the same
        shape as the wavelength array and you'd like to attach
        it to this Rainbow object. This will try to save it
        in the most relevant core dictionary (of the choices
        timelike, wavelike, fluxlike).

        Parameters
        ----------
        key : str
            The attribute we're trying to get.
        value : np.array
            The quantity we're trying to attach to that name.
        """
        try:
            if key in self._core_dictionaries:
                raise ValueError("Trying to set a core dictionary.")
            elif key == "wavelength":
                self.wavelike["wavelength"] = value
                self._validate_core_dictionaries()
            elif key == "time":
                self.timelike["time"] = value
                self._validate_core_dictionaries()
            elif key in ["flux", "uncertainty", "ok"]:
                self.fluxlike[key] = value
                self._validate_core_dictionaries()
            else:
                self._put_array_in_right_dictionary(key, value)
        except ValueError:
            self.__dict__[key] = value

    @property
    def _nametag(self):
        """
        This short phrase will preface everything
        said with `self.speak()`.
        """
        return f"🌈({self.nwave}w, {self.ntime}t)"

    @property
    def shape(self):
        """
        The shape of the flux array (nwave, ntime).
        """
        return (self.nwave, self.ntime)

    @property
    def nwave(self):
        """
        The number of wavelengths.
        """
        if self.wavelength is None:
            return 0
        else:
            return len(self.wavelength)

    @property
    def ntime(self):
        """
        The number of times.
        """
        if self.time is None:
            return 0
        else:
            return len(self.time)

    @property
    def nflux(self):
        """
        The total number of fluxes.
        """
        return np.prod(self.shape)

    def is_ok(self):
        """
        Create a flux-like array indicating which data are OK,
        meaning they are both finite and not marked somewhere
        ask being bad.

        Returns
        -------
        ok : boolean array
            Fluxlike array of Trues and Falses indicating
            which data entries are OK.
        """

        ok = np.isfinite(self.flux)
        try:
            ok *= self.fluxlike["ok"]
        except KeyError:
            pass
        return ok

    def _validate_core_dictionaries(self):
        """
        Do some simple checks to make sure this Rainbow
        is populated with the minimal data needed to do anything.
        It shouldn't be run before the Rainbow is fully
        initialized; otherwise, it might complain about
        a half-populated object.
        """

        # make sure there are some times + wavelengths defined
        if self.ntime is None:
            warnings.warn(
                f"""
            No times are defined for this Rainbow.
            """
            )
        if self.nwave is None:
            warnings.warn(
                f"""
            No wavelengths are defined for this Rainbow.
            """
            )

        # does the flux have the right shape?
        if self.shape != self.flux.shape:
            message = f"""
            Something doesn't line up!
            The flux array has a shape of {self.flux.shape}.
            The wavelength array has {self.nwave} wavelengths.
            The time array has {self.ntime} times.
            """
            if self.shape == self.flux.shape[::-1]:
                warnings.warn(
                    f"""{message}
                    Any chance your flux array is transposed?
                    """
                )
            else:
                warnings.warn(message)

        for n in ["uncertainty", "ok"]:
            x = getattr(self, n)
            if x is not None:
                if x.shape != self.flux.shape:
                    message = f"""
                    Watch out! The '{n}' array has
                    a shape of {x.shape}, which doesn't match the
                    flux array's shape of {self.flux.shape}.
                    """
                    warnings.warn(message)

    def __getitem__(self, key):
        """
        Trim a rainbow by indexing, slicing, or masking.
        Two indices must be provided (`[:,:]`).

        Examples
        --------
        ```
        r[:,:]
        r[10:20, :]
        r[np.arange(10,20), :]
        r[r.wavelength > 1*u.micron, :]
        r[:, np.abs(r.time) < 1*u.hour]
        r[r.wavelength > 1*u.micron, np.abs(r.time) < 1*u.hour]
        ```

        Parameters
        ----------
        key : tuple
            The (wavelength, time) slices, indices, or masks.
        """

        i_wavelength, i_time = key

        # create a copy
        new = self._create_copy()

        # do indexing of wavelike
        for w in self.wavelike:
            new.wavelike[w] = self.wavelike[w][i_wavelength]

        # do indexing of timelike
        for t in self.timelike:
            new.timelike[t] = self.timelike[t][i_time]

        # do indexing of fluxlike
        for f in self.fluxlike:
            # (indexing step by step seems more stable)
            if self.fluxlike[f] is None:
                continue
            temporary = self.fluxlike[f][i_wavelength, :]
            new.fluxlike[f] = temporary[:, i_time]

        # finalize the new rainbow
        new._validate_core_dictionaries()
        new._guess_wscale()

        return new

    def __repr__(self):
        """
        How should this object be represented as a string?
        """
        n = self.__class__.__name__.replace("Rainbow", "🌈")
        return f"<{n}({self.nwave}w, {self.ntime}t)>"

    def help(self, categories=["actions", "visualizations", "wavelike_summaries"]):
        """
        Provide a quick reference of key actions available for this Rainbow.

        Parameters
        ----------

        """
        print(
            textwrap.dedent(
                """
        Hooray for you! You asked for help on what you can do
        with this 🌈 object. Here's a quick reference of a few
        available options for things to try."""
            )
        )

        base_directory = pkg_resources.resource_filename("chromatic", "rainbows")
        for c in categories:
            print(
                "\n"
                + "-" * (len(c) + 4)
                + "\n"
                + f"| {c} |\n"
                + "-" * (len(c) + 4)
                + "\n"
            )
            directory = os.path.join(base_directory, c)
            descriptions_file = os.path.join(directory, "descriptions.txt")
            table = ascii.read(descriptions_file)
            for row in table:
                if row["name"] in "+-*/":
                    function_call = f"{row['name']}"
                else:
                    function_call = f".{row['name']}()"

                item = (
                    f"{row['cartoon']} | {function_call:<28} \n   {row['description']}"
                )
                print(item)

    # import the basic operations for Rainbows
    from .actions.operations import __add__, __sub__, __mul__, __truediv__, __eq__

    # import other actions that return other Rainbows
    from .actions import (
        normalize,
        bin,
        bin_in_time,
        bin_in_wavelength,
        trim,
        trim_nan_times,
        trim_nan_wavelengths,
        _create_shared_wavelength_axis,
        align_wavelengths,
        to_nparray,
        to_df,
    )

    # import summary statistics for each wavelength
    from .wavelike_summaries import (
        get_spectrum,
        get_spectral_resolution,
        get_typical_uncertainty,
    )

    # import visualizations that can act on Rainbows
    from .visualizations import (
        imshow,
        plot,
        _setup_animate_lightcurves,
        animate_lightcurves,
        _setup_animate_spectra,
        animate_spectra,
        _setup_animated_scatter,
        _setup_wavelength_colors,
        _make_sure_cmap_is_defined,
        get_wavelength_color,
        imshow_quantities,
        plot_quantities,
        imshow_interact,
    )
