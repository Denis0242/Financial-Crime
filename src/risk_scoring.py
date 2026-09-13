def financial_crime_score(kyc_points, pep_flag, total_alerts, repeat_alert, multi_risk, high_risk_geo_ratio, escalations):
    return min(100, round(
        kyc_points + pep_flag*12 + min(total_alerts*4,20) +
        repeat_alert*10 + multi_risk*15 +
        min(high_risk_geo_ratio*40,12) + min(escalations*5,15), 1
    ))
