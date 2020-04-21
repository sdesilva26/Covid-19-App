# Covid 19 Visualisations

![Alt Text](covid-19-web-app-demo-2.gif)

## Web App

I have deployed this app at: https://covid-19-uk-bokeh-plots.herokuapp.com/Covid_19_Plots for
 people to view.

## Run the app locally

To run this project locally follows these steps:

1. Clone this repo git clone https://github.com/sdesilva26/Covid-19-App.git
2. Install the dependencies in the requirements.txt
3. [optional] Get the latest data from NHS england by running
    ``` 
    python ./scripts/data_script.py "./data/COVID-19-total-announced-deaths.xlsx"
    ```
     *NOTE: if you change the filename here by specifying a different argument in the command above
    you will need to change the filepath in main.py*

4. Create a Google Maps API key by following the instructions [here](https://developers.google.com/maps/documentation/javascript/get-api-key)
5. Set the google api you just generated as an environment variable with the name "GOOGLE_API_KEY"
6. From the repository root run the command
``` 
bokeh serve --show Covid_19_Plots/
```
The app should now pop up in your internet browser in a new window
7. [optional] To keep the data up to date set up a cron job that runs the cron_script.sh daily
 after 2pm as this is when NHS England's daily data release occurs 




