from signalnoise.risk.risk_model import (
    Risk
)
from signalnoise.executive_summary.executive_summary_model import (
    ExecutiveSummary
)

from typing import List

class ExecutiveSummaryGenerator:
    def generate_summary(self, risks:List[Risk], forecast_outlook: str = "No forecast available") -> ExecutiveSummary:
        key_rsiks=[]
        overall_risk ="Low"

        for risk in risks:
            key_rsiks.append(
                f"{risk.signal_type} " f"({risk.severity})"
            )

            if risk.severity == "High":
                overall_risk = "High"
            elif(
                risk.severity =="Medium"
                and overall_risk !="High"
            ):
                overall_risk ="Medium"
        
        summary = f"Key risks identified: {', '.join(key_rsiks)}."

        if overall_risk == "High":
            summary += "Immediate attention is required."
        elif(
            overall_risk =="Medium"
            and overall_risk !="High"
        ):
            summary += "Monitor the risks closely."
        else:
            summary += "No significant risks detected."

        return ExecutiveSummary(
            overall_risk=overall_risk,
            key_risks=key_rsiks,
            forecast_outlook=forecast_outlook,
            summary=summary
        )

