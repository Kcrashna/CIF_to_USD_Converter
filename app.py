from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://www.nrb.org.np/api/forex/v1/rate"

@app.route('/', methods=['GET', 'POST'])
def index():
    exchange_rate = None
    selected_date = None
    cif_value = None
    cif_in_usd = None
    error_message = None
    step = 1  # Track step: 1 = select date, 2 = enter CIF

    if request.method == 'POST':
        selected_date = request.form.get('date')
        cif_input = request.form.get('cif')

        try:
            response = requests.get(API_URL, params={'date': selected_date})
            data = response.json()

            if data['status']['code'] == 200:
                rates = data['data']['payload']['rates']
                for rate in rates:
                    if rate['currency']['iso3'] == 'USD':
                        exchange_rate = float(rate['buy'])
                        break

                if exchange_rate is None:
                    error_message = "USD exchange rate not found for the selected date."
                else:
                    step = 2  # Allow CIF input
            else:
                error_message = "Data fetch failed with status code: " + str(data['status']['code'])

            # Process CIF only if entered and rate is available
            if cif_input and exchange_rate:
                try:
                    cif_value = float(cif_input)
                    cif_in_usd = round(cif_value / exchange_rate, 2)
                except ValueError:
                    error_message = "Invalid CIF value entered."

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    return render_template('index.html',
                           exchange_rate=exchange_rate,
                           selected_date=selected_date,
                           cif_value=cif_value,
                           cif_in_usd=cif_in_usd,
                           error_message=error_message,
                           step=step)

if __name__ == '__main__':
    app.run(debug=True)
