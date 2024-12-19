from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for the input form and results page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carbon Footprint Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="number"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #3498db;
            color: #fff;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .results {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .results ul {
            list-style-type: none;
            padding: 0;
        }
        .results li {
            margin-bottom: 10px;
        }
        .total {
            font-weight: bold;
            color: #e74c3c;
        }
        .flex {
            display: flex;
        }
    </style>
</head>
<body>
    <h1>Carbon Footprint Monitoring Tool</h1>
    <form method="POST">
        <h2>Energy Usage</h2>
        <label for="electricity_bill">Average Monthly Electricity Bill in Euros:</label>
        <input type="number" step="0.01" name="electricity_bill" id="electricity_bill" required>
        
        <label for="natural_gas_bill">Average Monthly Natural Gas Bill in Euros:</label>
        <input type="number" step="0.01" name="natural_gas_bill" id="natural_gas_bill" required>
        
        <label for="fuel_bill">Average Monthly Fuel Bill for Transportation in Euros:</label>
        <input type="number" step="0.01" name="fuel_bill" id="fuel_bill" required>
        
        <h2>Waste</h2>
        <label for="waste_generated">Total Waste Generated Per Month (kg):</label>
        <input type="number" step="0.01" name="waste_generated" id="waste_generated" required>
        
        <label for="recycling_percentage">Percentage of Waste Recycled or Composted (%):</label>
        <input type="number" step="0.01" name="recycling_percentage" id="recycling_percentage" required>
        
        <h2>Business Travel</h2>
        <label for="business_km">Total Kilometers Traveled Per Year for Business Purposes:</label>
        <input type="number" step="0.01" name="business_km" id="business_km" required>
        
        <label for="fuel_efficiency">Average Fuel Efficiency of Vehicles (L/100 km):</label>
        <input type="number" step="0.01" name="fuel_efficiency" id="fuel_efficiency" required>
        
        <button type="submit">Calculate Carbon Footprint</button>
    </form>

    {% if results %}
        <div class="results">
            <h2>Carbon Footprint Results (kgCO2):</h2>
            <div>
                <ul>
                    <li>Energy Usage: {{ results.energy_usage }}</li>
                    <li>Waste: {{ results.waste }}</li>
                    <li>Business Travel: {{ results.business_travel }}</li>
                    <li class="total">Total Carbon Footprint: {{ results.total }}</li>
                </ul>
                <canvas id="myDoughnutChart" width="60" height="60"></canvas>
            </div>

            <h3>Global Contribution and Insights</h3>
            <ul>
                <li>Your carbon footprint is equivalent to {{ results.global_percentage }}% of the average global per capita carbon footprint (4,800 kgCO2/year).</li>
                <li>Your waste carbon footprint represents {{ results.waste_percentage }}% of the total carbon footprint.</li>
                <li>Your business travel emissions account for {{ results.travel_percentage }}% of the total carbon footprint.</li>
            </ul>
        </div>
    {% endif %}

    {% if results %}
    <div class="results">
        <h1>Ways to Reduce Your Carbon Footprint</h1>

        <h2>At Home</h2>
        <ul>
            <li><strong>Switch to Renewable Energy:</strong> Opt for solar, wind, or hydroelectric power if available.</li>
            <li><strong>Improve Energy Efficiency:</strong>
                <ul>
                    <li>Use energy-efficient appliances (Energy Star certified).</li>
                    <li>Replace incandescent bulbs with LEDs.</li>
                    <li>Insulate your home to reduce heating and cooling needs.</li>
                </ul>
            </li>
        </ul>

        <h2>Transportation</h2>
        <ul>
            <li><strong>Reduce Car Use:</strong> Walk, bike, or use public transport when possible. Carpool or rideshare.</li>
            <li><strong>Switch to Electric Vehicles:</strong> Transition to EVs or hybrid vehicles if practical.</li>
            <li><strong>Fly Less:</strong> Opt for virtual meetings, trains, or buses instead of flying. Choose direct flights and offset emissions if necessary.</li>
        </ul>

        <h2>Waste Management</h2>
        <ul>
            <li><strong>Reduce, Reuse, Recycle:</strong>
                <ul>
                    <li>Minimize single-use plastics.</li>
                    <li>Recycle according to local guidelines.</li>
                    <li>Repurpose items instead of discarding them.</li>
                </ul>
            </li>
            <li><strong>Compost:</strong> Divert organic waste from landfills to reduce methane emissions.</li>
        </ul>

        <h2>Personal and Community Actions</h2>
        <ul>
            <li><strong>Plant Trees:</strong> Offset your emissions by planting native trees or supporting reforestation projects.</li>
            <li><strong>Advocate for Policy Change:</strong> Support clean energy and climate policies.</li>
            <li><strong>Educate Others:</strong> Share your sustainable practices to inspire friends and family.</li>
        </ul>
        </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        // Data for the chart
        const data = {
            labels: ['Energy Usage', 'Waste', 'Business Travel'],
            datasets: [{
                label: 'Carbon Footprint Results',
                data: [{{ results.energy_usage }}, {{ results.waste }}, {{ results.business_travel }}],
                borderWidth: 1
            }]
        };

        // Config for the chart
        const config = {
            type: 'doughnut',
            data: data,
        };

        // Render the chart
        const myDoughnutChart = new Chart(
            document.getElementById('myDoughnutChart'),
            config
        );
    </script>
</body>
</html>
"""

def calculate_energy_usage(electricity, natural_gas, fuel):
    return ((electricity * 12) * 0.0005) + ((natural_gas * 12) * 0.0053) + ((fuel * 12) * 2.32)

def calculate_waste_footprint(waste_generated, recycling_percentage):
    return (waste_generated * 12) * (0.57 - (recycling_percentage / 100))

def calculate_business_travel(km_traveled, fuel_efficiency):
    return (km_traveled * (1 / fuel_efficiency)) * 2.31

def calculate_global_percentage(total):
    global_average = 4800  # Average global per capita carbon footprint in kgCO2/year
    return (total / global_average) * 100

@app.route('/', methods=['GET', 'POST'])
def carbon_footprint():
    results = None
    if request.method == 'POST':
        # Get user inputs
        electricity_bill = float(request.form['electricity_bill'])
        natural_gas_bill = float(request.form['natural_gas_bill'])
        fuel_bill = float(request.form['fuel_bill'])
        waste_generated = float(request.form['waste_generated'])
        recycling_percentage = float(request.form['recycling_percentage'])
        business_km = float(request.form['business_km'])
        fuel_efficiency = float(request.form['fuel_efficiency'])

        # Calculate individual components
        energy_usage = calculate_energy_usage(electricity_bill, natural_gas_bill, fuel_bill)
        waste = calculate_waste_footprint(waste_generated, recycling_percentage)
        business_travel = calculate_business_travel(business_km, fuel_efficiency)

        # Calculate total carbon footprint
        total = energy_usage + waste + business_travel

        # Additional statistics
        global_percentage = calculate_global_percentage(total)
        waste_percentage = (waste / total) * 100 if total > 0 else 0
        travel_percentage = (business_travel / total) * 100 if total > 0 else 0

        # Pass results to the template
        results = {
            'energy_usage': round(energy_usage, 2),
            'waste': round(waste, 2),
            'business_travel': round(business_travel, 2),
            'total': round(total, 2),
            'global_percentage': round(global_percentage, 2),
            'waste_percentage': round(waste_percentage, 2),
            'travel_percentage': round(travel_percentage, 2)
        }

    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(debug=True)
