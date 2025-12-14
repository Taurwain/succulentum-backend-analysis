import dash

from dashboard import styles, callbacks, layout, data_loader


class Dashboard:
    """
    A class to represent a dashboard application for succulent analytics using Dash.

    Attributes
    ----------
    app : dash.Dash or None
        The Dash application instance.
    plants_df : pandas.DataFrame or None
        DataFrame containing plant data.
    all_genera : list or None
        List of all genera available in the dataset.
    all_species : list or None
        List of all species available in the dataset.
    all_varieties : list or None
        List of all varieties available in the dataset.

    Methods
    -------
    initialize():
        Initializes the Dash application, loads data, and sets up the layout and callbacks.
    _load_data():
        Loads plant data and initializes filter options for genera, species, and varieties.
    _register_callbacks(initial_data):
        Registers callbacks for the Dash application.
    run(debug=True, port=8050):
        Runs the Dash application server.
    """
    def __init__(self):
        """
        Initializes the Dashboard class with default attributes set to None.
        """
        self.app = None
        self.plants_df = None
        self.all_genera = None
        self.all_species = None
        self.all_varieties = None

    def initialize(self):
        """
        Initializes the Dash application, loads data, and sets up the layout and callbacks.

        This method creates a Dash application instance, configures it, loads plant data,
        sets up the initial layout with filter options, and registers necessary callbacks.
        """
        self.app = dash.Dash(__name__, title='Succulentum Analytics')
        self.app.config.suppress_callback_exceptions = True

        self.app.index_string = styles.HTML_STYLES

        self._load_data()

        initial_data = self.plants_df.to_json(date_format='iso', orient='split')

        self.app.layout = layout.create_layout(
            self.all_genera,
            self.all_species,
            self.all_varieties,
            initial_data
        )

        callbacks.register_callbacks(self.app, self.plants_df, initial_data)

    def _load_data(self):
        """
        Loads plant data and initializes filter options for genera, species, and varieties.

        This private method uses the data_loader module to load plant data into a DataFrame
        and retrieves filter options for genera, species, and varieties.
        """
        self.plants_df = data_loader.load_plants_data()

        self.all_genera, self.all_species, self.all_varieties = \
            data_loader.get_filter_options(self.plants_df)

    def _register_callbacks(self, initial_data):
        """
        Registers callbacks for the Dash application.

        Parameters
        ----------
        initial_data : str
            JSON string representation of the initial plant data.

        This private method registers callbacks using the callbacks module, enabling interactivity
        within the Dash application based on the provided initial data.
        """
        callbacks.register_callbacks(self.app, self.plants_df, initial_data)

    def run(self, debug=True, port=8050):
        """
        Runs the Dash application server.

        Parameters
        ----------
        debug : bool, optional
            If True, enables debug mode for the Dash application (default is True).
        port : int, optional
            The port number on which the Dash server will run (default is 8050).

        This method checks if the application is initialized and runs the Dash server
        with the specified debug mode and port.
        """
        if not self.app:
            self.initialize()

        self.app.run(debug=debug, port=port)
