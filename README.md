# DemoSchedulePuller

# Soccer Schedule Dash App

This Dash application pulls the schedule of soccer games from a Demosphere website, organizes the data into a pandas DataFrame, and allows filtering based on teams and age groups. The filtered data can then be exported as an ics file or printed

## Usage

This app is designed to be used by soccer league organizers who need to view and distribute game schedules from Demosphere. Users can select specific teams and age groups to filter the game schedules, which can then be exported as a ics file or printed for easy distribution.

Make sure to have the following environmental variable, use your UID:

SCED_URL https://app.demosphere.com/_widgets/v1/seasonal_schedule/{UID}/groupings

To run the app, simply execute the script in a Python environment where all dependencies (e.g., Dash, pandas) are installed. The app will be accessible locally via the specified port and can be used interactively through a web browser.

## Dependencies

- Python 3.x
- Dash
- flask
- pandas
- requests (for pulling data from the website)
- ics (for exporting schedules as ics files)
- bs4
- dash_bootstrap_components
- gunicorn