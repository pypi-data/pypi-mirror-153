import plotly.express as px


class ConfigHeatmap:
    def __init__(self, array, options):
        self.array = array
        self.options = options

        self.fig = px.imshow(array, color_continuous_scale=options['color'])

    def title(self):
        self.fig.update_layout(title_text=self.options['title'])

        if self.options['center_title']:
            self.fig.update_layout(title_x=0.5)

        if self.options['title_pos'] == 'bottom':
            self.fig.update_layout(title_y=0.1)

    def axes(self):
        self.fig.update_xaxes(visible=self.options['x_axis'])
        self.fig.update_yaxes(visible=self.options['y_axis'])

        self.fig.update_layout(xaxis_side=self.options['x_axis_pos'], yaxis_side=self.options['y_axis_pos'])

    def config_all(self):
        self.title()
        self.axes()
