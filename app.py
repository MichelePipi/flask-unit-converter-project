import math
from flask import Flask, render_template, request

app = Flask(__name__)

### CONSTANTS

# Note all units are shown in comparison to the largest (i.e since Megameters are the largest,
# they are set to 1 in the dict, and Kilometers are set to the quotient of 0.001 and 1 and so forth)

DISTANCE_TYPES = {
    "Mm": 1,  # Mega meter
    "km": math.pow(10, -4),  # Kilometer
    "m": math.pow(10, -6),  # Meter
    "cm": math.pow(10, -8),  # Centimeter
    "mm": math.pow(10, -9),  # Millimeter
}

MASS_TYPES = {
    "t": 1,  # Tonne
    "kg": math.pow(10, -3),  # Kilogram (0.001)
    "g": math.pow(10, -6),  # Gram (0.000001)
    "mg": math.pow(10, -9),  # Millogram (0.000000001)
}

CAPACITY_TYPES = {
    "kL": 1,  # Kiloliter
    "L": math.pow(10, -3),  # Liter (0.001)
    "cL": math.pow(10, -5),  # Centiliter (0.00001)
    "mL": math.pow(10, -6),  # Milliliter (0.000001)
}

VOLUME_TYPES = {
    "km3": 1,  # Cubed kilometer
    "m3": math.pow(10, -9),  # Cubed meter 
    "cm3": math.pow(10, -15),  # Cubed centimeter 
    "mm3": math.pow(10, -18),  # Cubed millimeter (0.000000000000000001)
}


def convert(types: dict, from_unit: str, from_value: float, to_unit: str) -> str:
    """Given a dict of measurements and a target measurement type,
    return a converted measurement."""
    from_type = float(types[from_unit])  # The measurement to convert from
    to_type = float(types[to_unit])  # The measurement to convert to
    result = from_value * (from_type / to_type)  # Multiply the input by the quotient
    # of the from units conversion factors to the target unit

    return str(
        round(result, 20)
    )  # Round to 20 decimals to prevent floating-point errors


@app.route("/", methods=["GET"])
def index():
    """Loads the root page"""
    return render_template("index.html")


@app.route("/converter/<conversion_type>", methods=["GET"])
def load_conversion_form(conversion_type=None):
    """Loads the specified conversion form"""
    return render_template(f"forms/form_{conversion_type}.html")


@app.route("/converter/<conversion_type>", methods=["POST"])
def conversion_result(conversion_type):
    """Takes form information and converts the input type into the target and returns it
    with the conversion result template"""
    types = None  # Determine which dictionary of values to use to convert
    if conversion_type == "distance":
        types = DISTANCE_TYPES
    if conversion_type == "mass":
        types = MASS_TYPES
    if conversion_type == "capacity":
        types = CAPACITY_TYPES
    if conversion_type == "volume":
        types = VOLUME_TYPES

    # Retrieve values from form
    from_unit = request.form["from_unit"]
    from_value = float(request.form["from_value"])
    to_unit = request.form["to_unit"]

    converted = convert(types, from_unit, from_value, to_unit)
    return render_template(
        "conversion_result.html",  # Template name
        from_unit=from_unit,  # Original conversion unit
        invalid=False,  # Input was valid
        from_value=from_value,  # Original value
        to_unit=to_unit,  # Target conversion unit
        converted=converted,  # Converted value
        previous=request.referrer,  # Previous page
    )


app.run(debug=True, port=5001)