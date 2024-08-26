# Demo Schedule Puller Dashboard

This is a web application built using Flask and Dash to display and manage soccer schedules. The application allows users to filter schedules by team or age group, export the schedules to an iCalendar (.ics) file, and open the schedule in Google Calendar.

## Features

- **Filter by Team or Age Group**: Filter the schedule by selecting a specific team or age group.
- **Export to Calendar**: Export the filtered schedule to an iCalendar (.ics) file.
- **Open in Google Calendar**: Open the first event in the filtered schedule directly in Google Calendar.
- **Responsive Design**: The layout is clean, responsive, and can be printed if needed.

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- Virtual environment (optional but recommended)

### Clone the Repository

```bash
git clone https://github.com/yourusername/soccer-schedule-dashboard.git
cd soccer-schedule-dashboard
```

### Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

You can run the application locally using Flask’s built-in server:

```bash
python app.py
```

### Running with Gunicorn (for Production)

To run the application using `gunicorn` for production, use the following command:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:server
```

- `-w 4` specifies the number of worker processes.
- `-b 0.0.0.0:8000` binds the server to all network interfaces on port 8000.

### Accessing the Application

Once the server is running, open your web browser and go to:

```
http://127.0.0.1:8000/
```

### Exporting Schedules

- **Filter the Schedule**: Use the dropdown menus to filter by team or age group.
- **Export to Calendar**: Click the "Export to Calendar" button to download the schedule as an iCalendar (.ics) file.
- **Open in Google Calendar**: Click the "Open in Google Calendar" button to add the first event to your Google Calendar.

## Project Structure

```
.
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── static/                 # Static files (CSS, JS, images)
```

## Deployment

### Deploying to Heroku

1. **Create a `Procfile`:**

    ```
    web: gunicorn -w 4 -b 0.0.0.0:$PORT app:server
    ```

2. **Push to Heroku:**

    ```bash
    git add .
    git commit -m "Deploying to Heroku"
    git push heroku master
    ```

### Deploying to AWS or Other Cloud Providers

Follow the respective cloud provider's documentation to deploy a Flask application.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License