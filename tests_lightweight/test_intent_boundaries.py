"""Rule matching regressions; does not evaluate real-world attack detection."""
import importlib.util
from pathlib import Path
import sys
import pytest

spec = importlib.util.spec_from_file_location("intent_under_test", Path(__file__).parents[1] / "ai_engine/intent_predictor.py")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


@pytest.mark.parametrize("command", ["start", "restart service", "star catalog", "scary", "dumpsite", "exfiltration_notes", "passwordless", "nmaple"])
def test_substrings_do_not_trigger_attack_labels(command):
    assert module.IntentPredictor().predict(command).intent == "low_signal"


@pytest.mark.parametrize("command,intent", [("nmap -sV localhost", "reconnaissance"),
    ("/usr/bin/nmap localhost", "reconnaissance"), ("WHOIS example.test", "reconnaissance"),
    ("hydra localhost", "credential_access"), ("password = test", "credential_access"),
    ("sqlmap --help", "exploit"), ("metasploit", "exploit"),
    ("tar -cf archive.tar files", "exfiltration"), ("scp sample local", "exfiltration"),
    ("dump", "exfiltration")])
def test_known_complete_indicators_still_match(command, intent):
    result = module.IntentPredictor().predict(command)
    assert result.intent == intent
    assert 0 <= result.confidence <= 1
