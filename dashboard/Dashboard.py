import dash

from dashboard import styles, callbacks, layout, data_loader


class Dashboard:
    def __init__(self):
        self.app = None
        self.plants_df = None
        self.all_genera = None
        self.all_species = None
        self.all_varieties = None

    def initialize(self):
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
        self.plants_df = data_loader.load_plants_data()

        self.all_genera, self.all_species, self.all_varieties = \
            data_loader.get_filter_options(self.plants_df)

    def _register_callbacks(self, initial_data):
        callbacks.register_callbacks(self.app, self.plants_df, initial_data)

    def run(self, debug=True, port=8050):
        if not self.app:
            self.initialize()

        self.app.run(debug=debug, port=port)
