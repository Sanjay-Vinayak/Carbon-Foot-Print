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
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --background-color: #ecf0f1;
            --form-background: #ffffff;
            --text-color: #333333;
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: var(--form-background);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: var(--primary-color);
        }
        form {
            display: grid;
            gap: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="number"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: var(--secondary-color);
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #2980b9;
        }
        .results, .insights, .tips {
            margin-top: 20px;
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
        }
        .results h2, .insights h3, .tips h2 {
            margin-top: 0;
        }
        ul {
            padding-left: 20px;
        }
        @media (max-width: 600px) {
            body {
                padding: 10px;
            }
            .container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Carbon Footprint Monitoring Tool</h1>
        <form id="carbonForm" method="POST">
            <h2>Energy Usage</h2>
            <div>
                <label for="electricity_bill">Average Monthly Electricity Bill in Euros:</label>
                <input type="number" step="0.01" id="electricity_bill" name="electricity_bill" required>
            </div>
            <div>
                <label for="natural_gas_bill">Average Monthly Natural Gas Bill in Euros:</label>
                <input type="number" step="0.01" id="natural_gas_bill" name="natural_gas_bill" required>
            </div>
            <div>
                <label for="fuel_bill">Average Monthly Fuel Bill for Transportation in Euros:</label>
                <input type="number" step="0.01" id="fuel_bill" name="fuel_bill" required>
            </div>
            
            <h2>Waste</h2>
            <div>
                <label for="waste_generated">Total Waste Generated Per Month (kg):</label>
                <input type="number" step="0.01" id="waste_generated" name="waste_generated" required>
            </div>
            <div>
                <label for="recycling_percentage">Percentage of Waste Recycled or Composted (%):</label>
                <input type="number" step="0.01" id="recycling_percentage" name="recycling_percentage" required>
            </div>
            
            <h2>Business Travel</h2>
            <div>
                <label for="business_km">Total Kilometers Traveled Per Year for Business Purposes:</label>
                <input type="number" step="0.01" id="business_km" name="business_km" required>
            </div>
            <div>
                <label for="fuel_efficiency">Average Fuel Efficiency of Vehicles (L/100 km):</label>
                <input type="number" step="0.01" id="fuel_efficiency" name="fuel_efficiency" required>
            </div>
            
            <button type="submit">Calculate Carbon Footprint</button>
        </form>

        <div id="resultsSection" class="results" style="display: none;">
            <h2>Carbon Footprint Results (kgCO2):</h2>
            <ul>
                <li>Energy Usage: <span id="energy_usage"></span></li>
                <li>Waste: <span id="waste"></span></li>
                <li>Business Travel: <span id="business_travel"></span></li>
                <li><strong>Total Carbon Footprint: <span id="total"></span></strong></li>
            </ul>
        </div>

        <div id="insightsSection" class="insights" style="display: none;">
            <h3>Global Contribution and Insights</h3>
            <ul>
                <li>Your carbon footprint is equivalent to <span id="global_percentage"></span>% of the average global per capita carbon footprint (4,800 kgCO2/year).</li>
                <li>Your waste carbon footprint represents <span id="waste_percentage"></span>% of the total carbon footprint.</li>
                <li>Your business travel emissions account for <span id="travel_percentage"></span>% of the total carbon footprint.</li>
            </ul>
        </div>

        <div class="tips">
            <h2>How to Reduce Your Carbon Footprint</h2>
            <ul>
                <li>Use energy-efficient appliances and LED light bulbs</li>
                <li>Improve home insulation to reduce heating and cooling needs</li>
                <li>Use public transportation, carpool, or switch to an electric vehicle</li>
                <li>Reduce, reuse, and recycle to minimize waste</li>
                <li>Choose renewable energy sources like solar or wind power</li>
                <li>Eat more plant-based meals and reduce meat consumption</li>
                <li>Use videoconferencing instead of traveling for business meetings</li>
                <li>Support and implement sustainable practices in your workplace</li>
                <li>Plant trees or support reforestation projects</li>
                <li>Use a programmable thermostat to optimize energy use</li>
            </ul>
        </div>
    </div>

    <script>
        document.getElementById('carbonForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simulate calculation (replace with actual calculation in a real app)
            const results = {
                energy_usage: 1000,
                waste: 500,
                business_travel: 750,
                total: 2250,
                global_percentage: 46.88,
                waste_percentage: 22.22,
                travel_percentage: 33.33
            };

            // Update results
            document.getElementById('energy_usage').textContent = results.energy_usage;
            document.getElementById('waste').textContent = results.waste;
            document.getElementById('business_travel').textContent = results.business_travel;
            document.getElementById('total').textContent = results.total;

            // Update insights
            document.getElementById('global_percentage').textContent = results.global_percentage.toFixed(2);
            document.getElementById('waste_percentage').textContent = results.waste_percentage.toFixed(2);
            document.getElementById('travel_percentage').textContent = results.travel_percentage.toFixed(2);

            // Show results and insights
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('insightsSection').style.display = 'block';
        });
    </script>
</body>
</html>
"""


def calculate_energy_usage(electricity, natural_gas, fuel):
    return (
        ((electricity * 12) * 0.0005)
        + ((natural_gas * 12) * 0.0053)
        + ((fuel * 12) * 2.32)
    )


def calculate_waste_footprint(waste_generated, recycling_percentage):
    return (waste_generated * 12) * (0.57 - (recycling_percentage / 100))


def calculate_business_travel(km_traveled, fuel_efficiency):
    return (km_traveled * (1 / fuel_efficiency)) * 2.31


def calculate_global_percentage(total):
    global_average = 4800  # Average global per capita carbon footprint in kgCO2/year
    return (total / global_average) * 100


@app.route("/", methods=["GET", "POST"])
def carbon_footprint():
    results = None
    if request.method == "POST":
        # Get user inputs
        electricity_bill = float(request.form["electricity_bill"])
        natural_gas_bill = float(request.form["natural_gas_bill"])
        fuel_bill = float(request.form["fuel_bill"])
        waste_generated = float(request.form["waste_generated"])
        recycling_percentage = float(request.form["recycling_percentage"])
        business_km = float(request.form["business_km"])
        fuel_efficiency = float(request.form["fuel_efficiency"])

        # Calculate individual components
        energy_usage = calculate_energy_usage(
            electricity_bill, natural_gas_bill, fuel_bill
        )
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
            "energy_usage": round(energy_usage, 2),
            "waste": round(waste, 2),
            "business_travel": round(business_travel, 2),
            "total": round(total, 2),
            "global_percentage": round(global_percentage, 2),
            "waste_percentage": round(waste_percentage, 2),
            "travel_percentage": round(travel_percentage, 2),
        }

    return render_template_string(HTML_TEMPLATE, results=results)


if __name__ == "__main__":
    app.run(debug=True)
