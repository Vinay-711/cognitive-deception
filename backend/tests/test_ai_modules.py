from cognitive_deception.ai.behavior_classifier import BehaviorClassifier
from cognitive_deception.ai.cognitive_bias_predictor import CognitiveBiasPredictor
from cognitive_deception.ai.threat_pattern_detector import ThreatPatternDetector


def test_behavior_classifier_predicts_valid_label():
    classifier = BehaviorClassifier()
    classifier.train(epochs=40)
    pred = classifier.predict("nmap -sV target", typing_speed_cps=4.3, history=[])

    assert pred.label in {"script_kiddie", "automated_bot", "pentester", "apt_actor"}
    assert 0.0 <= pred.confidence <= 1.0
    assert len(pred.feature_vector) == 10


def test_bias_predictor_and_pattern_detector():
    bias = CognitiveBiasPredictor().predict(
        command="hydra -l admin -P creds.txt ssh://10.0.0.2",
        typing_speed_cps=5.0,
        repeats_ratio=0.2,
        attack_label="script_kiddie",
    )
    pattern = ThreatPatternDetector().detect("sqlmap -u http://app?id=1", history=[])

    assert bias.bias in {"overconfidence", "time_pressure", "confirmation_bias", "reconnaissance_pattern"}
    assert pattern.exploit_pattern == "exploit_injection"
