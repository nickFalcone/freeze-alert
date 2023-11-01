def run_check_temperature(event, context):
    from temperature_alert import check_temperature
    check_temperature()
