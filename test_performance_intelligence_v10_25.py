from brain.performance_intelligence_v10_25 import PerformanceIntelligenceV10_25


def run_test():

    print(
        "========== PERFORMANCE INTELLIGENCE V10.25 =========="
    )


    intelligence = PerformanceIntelligenceV10_25()


    result = {
        "trades": [
            {
                "status":"EXECUTED"
            }
        ],
        "feedback":[
            {
                "status":"INTELLIGENCE_UPDATED"
            }
        ]
    }


    analysis = intelligence.analyze(
        result
    )


    print("\nANALYSIS:")
    print(analysis)


    print("\nSTATE:")
    print(
        intelligence.state()
    )


    assert analysis["performance_score"] == 100
    assert analysis["mode"] == "OPTIMAL"


    print(
        "\nPERFORMANCE INTELLIGENCE V10.25 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
